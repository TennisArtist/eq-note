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
        kind = (elem.meta or {}).get("text_kind", "block")

        # 行內片段：仍然維持原本策略（不走 Markdown）
        if kind == "inline":
            return html.escape(elem.text)

        # ===== 路線 A：Block 文字 → 交給 Markdown =====
        html_out = markdown2.markdown(
            elem.text,
            extras=[
                "fenced-code-blocks",
                "tables",
                "strike",
            ]
        )

        return html_out

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
