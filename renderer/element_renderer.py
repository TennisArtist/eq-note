# renderer/element_renderer.py
import markdown2
import html  # ★ 新增：為了 escape 輸出內容

from document.element import (
    BaseElement,
    TextElement,
    LatexElement,
    PlotElement,
    ImageElement,
    PythonElement
)

import re
from latex.constants import MATH_TOKEN_L, MATH_TOKEN_R


_math_inline_re = re.compile(r"\$(.+?)\$", re.DOTALL)


def protect_math(text: str):
    math_map = {}
    idx = 0

    def repl(m):
        nonlocal idx
        # key = f"\uFFF0{idx}\uFFF1"
        key = f"{MATH_TOKEN_L}{idx}{MATH_TOKEN_R}"
        math_map[key] = m.group(0)
        idx += 1
        return key

    text = _math_inline_re.sub(repl, text)
    return text, math_map


class ElementRenderer:
    def __init__(self, plot_renderer, python_renderer=None):
        self.plot_renderer = plot_renderer
        self.python_renderer = python_renderer

    def render_element(self, elem: BaseElement) -> str:
        if isinstance(elem, TextElement):
            return self._render_text(elem)
        elif isinstance(elem, LatexElement):
            return self._render_latex(elem)
        elif isinstance(elem, PlotElement):
            return self._render_plot(elem)
        elif isinstance(elem, ImageElement):
            return self._render_image(elem)
        elif isinstance(elem, PythonElement):
            return self._render_python(elem)
        return ""

    def _render_text(self, elem: TextElement) -> str:
        """
        【渲染順序（不可改）】
        1. 還原 LaTeX token
        2. 保護數學（避免 Markdown 介入）
        3. Markdown → HTML
        4. 還原數學
        """

        text = elem.text

        # 1) 還原 LaTeX token
        token_map = getattr(self.doc_model, "latex_token_map", {})
        for token in sorted(token_map.keys(), key=len, reverse=True):
            text = text.replace(token, token_map[token].raw)

        # 2) ★ 保護數學，避免 Markdown 碰到 _
        text, math_map = protect_math(text)

        # 3) Markdown（必須啟用 mathjax）
        html = markdown2.markdown(
            text,
            extras=[
                "tables",
                "fenced-code-blocks",
                "strike",
                "task_list",
                "no-intra-emphasis",
            ]
        )

        # 4) ★ 還原數學
        for key, math in math_map.items():
            html = html.replace(key, math)

        return html

    def _render_latex(self, elem: LatexElement) -> str:
        if elem.meta and elem.meta.get("inline"):
            # inline math：不換行
            return f"<span>\\({elem.latex}\\)</span>"
        else:
            # display math
            return f"<div>$$ {elem.latex} $$</div>"

    def _render_plot(self, elem: PlotElement) -> str:
        return self.plot_renderer.render_plot_element(elem)

    def _render_image(self, elem: ImageElement) -> str:
        if elem.width:
            return f'<img src="{elem.src}" width="{elem.width}">'
        return f'<img src="{elem.src}">'

    # =========================================================
    # ★ 修改重點：同時渲染程式碼與結果
    # =========================================================
    def _render_python(self, elem: PythonElement) -> str:
        elem_id = elem.id
        code_html = html.escape(elem.code)

        # output HTML，如果沒有輸出保持空白
        output_html = (
            f"<pre>{html.escape(elem.output)}</pre>" if elem.output else ""
        )

        return f"""
    <div class="py-block" id="block-{elem_id}"
         style="border:1px solid #444; padding:6px; margin:10px 0;">

        <div style="text-align:right;">
            <button onclick="runBlock('{elem_id}')"
                    style="font-size:12px; padding:2px 6px;">Run</button>
        </div>

        <pre class="python-code">{code_html}</pre>

        <div class="python-output" id="output-{elem_id}">
            {output_html}
        </div>
    </div>
    """
