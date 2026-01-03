# core_plot_data.py
import numpy as np
import json
from datetime import datetime

class PlotDataEngine:
    """
    讀取 2D/多欄實驗數據，並生成 Plotly 的 2D 線圖 HTML 片段。
    支援：
       x y1 y2 y3 ...
       有或沒有 header 都可
    """

    @staticmethod
    def load_xy_multi(filepath: str):
        """
        回傳：
            x: 一維 ndarray
            ys: 多條線的 list，每條都是 ndarray
            labels: ["x", "y1", "y2", ...]
        """

        # 讀第一行看是否為 header
        with open(filepath, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()

        cols = first_line.split()
        has_header = False

        if len(cols) >= 2:
            try:
                float(cols[0]); float(cols[1])
            except:
                has_header = True

        if has_header:
            # 跳過 header
            data = np.loadtxt(filepath, skiprows=1)
            labels = cols  # header 名稱
        else:
            data = np.loadtxt(filepath)
            ncol = data.shape[1]
            labels = ["x"] + [f"y{i}" for i in range(1, ncol)]

        if data.ndim == 1 or data.shape[1] < 2:
            raise ValueError("資料至少需要兩欄（x 與至少一條 y）。")

        x = data[:, 0]
        ys = [data[:, i] for i in range(1, data.shape[1])]

        return x, ys, labels

    @staticmethod
    def make_xy_plot(filepath: str, dark_mode=True):
        """
        回傳可嵌入 HTML 的 <div> + <script>，自動畫多條線。
        """

        x, ys, labels = PlotDataEngine.load_xy_multi(filepath)

        # labels[0] 是 x label，其餘是 y labels
        x_label = labels[0]
        y_labels = labels[1:]

        div_id = "plotdata_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        js_div = json.dumps(div_id)
        js_x = json.dumps(x.tolist())

        bg = "#000000" if dark_mode else "#ffffff"
        fg = "#ffffff" if dark_mode else "#000000"

        # 建立 JS data list
        js_data_lines = []
        palette = ["#ff5733", "#33c1ff", "#9dff33", "#ff33ed", "#febf00", "#62ffda"]

        for i, y in enumerate(ys):
            js_y = json.dumps(y.tolist())
            color = json.dumps(palette[i % len(palette)])
            name = json.dumps(y_labels[i])

            js_data_lines.append(f"""
            {{
                x: {js_x},
                y: {js_y},
                mode: 'lines+markers',
                name: {name},
                line: {{color: {color}, width: 2}}
            }}
            """)

        js_data = ",\n".join(js_data_lines)

        html = f"""
<div id="{div_id}" style="width:100%; height:400px;"></div>
<script>
(function() {{
  var data = [
    {js_data}
  ];

  var layout = {{
      margin: {{l: 50, r: 10, t: 30, b: 50}},
      paper_bgcolor: {json.dumps(bg)},
      plot_bgcolor: {json.dumps(bg)},
      font: {{color: {json.dumps(fg)}}},
      xaxis: {{title: {json.dumps(x_label)}, color: {json.dumps(fg)}}},
      yaxis: {{title: 'value', color: {json.dumps(fg)}}},
      legend: {{
        x: 1.02,
        y: 1,
        bgcolor: {json.dumps(bg)}
      }}
  }};

  Plotly.newPlot({js_div}, data, layout);
}})();
</script>
"""
        return html
