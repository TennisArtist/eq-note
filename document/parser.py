# document/parser.py

import re
from typing import List, Tuple

from document.document_model import DocumentModel
from document.element import (
    BaseElement,
    TextElement,
    LatexElement,
    PlotElement,
    ImageElement,
    PythonElement,
)


class DocumentParser:

    def __init__(self):
        self._id_counter = 0

    def _next_id(self):
        self._id_counter += 1
        return f"e{self._id_counter}"

    """
    EQ-Note v2 文件解析器：
    將 Markdown + LaTeX + plot 指令解析成 Element 列表。

    升級版特點：
      - 仍然以「空白行」切 block（穩定簡單）
      - 先偵測：
          1. Python code block：```python ... ```
          2. Plot 指令（plot_data, plot3d, plot$$, ...）
          3. 純 LaTeX display block：
                a) $$ ... $$
                b) \[ ... \]
          4. <img ...> 圖片
          5. 其他全部當作 TextElement（裡面可含 $...$ / \(...\)）
    """

    # =========================================================
    # Plot 指令樣式
    # =========================================================
    _plot_patterns: List[Tuple[str, str]] = [
        # LaTeX 3D（plot3d$$ z = ... $$）
        (r'plot3d\$\$(.*?)\$\$', "3d_latex"),

        # LaTeX 2D（plot$$ y = ... $$）
        (r'plot\$\$(.*?)\$\$', "2d_latex"),

        # Data 3D：plot3d_data("file.txt")
        (r'plot3d_data\(\s*[\'"](.+?)[\'"]\s*\)', "3d_data"),

        # Data 2D：plot_data("file.txt")
        (r'plot_data\(\s*[\'"](.+?)[\'"]\s*\)', "2d_data"),

        # Python 3D：plot3d('sin(x)*cos(y)', -5,5,-5,5)
        (
            r'plot3d\(\s*[\'"](.+?)[\'"]\s*,\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*\)',
            "3d_py",
        ),

        # Python 2D：plot('sin(x)', -5, 5)
        (
            r'plot\(\s*[\'"](.+?)[\'"]\s*,\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*\)',
            "2d_py",
        ),
    ]

    # 純 LaTeX display block（整個 block 就是數學，不含其他文字）

    # 1) $$ ... $$ 形式
    _display_dollar_re = re.compile(
        r"^\s*\$\$(.*?)\$\$\s*$",
        flags=re.DOTALL,
    )

    # 2) \[ ... \] 形式
    _display_bracket_re = re.compile(
        r"^\s*\\\[(.*?)\\\]\s*$",
        flags=re.DOTALL,
    )

    # 圖片 <img src="...">
    _img_pattern = re.compile(
        r'<img\s+src=\"(.+?)\"(?:\s+width=\"(\d+)\")?\s*>'
    )

    # Inline LaTeX：
    # 1) \( ... \)
    _inline_paren_re = re.compile(r'\\\((.+?)\\\)')

    # 2) $ ... $（避免 $$）
    _inline_dollar_re = re.compile(
        r'(?<!\$)\$(.+?)\$(?!\$)'
    )

    # =========================================================
    # 主解析入口
    # =========================================================
    def parse(self, raw_text: str) -> DocumentModel:
        elements: List[BaseElement] = []

        # 1. 以空白行拆段
        blocks = re.split(r"\n\s*\n", raw_text)

        for block in blocks:
            block = block.strip()
            if not block:
                continue

            elems = self._parse_block(block)
            elements.extend(elems)

        return DocumentModel(elements)

    # =========================================================
    # 解析單一 block
    # =========================================================
    def _parse_block(self, block: str) -> List[BaseElement]:
        """
        解析單一段落 block，優先序：
          1. Python code block
          2. Plot 指令
          3. 純 LaTeX display block：$$...$$ 或 \[...\]
          4. Image
          5. Text（含 inline LaTeX：\( ... \)、$ ... $）
        """

        # ----------- 0. Python Code Block ----------- #
        py_match = re.match(r"```python(.*?)```", block, flags=re.DOTALL)
        if py_match:
            code = py_match.group(1).strip()
            return [PythonElement(code=code, elem_id=self._next_id())]

        # ----------- 1. Plot 指令 ----------- #
        plot_results: List[BaseElement] = []

        for pattern, kind in self._plot_patterns:
            for m in re.finditer(pattern, block, flags=re.DOTALL):
                groups = m.groups()

                if kind in ("2d_latex", "3d_latex"):
                    code = groups[0].strip()
                    plot_results.append(
                        PlotElement(code=code, kind=kind, id=self._next_id())
                    )
                else:
                    plot_results.append(
                        PlotElement(code=groups, kind=kind, id=self._next_id())
                    )

        if plot_results:
            return plot_results

        # ----------- 2. 純 LaTeX display block ----------- #
        m = self._display_dollar_re.match(block)
        if m:
            return [LatexElement(latex=m.group(1).strip(), id=self._next_id())]

        m = self._display_bracket_re.match(block)
        if m:
            return [LatexElement(latex=m.group(1).strip(), id=self._next_id())]

        # ----------- 3. Image ----------- #
        img_results = []
        for m in re.finditer(self._img_pattern, block):
            src = m.group(1)
            width = int(m.group(2)) if m.group(2) else None
            img_results.append(
                ImageElement(src=src, width=width, id=self._next_id())
            )

        if img_results:
            return img_results

        # ----------- 4. Text + Inline LaTeX ----------- #
        elements: List[BaseElement] = []

        patterns = [
            self._inline_paren_re,  # \( ... \) → display
            self._inline_dollar_re,  # $ ... $   → inline
        ]

        matches = []
        for pat in patterns:
            for m in pat.finditer(block):
                matches.append((m.start(), m.end(), m.group(1), pat))

        if not matches:
            return [TextElement(text=block, id=self._next_id(), meta={"text_kind": "block"})]

        matches.sort(key=lambda x: x[0])

        last = 0
        for start, end, latex_code, pat in matches:
            # 前段文字
            if start > last:
                elements.append(
                    TextElement(
                        text=block[last:start],
                        id=self._next_id(),
                        meta={"text_kind": "inline"}
                    )
                )

            # LaTeX 本體
            if pat is self._inline_dollar_re:
                # $...$ → inline
                elements.append(
                    LatexElement(
                        latex=latex_code.strip(),
                        id=self._next_id(),
                        meta={"inline": True}
                    )
                )
            else:
                # \( ... \) → display
                elements.append(
                    LatexElement(
                        latex=latex_code.strip(),
                        id=self._next_id()
                    )
                )

            last = end

        # 剩餘文字
        if last < len(block):
            elements.append(
                TextElement(
                    text=block[last:],
                    id=self._next_id(),
                    meta={"text_kind": "inline"}
                )
            )

        return elements




