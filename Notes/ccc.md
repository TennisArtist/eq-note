# 從變分法推導運動方程（Euler–Lagrange 方程）

## 一、作用量（Action）

在經典力學中，系統的運動可由 **最小作用量原理**（Principle of Least Action）決定。  
定義作用量為：
$$
S[q(t)] = \int_{t_1}^{t_2} L(q, \dot{q}, t)\, dt
$$

其中：

- $L(q, \dot{q}, t)$ 為 **拉格朗日量**（Lagrangian）

- $q(t)$ 為廣義座標

- $\dot{q}(t) = \frac{dq}{dt}$

---

## 二、取變分

假設 \( q(t) \) 有微小變化：
$$
q(t) \to q(t) + \delta q(t)
$$
則速度變為：
$$
\dot{q}(t) \to \dot{q}(t) + \delta \dot{q}(t)
$$

因此作用量的變化為：
$$
\delta S = \int_{t_1}^{t_2} 
\left(
\frac{\partial L}{\partial q} \delta q + 
\frac{\partial L}{\partial \dot{q}} \delta \dot{q}
\right) dt
$$

---

## 三、分部積分（Integration by Parts）

第二項可用分部積分轉換：
$$
\int_{t_1}^{t_2} 
\frac{\partial L}{\partial \dot{q}} \delta \dot{q} dt=
\left[ 
\frac{\partial L}{\partial \dot{q}} \delta q
\right]_{t_1}^{t_2}
-
\int_{t_1}^{t_2} 
\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{q}}\right) 
\delta q\, dt
$$

由於端點變分固定：
$$
\delta q(t_1) = \delta q(t_2) = 0
$$
故邊界項消失。

---

## 四、合併後得到：

$$
\delta S = 
\int_{t_1}^{t_2}
\left[
\frac{\partial L}{\partial q}
-
\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{q}}\right)
\right]
\delta q\, dt
$$

---

## 五、最小作用量原理

若系統的實際路徑使 \( S \) 取極值，則對任意微小變化 \( \delta q \) 都必須有：
$$
\delta S = 0
$$
因此可得：

$$
\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{q}}\right)
-
\frac{\partial L}{\partial q}
= 0
$$

---

## 六、這即是 **Euler–Lagrange 方程**

$$
\boxed{
\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{q}}\right)=
\frac{\partial L}{\partial q}
}
$$

---

## 七、應用範例：單質點運動

若：
$$
L = \frac{1}{2}m\dot{q}^2 - V(q)
$$
則：
$$
\frac{\partial L}{\partial q} = -\frac{dV}{dq} = -F
$$
$$
\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{q}}\right)
= \frac{d}{dt}(m\dot{q}) = m\ddot{q}
$$

代入：
$$
m\ddot{q} = F
$$

這就是 **牛頓第二運動定律**。
