# core_plot3d.py
import numpy as np
import json
from datetime import datetime
import os

class Plot3DEngine:
    """
    產生可由 Plotly 渲染的 3D 曲面 HTML 片段。

    支援兩種來源：
    1) 函數：   make_surface_from_func(expr_py, x_min, x_max, y_min, y_max, dark_mode, label)
    2) 資料檔： make_surface_from_xyz_file(filepath, dark_mode, label)
       檔案格式為 3 欄 (x, y, z)，可含或不含 header：
         x y z
         0 0 1.0
         0 1 1.2
         ...
    """

    # --------- 共用：把 X,Y,Z 轉成 Plotly 3D HTML ---------
    @staticmethod
    def _surface_html_from_grid(X, Y, Z, dark_mode=True, label=None, div_id=None):
        if div_id is None:
            div_id = "plot3d_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        if label is None:
            label = "3D surface"

        x = X[0, :]               # meshgrid 結構，第一列就是所有 x
        y = Y[:, 0]               # 第一欄就是所有 y
        Z = np.asarray(Z)

        x_list = x.tolist()
        y_list = y.tolist()
        z_list = Z.tolist()

        bg = "#000000" if dark_mode else "#ffffff"
        fg = "#ffffff" if dark_mode else "#000000"

        js_x = json.dumps(x_list)
        js_y = json.dumps(y_list)
        js_z = json.dumps(z_list)
        js_div = json.dumps(div_id)
        js_title = json.dumps(label)
        js_bg = json.dumps(bg)
        js_fg = json.dumps(fg)

        html = f"""
<div id="{div_id}" style="width:100%; height:400px;"></div>
<script>
(function() {{
  var x = {js_x};
  var y = {js_y};
  var z = {js_z};

  var data = [{{
    type: "surface",
    x: x,
    y: y,
    z: z
  }}];

  var layout = {{
    margin: {{l: 0, r: 0, t: 30, b: 0}},
    paper_bgcolor: {js_bg},
    plot_bgcolor: {js_bg},
    scene: {{
      xaxis: {{title: "x", color: {js_fg}}},
      yaxis: {{title: "y", color: {js_fg}}},
      zaxis: {{title: "z", color: {js_fg}}}
    }},
    title: {js_title},
    font: {{color: {js_fg}}}
  }};

  Plotly.newPlot({js_div}, data, layout);
}})();
</script>
"""
        return html

    # --------- 情況 1：由函數 f(x,y) 構建 3D 曲面 ---------
    @staticmethod
    def make_surface_from_func(expr_py: str,
                               x_min: float = -5, x_max: float = 5,
                               y_min: float = -5, y_max: float = 5,
                               dark_mode: bool = True,
                               label: str = None) -> str:
        """
        expr_py: 可被 eval 的 numpy 表達式，例如 "np.sin(x)*np.cos(y)"
        """
        nx, ny = 40, 40
        x = np.linspace(x_min, x_max, nx)
        y = np.linspace(y_min, y_max, ny)
        X, Y = np.meshgrid(x, y)

        try:
            Z = eval(expr_py, {
                "np": np,
                "x": X,
                "y": Y,
                "sin": np.sin,
                "cos": np.cos,
                "exp": np.exp,
                "sqrt": np.sqrt,
                "tan": np.tan,
                "pi": np.pi
            })
        except Exception as e:
            raise ValueError(f"3D 公式運算失敗：{e}\n轉換後: {expr_py}")

        return Plot3DEngine._surface_html_from_grid(X, Y, Z, dark_mode=dark_mode, label=label)

    # --------- 情況 2：由 xyz 檔案構建 3D 曲面 ---------
    @staticmethod
    def make_surface_from_xyz_file(filepath: str,
                                   dark_mode: bool = True,
                                   label: str = None) -> str:
        """
        讀取 3 欄 (x, y, z) 資料檔，重建規則網格並畫 3D 曲面。
        檔案可有 header，也可無：

        x y z
        0 0 1.0
        0 1 1.2
        ...

        或：

        0 0 1.0
        0 1 1.2
        ...
        """

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"找不到資料檔：{filepath}")

        # 判斷是否有 header
        with open(filepath, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
        tokens = first_line.split()
        has_header = False
        if len(tokens) >= 3:
            try:
                float(tokens[0]); float(tokens[1]); float(tokens[2])
            except:
                has_header = True

        if has_header:
            data = np.loadtxt(filepath, skiprows=1)
        else:
            data = np.loadtxt(filepath)

        if data.ndim == 1 or data.shape[1] < 3:
            raise ValueError("3D 資料檔需至少三欄 (x, y, z)。")

        xs = data[:, 0]
        ys = data[:, 1]
        zs = data[:, 2]

        x_unique = np.unique(xs)
        y_unique = np.unique(ys)
        nx = len(x_unique)
        ny = len(y_unique)

        if nx * ny != len(xs):
            raise ValueError(
                f"資料點數 {len(xs)} 無法重組為規則網格 nx*ny = {nx}*{ny}。"
            )

        # 建立網格索引：假設資料是任意順序，我們按 (y, x) 排序後 reshape
        # 先依 y, 再依 x 排序
        order = np.lexsort((xs, ys))
        xs_sorted = xs[order]
        ys_sorted = ys[order]
        zs_sorted = zs[order]

        X = xs_sorted.reshape(ny, nx)
        Y = ys_sorted.reshape(ny, nx)
        Z = zs_sorted.reshape(ny, nx)

        if label is None:
            label = os.path.basename(filepath)

        return Plot3DEngine._surface_html_from_grid(X, Y, Z, dark_mode=dark_mode, label=label)

    @staticmethod
    def make_surface_from_latex(latex_str: str,
                                dark_mode=True,
                                label=None):
        """
        將 LaTeX 的 z = f(x,y) 解析為 3D 曲面。
        支援：
            plot3d$$ z = \sin(x)\cos(y) $$
            plot3d$$ \sin(x)\cos(y) $$
        """
        # 移除 $$ 與前後空白
        latex_str = latex_str.strip().strip('$')

        # 取等號右側
        if '=' in latex_str:
            expr_part = latex_str.split('=', 1)[1].strip()
        else:
            expr_part = latex_str

        # 轉成 Python 可執行語法
        from latex.core_latex import LatexPlotEngine
        expr_py = LatexPlotEngine._latex_to_python(expr_part)

        # 直接用函數版做 meshgrid
        return Plot3DEngine.make_surface_from_func(
            expr_py,
            x_min=-5, x_max=5,
            y_min=-5, y_max=5,
            dark_mode=dark_mode,
            label=label or "3D Surface"
        )

    @staticmethod
    def make_surface_div(expr_py: str,
                         x_min: float = -5, x_max: float = 5,
                         y_min: float = -5, y_max: float = 5,
                         dark_mode: bool = True,
                         label: str = None) -> str:
        """
        通用 3D 曲面 API：
        - expr_py 為 Python 可 eval 的 numpy 表達式（例如：np.sin(x)*np.cos(y)）
        - 可自訂 x/y 範圍
        - 回傳 Plotly 3D HTML
        """
        nx, ny = 40, 40
        x = np.linspace(x_min, x_max, nx)
        y = np.linspace(y_min, y_max, ny)
        X, Y = np.meshgrid(x, y)

        try:
            Z = eval(expr_py, {
                "np": np,
                "x": X,
                "y": Y,
                "sin": np.sin,
                "cos": np.cos,
                "exp": np.exp,
                "sqrt": np.sqrt,
                "tan": np.tan,
                "pi": np.pi
            })
        except Exception as e:
            raise ValueError(f"3D 公式運算失敗：{e}\n轉換後: {expr_py}")

        return Plot3DEngine._surface_html_from_grid(
            X, Y, Z,
            dark_mode=dark_mode,
            label=label
        )
