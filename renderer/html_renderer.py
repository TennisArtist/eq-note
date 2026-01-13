# renderer/html_renderer.py

import os
from PyQt5.QtCore import QUrl

from renderer.plot_renderer import PlotRenderer
from .element_renderer import ElementRenderer
import re

# ★ 你原本的 HTML_TEMPLATE — 完整保留（我沒有動它）
HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html>
<head>

<script src="qrc:///qtwebchannel/qwebchannel.js"></script>

<script>
var bridge = null;

new QWebChannel(qt.webChannelTransport, function(channel) {
    bridge = channel.objects.bridge;

    bridge.executionFinished.connect(function(id, html_output) {
        let out = document.getElementById("output-" + id);
        if (out) out.innerHTML = html_output;
    });
});

function runBlock(id) {
    if (bridge) bridge.runBlock(id);
}
</script>

<meta charset="utf-8">
<script>
  window.MathJax = {
    loader: {
      load: ['[tex]/braket', '[tex]/physics', '[tex]/mhchem', '[tex]/ams']
    },
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']],
      displayMath: [['$$','$$'], ['\\[','\\]']],
      processEscapes: true,
      packages: {'[+]': ['braket', 'physics', 'mhchem', 'ams']},
      macros: {
        abs: ['\\left| #1 \\right|', 1],
        norm: ['\\left\\lVert #1 \\right\\rVert', 1],
        vec: ['\\boldsymbol{#1}', 1],
        Tr: '\\operatorname{Tr}',
        grad: '\\nabla',
        div:  '\\nabla\\cdot',
        curl: '\\nabla\\times'
      }
    },
    svg: {fontCache: 'global'}
  };
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>

<style>
body {
  font-family: 'Consolas', monospace;
  margin: 15px;
  line-height: 1.5;
  word-wrap: break-word;
  overflow-wrap: break-word;
}
img {
  display: block;
  margin: 10px auto;
  max-width: 90%;
}
</style>
</head>
<body>
<div id="content">%%CONTENT%%</div>
<script>
  document.addEventListener("DOMContentLoaded", () => {
    MathJax.typesetPromise();
  });
</script>
</body>
</html>
"""


class HtmlRenderer:
    """
    HtmlRenderer（新版）
    ★ 接受 DocumentModel
    ★ 呼叫 ElementRenderer 渲染 Element
    ★ 套入 HTML_TEMPLATE
    """

    def __init__(self, dark_mode=True):
        self.dark_mode = dark_mode

        # PlotRenderer 用於 PlotElement
        self.plot_renderer = PlotRenderer(dark_mode=dark_mode)

        # ElementRenderer 用於每個 Element → HTML
        self.element_renderer = ElementRenderer(self.plot_renderer)

    # ----------------------------------------------------------------------
    # ★ 新版 render：吃 DocumentModel，不吃 raw_text
    # ----------------------------------------------------------------------
    def render(self, doc_model):
        """
        doc_model: DocumentModel
        回傳 (html, base_url)
        """

        # 1) 把所有 Element 轉成 HTML block
        html_blocks = []
        for elem in doc_model.elements:
            block_html = self.element_renderer.render_element(elem)
            html_blocks.append(block_html)

        # 2) 合併
        html_body = "\n".join(html_blocks)

        # -----------------------------
        # 2.5) 關閉斜體 <em> / <i>
        # -----------------------------
        html_body = re.sub(r"</?em>", "", html_body)
        html_body = re.sub(r"</?i>", "", html_body)

        # --------------------
        # 3) 主題處理 (dark/light)
        # （保留原本的背景、字色、code 配色）
        # --------------------
        # 專業深色模式配色建議
        bg = "#212121" if self.dark_mode else "#E3C65B"  # 背景不再是死黑
        fg = "#E3E3E3" if self.dark_mode else "#000"  # 字體柔和一點
        code_bg = "#171717" if self.dark_mode else "#f5f5f5"  # 程式碼區塊稍微亮起來
        border_color = "#2D2D2D" if self.dark_mode else "#ccc"  # 邊框與背景融合更好

        html_style = f"""
        <style>
        body {{
            background-color: {bg};
            color: {fg};
            font-family: Consolas, monospace;
        }}
        pre, code {{
            background-color: {code_bg};
            color: {fg};
            border-radius: 4px;
            padding: 2px 4px;
        }}
        img {{
            border: 1px solid {border_color};
            margin: 10px auto;
            display: block;inlineMath
        }}
        
        h1 {{
            color: {"#E63F00" if self.dark_mode else "#000"};
            font-weight: bold;
        }}
        
        h2 {{
            color: {"#FFDDAA" if self.dark_mode else "#000"};
            font-weight: bold;
        }}
        
        h3 {{
            color: {"#DDFF77" if self.dark_mode else "#000"};
            font-weight: bold;
        }}
        
        h4 {{
            color: {"#66FF66" if self.dark_mode else "#000"};
            font-weight: bold;
        }}
        
        h5 {{
            color: {"#337357" if self.dark_mode else "#000"};
            font-weight: bold;
        }}
        
        h6 {{
            color: {"#FF0000" if self.dark_mode else "#000"};
        }}
        blockquote {{
            border-left: 4px solid {"#E6C300" if self.dark_mode else "#003399"};
            margin: 10px 0;
            padding: 8px 12px;
            background: {"#0D0D0D" if self.dark_mode else "#eef3ff"};
            color: {fg};
        }}
        blockquote p {{
            margin: 0;
        }}
        table {{
            border-collapse: collapse;
            margin: 12px 0;
            width: 100%;
        }}
        th, td {{
            border: 1px solid {border_color};
            padding: 6px 10px;
        }}
        th {{
            background-color: {"#333" if self.dark_mode else "#dde7ff"};
            color: {fg};
        }}
        td {{
            background-color: {"#111" if self.dark_mode else "#ffffff"};
            color: {fg};
        }}
        pre {{
            padding: 10px;
            border-radius: 6px;
            border: 1px solid {border_color};
            overflow-x: auto;
            font-size: 12pt;
        }}
        code {{
            font-family: Consolas, monospace;
            font-size: 12pt;
        }}

        /* ============================================================= */
        /* ★ 新增：Python Block 雙欄（程式碼 + 輸出）美化樣式           */
        /* ============================================================= */

        .python-container {{
            border-radius: 6px;
            overflow: hidden; /* 讓外框圓角生效 */
            margin-bottom: 20px;
            border: 1px solid {border_color};
        }}

        .python-code pre {{
            background-color: {code_bg};
            color: {fg};
            padding: 10px;
            margin: 0;
            border: none;
            border-radius: 0;
        }}

        .python-output pre {{
            background-color: {"#222" if self.dark_mode else "#fff"};
            color: {"#ddd" if self.dark_mode else "#333"};
            padding: 10px;
            margin: 0;
            border: none;
            border-top: 1px solid {border_color};
            font-size: 0.95em; /* 輸出字小一點 */
        }}
        </style>
        """

        # --------------------
        # 4) 套入 template
        # --------------------
        full_html = HTML_TEMPLATE.replace("%%CONTENT%%", html_style + html_body)

        # ★ Debug：匯出渲染後的 HTML （為了找 Crash 的根源）
        with open("debug_output.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        # --------------------
        # 5) base_url（圖片 / Plotly）
        # --------------------
        base_url = QUrl.fromLocalFile(os.getcwd() + "/")

        return full_html, base_url
