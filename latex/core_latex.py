# core_latex.py
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


class LatexPlotEngine:
    """進階輕量版：從 LaTeX 公式繪製函數圖形（不依賴 sympy 或 antlr4）"""

    @staticmethod
    def _latex_to_python(expr: str) -> str:
        """
        將 LaTeX 轉成 Python/Numpy 語法（強化版）
        支援：
          - \frac{A}{B}
          - \sin^2(x)
          - 3x → 3*x
          - x y → x*y
          - \cos(x y)
          - 絕對值 |...|
          - 多層嵌套
        """

        # -------- 1) 處理分數 \frac{A}{B} --------
        expr = re.sub(
            r'\\frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}',
            r'(\1)/(\2)',
            expr
        )

        # -------- 2) 先處理函數名稱（保留反斜線）--------
        func_map = {
            r'\\sin': 'np.sin',
            r'\\cos': 'np.cos',
            r'\\tan': 'np.tan',
            r'\\exp': 'np.exp',
            r'\\sqrt': 'np.sqrt',
            r'\\ln': 'np.log',
            r'\\log': 'np.log10',
        }
        for k, v in func_map.items():
            expr = re.sub(k, v, expr)

        # -------- 3) 處理符號 --------
        symbol_map = {
            r'\\pi': 'np.pi',
            r'\\cdot': '*',
            r'\\times': '*',
        }
        for k, v in symbol_map.items():
            expr = re.sub(k, v, expr)

        # -------- 4) 移除 \left, \right 與 spacing --------
        expr = re.sub(r'\\left', '', expr)
        expr = re.sub(r'\\right', '', expr)
        expr = re.sub(r'\\[;,!:]\s*', '', expr)

        # -------- 5) 絕對值 |...| --------
        expr = re.sub(r'\|\s*([^|]+?)\s*\|', r'np.abs(\1)', expr)

        # -------- 6) 運算子 ^ → ** --------
        expr = re.sub(r'\^', '**', expr)

        # -------- 7) 處理函數平方 sin^2(x) --------
        # np.sin**2(x) → (np.sin(x))**2
        expr = re.sub(
            r'(np\.\w+)\s*\*\*\s*(\d+)\s*\(([^()]+)\)',
            r'(\1(\3))**\2',
            expr
        )

        # -------- 8) 統一括號 {} → () --------
        expr = expr.replace('{', '(').replace('}', ')')

        # -------- 9) 隱式乘法（變數/數字相鄰 → *）--------
        # 3x → 3*x
        expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr)

        # x y → x*y
        expr = re.sub(r'([a-zA-Z\)])\s+([a-zA-Z\(])', r'\1*\2', expr)

        # -------- 10) 刪除無用反斜線（不刪除函數）--------
        expr = re.sub(r'\\(?=[^a-zA-Z])', '', expr)

        # -------- 11) 移除多餘空白 --------
        expr = re.sub(r'\s+', '', expr)

        return expr

    @staticmethod
    def plot_from_latex(latex_str: str, x_min=-10, x_max=10, color="orange", dark_mode=True):
        """解析 LaTeX 公式並繪製（支援多函數 + 主題顏色）"""
        import re

        latex_str = latex_str.strip().strip('$')

        # 取等號右側（允許多個式子）
        if '=' in latex_str:
            expr_part = latex_str.split('=')[-1]
        else:
            expr_part = latex_str

        # 處理範圍資訊，如 x∈[-5,5] 或 x in [-5,5]
        range_match = re.search(r'x\s*(?:∈|in)\s*\[([\-]?\d+(?:\.\d+)?),\s*([\-]?\d+(?:\.\d+)?)\]', expr_part)
        if range_match:
            x_min, x_max = map(float, range_match.groups())
            expr_part = re.sub(r'x\s*(?:∈|in)\s*\[[^\]]+\]', '', expr_part)

        expr_part = expr_part.strip().rstrip(',')

        # 將逗號或分號分隔的多函數切開
        expr_list = [e.strip() for e in re.split(r'[;,]', expr_part) if e.strip()]

        # 轉成 Python/Numpy 可執行語法
        expr_py_list = [LatexPlotEngine._latex_to_python(e) for e in expr_list]

        # 繪圖資料
        x = np.linspace(x_min, x_max, 600)
        colors = ["orange", "cyan", "lime", "magenta", "red", "blue"]

        # 🎨 主題設定
        bg = "black" if dark_mode else "white"
        fg = "white" if dark_mode else "black"

        # 繪圖
        plt.figure(facecolor=bg)
        for i, expr_py in enumerate(expr_py_list):
            try:
                y = eval(expr_py, {"np": np, "x": x})
                plt.plot(x, y, color=colors[i % len(colors)], linewidth=2, label=expr_list[i])
            except Exception as e:
                print(f"⚠️ 無法繪製 {expr_list[i]}: {e}")

        plt.grid(True, color="gray", alpha=0.3)
        plt.legend(facecolor=bg, edgecolor="gray", labelcolor=fg)
        plt.title(latex_str, color=fg)
        plt.xlabel("x", color=fg)
        plt.ylabel("y", color=fg)
        plt.gca().tick_params(colors=fg)

        # === 在這裡建立 filename（之前的版本少了這行，導致 NameError）===
        os.makedirs("plots", exist_ok=True)
        filename = f"plots/latex_plot_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"

        # 儲存與關閉
        plt.savefig(filename, dpi=150, bbox_inches="tight", facecolor=bg)
        plt.close()
        return filename
