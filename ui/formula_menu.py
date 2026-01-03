# formula_menu.py
# 插入常用「數學符號與運算子」選單
# -----------------------------------
# 類別：基本運算、向量與矩陣、微積分運算、邏輯與集合、物理常用
# 使用方法：ui_mainwindow.py 只需
#     from formula_menu import create_formula_menu
#     menu = create_formula_menu(self, self.insert_formula_text)
#     menu.exec_(self.btn_insert_formula.mapToGlobal(self.btn_insert_formula.rect().bottomLeft()))

from PyQt5.QtWidgets import QMenu
from functools import partial

def create_formula_menu(parent, insert_callback):
    """建立插入符號的簡易公式選單。"""
    menu = QMenu(parent)

    # === 基本運算 ===
    basic = QMenu("基本運算", menu)
    basic.addAction("乘號 (\\times)", partial(insert_callback, "$\\times$"))
    basic.addAction("除號 (\\div)", partial(insert_callback, "$\\div$"))
    basic.addAction("平方 (x^2)", partial(insert_callback, "$x^2$"))
    basic.addAction("平方根 (\\sqrt{x})", partial(insert_callback, "$\\sqrt{x}$"))
    basic.addAction("絕對值 (|x|)", partial(insert_callback, "$|x|$"))
    basic.addAction("無限大 (\\infty)", partial(insert_callback, "$\\infty$"))
    basic.addAction("近似等於 (\\approx)", partial(insert_callback, "$\\approx$"))
    basic.addAction("不等於 (\\neq)", partial(insert_callback, "$\\neq$"))
    basic.addAction("小於等於 (\\leq)", partial(insert_callback, "$\\leq$"))
    basic.addAction("大於等於 (\\geq)", partial(insert_callback, "$\\geq$"))
    menu.addMenu(basic)

    # === 向量與矩陣 ===
    vector = QMenu("向量與矩陣", menu)
    vector.addAction("向量箭頭 (\\vec{v})", partial(insert_callback, "$\\vec{v}$"))
    vector.addAction("內積 (\\cdot)", partial(insert_callback, "$\\cdot$"))
    vector.addAction("外積 (\\times)", partial(insert_callback, "$\\times$"))
    vector.addAction("單位向量 (\\hat{i})", partial(insert_callback, "$\\hat{i}$"))
    vector.addAction("矩陣符號 (A_{ij})", partial(insert_callback, "$A_{ij}$"))
    vector.addAction("行列式符號 (\\det A)", partial(insert_callback, "$\\det A$"))
    vector.addAction("轉置 (A^T)", partial(insert_callback, "$A^T$"))
    vector.addAction("逆矩陣 (A^{-1})", partial(insert_callback, "$A^{-1}$"))
    menu.addMenu(vector)

    # === 微積分運算 ===
    calculus = QMenu("微積分運算", menu)
    calculus.addAction("導數符號 (\\frac{d}{dx})", partial(insert_callback, "$\\frac{d}{dx}$"))
    calculus.addAction("偏導符號 (\\frac{\\partial}{\\partial x})", partial(insert_callback, "$\\frac{\\partial}{\\partial x}$"))
    calculus.addAction("積分符號 (\\int)", partial(insert_callback, "$\\int$"))
    calculus.addAction("重積分符號 (\\iint)", partial(insert_callback, "$\\iint$"))
    calculus.addAction("三重積分符號 (\\iiint)", partial(insert_callback, "$\\iiint$"))
    calculus.addAction("梯度 (\\nabla f)", partial(insert_callback, "$\\nabla f$"))
    calculus.addAction("散度 (\\nabla\\cdot\\vec{F})", partial(insert_callback, "$\\nabla\\cdot\\vec{F}$"))
    calculus.addAction("旋度 (\\nabla\\times\\vec{F})", partial(insert_callback, "$\\nabla\\times\\vec{F}$"))
    calculus.addAction("Laplace 算子 (\\nabla^2)", partial(insert_callback, "$\\nabla^2$"))
    menu.addMenu(calculus)

    # === 邏輯與集合 ===
    logic = QMenu("邏輯與集合", menu)
    logic.addAction("屬於 (\\in)", partial(insert_callback, "$\\in$"))
    logic.addAction("不屬於 (\\notin)", partial(insert_callback, "$\\notin$"))
    logic.addAction("包含 (\\subseteq)", partial(insert_callback, "$\\subseteq$"))
    logic.addAction("並集 (\\cup)", partial(insert_callback, "$\\cup$"))
    logic.addAction("交集 (\\cap)", partial(insert_callback, "$\\cap$"))
    logic.addAction("對所有 (\\forall)", partial(insert_callback, "$\\forall$"))
    logic.addAction("存在 (\\exists)", partial(insert_callback, "$\\exists$"))
    logic.addAction("邏輯與 (\\land)", partial(insert_callback, "$\\land$"))
    logic.addAction("邏輯或 (\\lor)", partial(insert_callback, "$\\lor$"))
    logic.addAction("推論箭頭 (\\Rightarrow)", partial(insert_callback, "$\\Rightarrow$"))
    menu.addMenu(logic)

    # === 物理常用 ===
    physics = QMenu("物理常用", menu)
    physics.addAction("偏時變 (\\frac{\\partial}{\\partial t})", partial(insert_callback, "$\\frac{\\partial}{\\partial t}$"))
    physics.addAction("電場 (\\vec{E})", partial(insert_callback, "$\\vec{E}$"))
    physics.addAction("磁場 (\\vec{B})", partial(insert_callback, "$\\vec{B}$"))
    physics.addAction("電流密度 (\\vec{J})", partial(insert_callback, "$\\vec{J}$"))
    physics.addAction("電荷密度 (\\rho)", partial(insert_callback, "$\\rho$"))
    physics.addAction("位勢 (\\phi)", partial(insert_callback, "$\\phi$"))
    physics.addAction("角速度 (\\omega)", partial(insert_callback, "$\\omega$"))
    physics.addAction("能量 (E)", partial(insert_callback, "$E$"))
    physics.addAction("動量 (\\vec{p})", partial(insert_callback, "$\\vec{p}$"))
    physics.addAction("力 (\\vec{F})", partial(insert_callback, "$\\vec{F}$"))
    menu.addMenu(physics)

    # === 量子力學 ===
    quantum = QMenu("量子力學", menu)
    quantum.addAction("Ket |ψ⟩", lambda: insert_callback("$$\\ket{\\psi}$$"))
    quantum.addAction("Bra ⟨φ|", lambda: insert_callback("$$\\bra{\\phi}$$"))
    quantum.addAction("內積 ⟨φ|ψ⟩", lambda: insert_callback("$$\\braket{\\phi|\\psi}$$"))
    quantum.addAction("外積 |ψ⟩⟨φ|", lambda: insert_callback("$$\\ket{\\psi}\\bra{\\phi}$$"))
    quantum.addAction("升算符 â††", lambda: insert_callback("$$\\hat{a}^\\dagger$$"))
    quantum.addAction("降算符 â", lambda: insert_callback("$$\\hat{a}$$"))
    quantum.addAction("對易關係", lambda: insert_callback("$$[\\hat{a},\\hat{a}^\\dagger]=1$$"))
    menu.addMenu(quantum)

    return menu
