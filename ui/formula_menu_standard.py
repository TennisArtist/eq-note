# formula_menu_standard.py
# ---------------------------------------------------------------
# 適用：標準 LaTeX / MathJax + physics 套件環境
# 所有指令均為官方 LaTeX 語法，不含自定別名。
# ---------------------------------------------------------------

from PyQt5.QtWidgets import QMenu
from functools import partial


def create_formula_menu(parent, insert_callback):
    """建立符合標準 LaTeX / physics 套件的公式符號選單"""
    menu = QMenu(parent)

    # === 基本運算 ===
    basic = QMenu("基本運算", menu)
    basic.addAction("乘號 (\\times)", partial(insert_callback, "$\\times$"))
    basic.addAction("除號符號 (÷)", partial(insert_callback, "÷"))
    basic.addAction("分式 (\\frac{a}{b})", partial(insert_callback, "$\\frac{a}{b}$"))
    basic.addAction("平方 (x^2)", partial(insert_callback, "$x^2$"))
    basic.addAction("平方根 (\\sqrt{x})", partial(insert_callback, "$\\sqrt{x}$"))
    basic.addAction("絕對值 (|x|)", partial(insert_callback, "$\\abs{x}$"))
    basic.addAction("範數 (‖v‖)", partial(insert_callback, "$\\norm{v}$"))
    basic.addAction("無限大 (\\infty)", partial(insert_callback, "$\\infty$"))
    basic.addAction("近似等於 (\\approx)", partial(insert_callback, "$\\approx$"))
    basic.addAction("不等於 (\\neq)", partial(insert_callback, "$\\neq$"))
    menu.addMenu(basic)

    # === 向量與矩陣 ===
    vector = QMenu("向量與矩陣", menu)
    vector.addAction("向量箭頭 (\\vec{v})", partial(insert_callback, "$\\vec{v}$"))
    vector.addAction("內積 (\\cdot)", partial(insert_callback, "$\\cdot$"))
    vector.addAction("外積 (\\times)", partial(insert_callback, "$\\times$"))
    vector.addAction("單位向量 (\\hat{i})", partial(insert_callback, "$\\hat{i}$"))
    vector.addAction("矩陣元素 (A_{ij})", partial(insert_callback, "$A_{ij}$"))
    vector.addAction("行列式 (\\det A)", partial(insert_callback, "$\\det A$"))
    vector.addAction("轉置 (A^T)", partial(insert_callback, "$A^T$"))
    vector.addAction("逆矩陣 (A^{-1})", partial(insert_callback, "$A^{-1}$"))
    menu.addMenu(vector)

    # === 微積分運算 ===
    calculus = QMenu("微積分運算", menu)
    calculus.addAction("導數 (dv)", partial(insert_callback, "$\\dv{y}{x}$"))
    calculus.addAction("偏導 (pdv)", partial(insert_callback, "$\\pdv{f}{x}$"))
    calculus.addAction("二階導數 (dv[2])", partial(insert_callback, "$\\dv[2]{y}{x}$"))
    calculus.addAction("二階偏導 (pdv[2])", partial(insert_callback, "$\\pdv[2]{f}{x}$"))
    calculus.addAction("積分 (\\int)", partial(insert_callback, "$\\int f(x)\\,dx$"))
    calculus.addAction("重積分 (\\iint)", partial(insert_callback, "$\\iint f(x,y)\\,dx\\,dy$"))
    calculus.addAction("三重積分 (\\iiint)", partial(insert_callback, "$\\iiint f(x,y,z)\\,dV$"))
    calculus.addAction("梯度 (\\grad f)", partial(insert_callback, "$\\grad f$"))
    calculus.addAction("散度 (\\div \\vec{F})", partial(insert_callback, "$\\div \\vec{F}$"))
    calculus.addAction("旋度 (\\curl \\vec{A})", partial(insert_callback, "$\\curl \\vec{A}$"))
    calculus.addAction("Laplace 算子 (\\nabla^2 f)", partial(insert_callback, "$\\nabla^2 f$"))
    menu.addMenu(calculus)

    # === 線代與算子 ===
    linalg = QMenu("線代與算子", menu)
    linalg.addAction("Trace (Tr)", partial(insert_callback, "$\\Tr(A)$"))
    linalg.addAction("投影 (\\proj)", partial(insert_callback, "$\\proj_{\\vec{u}}\\vec{v}$"))
    linalg.addAction("外積符號 (\\otimes)", partial(insert_callback, "$\\otimes$"))
    linalg.addAction("內積符號 (\\langle v,w \\rangle)", partial(insert_callback, "$\\langle v,w \\rangle$"))
    menu.addMenu(linalg)

    # === 量子力學 ===
    quantum = QMenu("量子力學", menu)
    quantum.addAction("Ket |ψ⟩", partial(insert_callback, "$\\ket{\\psi}$"))
    quantum.addAction("Bra ⟨φ|", partial(insert_callback, "$\\bra{\\phi}$"))
    # quantum.addAction("內積 ⟨φ|ψ⟩", partial(insert_callback, "$\\braket{\\phi|\\psi}$"))
    quantum.addAction("內積 ⟨φ|ψ⟩", partial(insert_callback, "$ \\langle\\phi | \\psi\\rangle $"))
    quantum.addAction("外積 |ψ⟩⟨φ|", partial(insert_callback, "$\\ket{\\psi}\\bra{\\phi}$"))
    quantum.addAction("升算符 â†", partial(insert_callback, "$\\hat{a}^\\dagger$"))
    quantum.addAction("降算符 â", partial(insert_callback, "$\\hat{a}$"))
    quantum.addAction("對易關係", partial(insert_callback, "$[\\hat{a},\\hat{a}^\\dagger]=1$"))
    quantum.addAction("波函數展開", partial(insert_callback, "$\\ket{\\psi}=\\sum_n c_n\\ket{n}$"))
    menu.addMenu(quantum)

    # === 物理常用 ===
    physics = QMenu("物理常用", menu)
    physics.addAction("電場 (\\vec{E})", partial(insert_callback, "$\\vec{E}$"))
    physics.addAction("磁場 (\\vec{B})", partial(insert_callback, "$\\vec{B}$"))
    physics.addAction("電流密度 (\\vec{J})", partial(insert_callback, "$\\vec{J}$"))
    physics.addAction("電荷密度 (\\rho)", partial(insert_callback, "$\\rho$"))
    physics.addAction("角速度 (\\omega)", partial(insert_callback, "$\\omega$"))
    physics.addAction("位能 (V)", partial(insert_callback, "$V$"))
    physics.addAction("能量 (E)", partial(insert_callback, "$E$"))
    physics.addAction("動量 (\\vec{p})", partial(insert_callback, "$\\vec{p}$"))
    physics.addAction("力 (\\vec{F})", partial(insert_callback, "$\\vec{F}$"))
    menu.addMenu(physics)

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

    return menu
