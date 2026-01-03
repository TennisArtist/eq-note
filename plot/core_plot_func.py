# core_plot_func.py
import numpy as np
import json
import re
from datetime import datetime

class PlotFunc2DEngine:
    """
    從 LaTeX 形式的 2D 函數（含多條）產生 Plotly 互動圖的 HTML 片段。

    支援語法範例：

      plot$$ y = \sin(x) $$

      plot$$ y = \sin(x), \cos(x), \frac{x}{5} $$

      plot$$ y = \sin(x)[red], \cos(x)[dashed], \frac{x}{5}[green dotted], x∈[-3,7] $$

    功能：
      - 多條線自動顏色
      - 可指定顏色 / 線型：
            [red] [blue dotted] [#ffaa00 dashed]
      - 支援 x 範圍：x∈[a,b] 或 x in [a,b]
    """

    @staticmethod
    def _split_top_level(expr: str):
        """
        以逗號分割多個函數，但避免在括號/大括號內切開。
        """
        parts = []
        buf = []
        depth = 0
        for ch in expr:
            if ch in '({[':
                depth += 1
            elif ch in ')}]':
                depth = max(0, depth - 1)
            if ch == ',' and depth == 0:
                parts.append(''.join(buf))
                buf = []
            else:
                buf.append(ch)
        if buf:
            parts.append(''.join(buf))
        return [p.strip() for p in parts if p.strip()]

    @staticmethod
    def _parse_style(style_spec: str, idx: int):
        """
        解析 [ ... ] 中的樣式：顏色 + 線型。
        例如：[red dashed]、[green dotted]、[#ffaa00]
        """
        palette = ["#ff5733", "#33c1ff", "#9dff33", "#ff33ed", "#febf00", "#62ffda"]
        line_default = "solid"

        if not style_spec:
            color = palette[idx % len(palette)]
            dash = line_default
            return color, dash

        tokens = re.split(r"[\s,]+", style_spec.strip())
        color = None
        dash = None

        linestyle_map = {
            "solid": "solid",
            "dash": "dash",
            "dashed": "dash",
            "dot": "dot",
            "dotted": "dot",
            "dashdot": "dashdot",
        }

        for t in tokens:
            if not t:
                continue
            tl = t.lower()
            if tl in linestyle_map:
                dash = linestyle_map[tl]
            elif tl.startswith("#"):
                color = t
            else:
                # 視為顏色名稱，例如 red, blue, green ...
                color = t

        if color is None:
            color = palette[idx % len(palette)]
        if dash is None:
            dash = line_default
        return color, dash

    @staticmethod
    def make_from_latex(latex_str: str, dark_mode=True):
        """
        給定 'y = ...' 或純函數列表的 LaTeX，回傳 Plotly 2D 圖的 HTML 片段。
        """
        from latex.core_latex import LatexPlotEngine  # 延遲 import 避免循環

        body = latex_str.strip().strip('$')

        # 先處理 x 範圍： x∈[-5,5] 或 x in [-5,5]
        x_min, x_max = -10.0, 10.0
        range_match = re.search(
            r'x\s*(?:∈|in)\s*\[([\-]?\d+(?:\.\d+)?),\s*([\-]?\d+(?:\.\d+)?)\]',
            body
        )
        if range_match:
            x_min, x_max = map(float, range_match.groups())
            body = re.sub(
                r'x\s*(?:∈|in)\s*\[[^\]]+\]',
                '',
                body
            )

        body = body.strip().rstrip(',')

        # 拿掉 y = 前綴（若有）
        if '=' in body:
            _, rhs = body.split('=', 1)
            expr_part = rhs.strip()
        else:
            expr_part = body

        # 以 top-level 逗號分割多個函數
        func_items = PlotFunc2DEngine._split_top_level(expr_part)

        if not func_items:
            raise ValueError("plot$$ 找不到任何函數。")

        # 把每個項目拆成「表達式」＋「樣式」
        expr_entries = []  # (expr_py, style_spec, expr_latex_for_label)
        for item in func_items:
            # 抓 [ ... ] 樣式
            m = re.match(r'(.+?)\[(.+)\]\s*$', item)
            if m:
                expr_latex = m.group(1).strip()
                style_spec = m.group(2).strip()
            else:
                expr_latex = item.strip()
                style_spec = None

            expr_py = LatexPlotEngine._latex_to_python(expr_latex)
            expr_entries.append((expr_py, style_spec, expr_latex))

        # 準備 x
        x = np.linspace(x_min, x_max, 600)

        # 計算每條 y(x)
        y_list = []
        labels = []
        styles = []
        for idx, (expr_py, style_spec, expr_latex) in enumerate(expr_entries):
            try:
                y = eval(expr_py, {
                    "np": np,
                    "x": x,
                    "sin": np.sin,
                    "cos": np.cos,
                    "tan": np.tan,
                    "exp": np.exp,
                    "sqrt": np.sqrt,
                    "pi": np.pi,
                })
            except Exception as e:
                raise ValueError(f"2D 公式運算失敗：{e}\n轉換後: {expr_py}")

            y_list.append(np.asarray(y))
            labels.append(expr_latex)
            styles.append(PlotFunc2DEngine._parse_style(style_spec, idx))

        # 準備 Plotly HTML
        div_id = "plot2d_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        js_div = json.dumps(div_id)
        js_x = json.dumps(x.tolist())

        bg = "#000000" if dark_mode else "#ffffff"
        fg = "#ffffff" if dark_mode else "#000000"

        traces_js = []
        for idx, y in enumerate(y_list):
            js_y = json.dumps(y.tolist())
            name = json.dumps(labels[idx])
            color, dash = styles[idx]
            js_color = json.dumps(color)
            js_dash = json.dumps(dash)

            traces_js.append(f"""
    {{
      x: {js_x},
      y: {js_y},
      mode: 'lines',
      name: {name},
      line: {{color: {js_color}, dash: {js_dash}, width: 2}}
    }}""")

        js_traces = ",\n".join(traces_js)
        js_bg = json.dumps(bg)
        js_fg = json.dumps(fg)
        js_xlabel = json.dumps("x")
        js_ylabel = json.dumps("y")

        html = f"""
<div id="{div_id}" style="width:100%; height:400px;"></div>
<script>
(function() {{
  var data = [
{js_traces}
  ];

  var layout = {{
    margin: {{l: 60, r: 10, t: 30, b: 50}},
    paper_bgcolor: {js_bg},
    plot_bgcolor: {js_bg},
    font: {{color: {js_fg}}},
    xaxis: {{title: {js_xlabel}, color: {js_fg}}},
    yaxis: {{title: {js_ylabel}, color: {js_fg}}},
    legend: {{
      x: 1.02,
      y: 1,
      bgcolor: {js_bg}
    }}
  }};

  Plotly.newPlot({js_div}, data, layout);
}})();
</script>
"""
        return html
