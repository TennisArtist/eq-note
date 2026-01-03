好的，我會用正常的 LaTeX 書寫方式，完整展示「從變分法推導到歐拉–拉格朗日方程（運動方程）」的過程。

$$
S[q] = \int_{t_1}^{t_2} L(q, \dot{q}, t),dt
$$
令作用量 ( S[q] ) 對軌跡 ( q(t) ) 取變分，考慮無限小擾動
$$
q(t) \to q(t) + \delta q(t)
$$
對應的變化為
$$
\dot{q}(t) \to \dot{q}(t) + \delta \dot{q}(t)
$$
將其代入作用量：
$$
\delta S = S[q + \delta q] - S[q]
= \int_{t_1}^{t_2}
\left[
L(q + \delta q,, \dot{q} + \delta \dot{q},, t)
L(q, \dot{q}, t)
\right] dt
$$
對 ( L ) 做一階泰勒展開（僅保留線性項）：
$$
\delta S = \int_{t_1}^{t_2}
\left(
\frac{\partial L}{\partial q}, \delta q
\frac{\partial L}{\partial \dot{q}}, \delta \dot{q}
\right) dt
$$
注意到 ( \delta \dot{q} = \frac{d}{dt}(\delta q) )，
因此：
$$
\delta S =
\int_{t_1}^{t_2}
\left(
\frac{\partial L}{\partial q}, \delta q
\frac{\partial L}{\partial \dot{q}}, \frac{d}{dt}(\delta q)
\right) dt
$$
將第二項做分部積分：
$$
\int_{t_1}^{t_2}
\frac{\partial L}{\partial \dot{q}}, \frac{d}{dt}(\delta q),dt
\left[ \frac{\partial L}{\partial \dot{q}}, \delta q \right]_{t_1}^{t_2}
\int_{t_1}^{t_2}
\frac{d}{dt}!\left(\frac{\partial L}{\partial \dot{q}}\right)! \delta q,dt
$$
因為變分在端點固定 (( \delta q(t_1)=\delta q(t_2)=0 ))，邊界項消失。
因此：
$$
\delta S =
\int_{t_1}^{t_2}
\left[
\frac{\partial L}{\partial q}
\frac{d}{dt}!\left(\frac{\partial L}{\partial \dot{q}}\right)
\right]!
\delta q, dt
$$
對任意的 ( \delta q(t) )，若要求 ( \delta S = 0 )，則括號內必須為零：
$$
\boxed{
\frac{d}{dt}!\left(\frac{\partial L}{\partial \dot{q}}\right)
\frac{\partial L}{\partial q} = 0
}
$$
這就是 歐拉–拉格朗日方程（Euler–Lagrange equation），
亦即從變分原理導出的運動方程。

如果要更直覺地看成牛頓力學的等價形式，
取 ( L = T - V = \frac{1}{2}m\dot{q}^2 - V(q) )，
則
$$
\frac{d}{dt}(m\dot{q}) + \frac{dV}{dq} = 0
\quad \Rightarrow \quad
m\ddot{q} = -\frac{dV}{dq}
$$
這正是 牛頓第二運動定律。

~plot$$ y= x^2$$
<img src="plots/latex_plot_20251108_003128_135007.png" width="400">
