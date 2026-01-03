好，我把你那套「反覆換慣性系」的推論，升級成 Minkowski 幾何：不再把「等加速度」當成 (d^2x/dt^2=\text{const})（這是座標依賴的），而是把它改寫成幾何不變量：世界線在 Minkowski 時空中的「曲率」固定。

1) 先把舞台換成 Minkowski 幾何
在 1+1 維（只看 (x) 方向）：
事件：(X^\mu=(ct,,x))
度規（取號誌 (+,-)）：
$$
ds^2 = c^2 dt^2 - dx^2
$$
定義固有時（proper time）：
$$
d\tau = \frac{1}{c}\sqrt{ds^2}=\sqrt{dt^2-\frac{dx^2}{c^2}}
$$
關鍵： (\tau) 是所有慣性觀察者都同意的（洛倫茲不變），所以用它來「參數化運動」才是幾何版本的做法。

2) 把「速度」換成四速度，把「加速度」換成四加速度
四速度：
$$
U^\mu=\frac{dX^\mu}{d\tau}=\left(c\frac{dt}{d\tau},,\frac{dx}{d\tau}\right)
$$
它滿足一個不變關係（直接由 (ds^2=c^2d\tau^2) 得到）：
$$
U^\mu U_\mu = c^2
$$
四加速度：
$$
A^\mu=\frac{dU^\mu}{d\tau}
$$
由 (U^\mu U_\mu=c^2) 對 (\tau) 微分得：
$$
U^\mu A_\mu = 0
$$
也就是「四加速度永遠與四速度 Minkowski 正交」。

3) Minkowski 版「等加速度」：固定的是 固有加速度（proper acceleration）
你在牛頓版「等加速度」其實在說：某個量的大小固定、可疊加。
在 Minkowski 幾何裡，唯一合理的「固定大小」是四加速度的模長（不變量）：
$$
\alpha \equiv \sqrt{-A^\mu A_\mu}=\text{常數}
$$
（負號是因為 (A^\mu) 是類空向量；(\alpha) 是實數。）
這句話就是：世界線的 Minkowski 曲率固定。這才叫「相對論真正的等加速度」。

4) 直接解出世界線：結果必然是「雙曲線」
引入快度（rapidity）(\eta)，用它把洛倫茲 boost 的群參數顯性化。定義：
$$
\beta\equiv \frac{v}{c}=\tanh\eta,\qquad \gamma=\cosh\eta,\qquad \gamma\beta=\sinh\eta
$$
那麼四速度可寫成非常乾淨的形式：
$$
U^\mu = (c\cosh\eta,; c\sinh\eta)
$$
你要的「等加速度」是 (\alpha) 常數。事實上可以驗證：
$$
\alpha = c,\left|\frac{d\eta}{d\tau}\right|
$$
所以「固有加速度常數」等價於：
$$
\frac{d\eta}{d\tau}=\frac{\alpha}{c}
\quad\Rightarrow\quad
\eta(\tau)=\frac{\alpha}{c}\tau ;(+\text{常數})
$$
取初始條件 (\tau=0) 時 (v=0\Rightarrow \eta=0)，得：
$$
\eta(\tau)=\frac{\alpha}{c}\tau
$$
把 (U^\mu=dX^\mu/d\tau) 積分：
時間分量：
$$
\frac{d(ct)}{d\tau}=c\cosh!\left(\frac{\alpha\tau}{c}\right)
\Rightarrow
ct(\tau)=\frac{c^2}{\alpha}\sinh!\left(\frac{\alpha\tau}{c}\right)
$$
空間分量：
$$
\frac{dx}{d\tau}=c\sinh!\left(\frac{\alpha\tau}{c}\right)
\Rightarrow
x(\tau)=\frac{c^2}{\alpha}\left[\cosh!\left(\frac{\alpha\tau}{c}\right)-1\right]
$$
消去 (\tau)（用 (\cosh^2-\sinh^2=1)）得到世界線方程：
$$
\left(x+\frac{c^2}{\alpha}\right)^2-(ct)^2=\left(\frac{c^2}{\alpha}\right)^2
$$
這就是你要的幾何結論：
等固有加速度的運動，在 Minkowski 圖上是一條雙曲線。

5) 把它翻回你熟悉的 (v(t))：你會看到「永遠追不到 (c)」
由 $\eta(\tau)=\alpha\tau/c$：
速度（用 $\beta=\tanh\eta$）：
$$
v(\tau)=c\tanh!\left(\frac{\alpha\tau}{c}\right)
$$
同時 (t(\tau)=\frac{c}{\alpha}\sinh(\alpha\tau/c))，消去 (\tau) 得：
$$
v(t)=\frac{\alpha t}{\sqrt{1+\left(\frac{\alpha t}{c}\right)^2}}
$$
所以 (t\to\infty) 時 (v\to c)，但永遠不超過。

6) 回到你的原始推法：你其實早就在用「快度加法」了
你原本反覆換慣性系，核心是「同樣的 boost 一直疊加」。
在 Minkowski 幾何裡，「boost 的量」就是快度 (\eta)，它是李群參數，可加：
$$
\eta_{\text{total}}=\sum \Delta\eta
$$
而「等固有加速度」就是說：
$$
\Delta\eta \propto \Delta\tau
\quad\Leftrightarrow\quad
\frac{d\eta}{d\tau}=\frac{\alpha}{c}
$$
你的推論升級後變成一句話：
把「每一步看到同樣的現象」從 $\Delta v$ 改成 $\Delta\eta$（或等價地用 (\tau) 參數化），等加速度的幾何形狀就從拋物線變成雙曲線。

如果你願意再往前推一小步（仍然是幾何、不是背公式）：我可以把「固定力」分成三種不同的“固定”（固定三力、固定四力、固定固有加速度），並指出它們在 Minkowski 幾何下對應到不同的世界線與不同的可測量量——這裡很多教材其實講得不乾淨。