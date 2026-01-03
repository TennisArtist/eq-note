import os, re
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class PlotEngine:
    """處理數學函數繪圖，可同圖畫多條曲線，支援主題顏色"""

    @staticmethod
    def plot(expr: str, x_min=-10, x_max=10, color=None, dark_mode=True):
        x = np.linspace(x_min, x_max, 500)
        expr_list = [e.strip() for e in re.split(r'[;,]', expr) if e.strip()]

        os.makedirs("plots", exist_ok=True)
        filename = f"plots/plot_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"

        # 🎨 根據主題設定顏色
        bg = "black" if dark_mode else "white"
        fg = "white" if dark_mode else "black"

        plt.figure(facecolor=bg)
        colors = ["cyan", "orange", "lime", "magenta", "red", "blue"]
        for i, e in enumerate(expr_list):
            try:
                y = eval(e, {"np": np, "x": x, "sin": np.sin, "cos": np.cos,
                             "exp": np.exp, "sqrt": np.sqrt, "tan": np.tan})
                c = color or colors[i % len(colors)]
                plt.plot(x, y, color=c, linewidth=2, label=e)
            except Exception as err:
                print(f"⚠️ 無法繪製: {e} → {err}")

        plt.grid(True, color="gray", alpha=0.3)
        plt.legend(facecolor=bg, edgecolor="gray", labelcolor=fg)
        plt.title(expr, color=fg)
        plt.xlabel("x", color=fg)
        plt.ylabel("y", color=fg)
        plt.gca().tick_params(colors=fg)
        plt.savefig(filename, dpi=150, bbox_inches="tight", facecolor=bg)
        plt.close()

        return filename
