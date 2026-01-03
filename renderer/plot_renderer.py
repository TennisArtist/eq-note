# renderer/plot_renderer.py

from typing import Tuple, Union

from plot.core_plot import PlotEngine
from plot.core_plot3d import Plot3DEngine
from plot.core_plot_data import PlotDataEngine
from plot.core_plot_func import PlotFunc2DEngine

from document.element import PlotElement


class PlotRenderer:
    """
    PlotRenderer：將 PlotElement → HTML 片段。
    新版 Parser 完全相容。
    """

    def __init__(self, dark_mode: bool = True):
        self.dark_mode = dark_mode

    # =========================================================
    # 主入口
    # =========================================================
    def render_plot_element(self, elem: PlotElement) -> str:
        kind = elem.kind
        code = elem.code

        try:
            if kind == "2d_data":
                return self._render_2d_data(code)
            elif kind == "3d_data":
                return self._render_3d_data(code)
            elif kind == "2d_latex":
                return self._render_2d_latex(code)
            elif kind == "3d_latex":
                return self._render_3d_latex(code)
            elif kind == "2d_py":
                return self._render_2d_py(code)
            elif kind == "3d_py":
                return self._render_3d_py(code)
            else:
                return self._error_html(f"未知的 plot kind: {kind}")
        except Exception as e:
            return self._error_html(f"Plot 錯誤：{e}")

    # =========================================================
    # 各類 plot handler
    # =========================================================

    # ---------- 1) XY data file ----------
    def _render_2d_data(self, code: Union[str, Tuple]) -> str:
        filepath = code[0] if isinstance(code, tuple) else code
        div_html = PlotDataEngine.make_xy_plot(filepath, dark_mode=self.dark_mode)
        return div_html

    # ---------- 2) XYZ file ----------
    def _render_3d_data(self, code: Union[str, Tuple]) -> str:
        filepath = code[0] if isinstance(code, tuple) else code
        div_html = Plot3DEngine.make_surface_from_xyz_file(
            filepath,
            dark_mode=self.dark_mode
        )
        return div_html

    # ---------- 3) plot$$ y = ... $$ ----------
    def _render_2d_latex(self, code: str) -> str:
        body = code.strip()
        div_html = PlotFunc2DEngine.make_from_latex(body, dark_mode=self.dark_mode)
        return div_html

    # ---------- 4) plot3d$$ z = ... $$ ----------
    def _render_3d_latex(self, code: str) -> str:
        body = code.strip()
        div_html = Plot3DEngine.make_surface_from_latex(
            body,
            dark_mode=self.dark_mode
        )
        return div_html

    # ---------- 5) 2D python expr ----------
    def _render_2d_py(self, code: Tuple) -> str:
        if not isinstance(code, tuple) or len(code) != 3:
            return self._error_html(f"2d_py 參數錯誤：{code}")

        expr, x_min_str, x_max_str = code
        x_min = float(x_min_str)
        x_max = float(x_max_str)

        filename = PlotEngine.plot(expr, x_min, x_max, dark_mode=self.dark_mode)
        rel_path = filename.replace("\\", "/")

        return f'<img src="{rel_path}" width="400">'

    # ---------- 6) 3D python expr ----------
    def _render_3d_py(self, code: Tuple) -> str:
        if not isinstance(code, tuple) or len(code) != 5:
            return self._error_html(f"3d_py 參數錯誤：{code}")

        expr, x_min_str, x_max_str, y_min_str, y_max_str = code
        x_min = float(x_min_str)
        x_max = float(x_max_str)
        y_min = float(y_min_str)
        y_max = float(y_max_str)

        # LaTeX 轉 Python
        from latex.core_latex import LatexPlotEngine
        expr_py = LatexPlotEngine._latex_to_python(expr)

        # 使用通用 3D API
        return Plot3DEngine.make_surface_div(
            expr_py,
            x_min, x_max,
            y_min, y_max,
            dark_mode=self.dark_mode,
            label=expr
        )

    # =========================================================
    def _error_html(self, msg: str) -> str:
        return f'<pre style="color:red;">{msg}</pre>'
