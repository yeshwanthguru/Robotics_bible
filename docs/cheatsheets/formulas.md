---
title: Formula Cheat Sheet
---

# One-Page Formulas (with plain-English meanings)

:::tip[How to use this page]
Each row gives the formula **and what it says in words**. In an interview, say the words first, then write the formula.
:::

## Math and ML

| Formula | In words |
|---|---|
| $p(a\mid b)=\dfrac{p(b\mid a)\,p(a)}{p(b)}$ | **Bayes:** update a belief with new evidence |
| $x\leftarrow x-\eta\nabla f$ | **Gradient descent:** step downhill; η is the step size |
| $x^{*}=(A^\top A)^{-1}A^\top b$ | **Least squares:** the answer that fits all noisy equations best |
| $\partial L/\partial z = p-y$ | **Softmax + cross-entropy gradient:** prediction minus truth |
| $\mathrm{softmax}(QK^\top/\sqrt d)\,V$ | **Attention:** compare queries with keys, blend the values accordingly |
| $\text{params/layer}\approx 12d^2$, FLOPs $\approx 6ND$ | **Transformer size / training cost rules of thumb** |
| $\text{Error}=\text{Bias}^2+\text{Var}+\text{Noise}$ | **Why models fail:** too simple, too jumpy, or noisy data |
| $\text{Precision}=\frac{TP}{TP+FP}$, $\text{Recall}=\frac{TP}{TP+FN}$ | **Of what I flagged, how much was real? Of what was real, how much did I flag?** |

## Reinforcement learning

| Formula | In words |
|---|---|
| $G_t=\sum_k\gamma^k r_{t+k}$ | **Return:** total future reward, sooner counts more |
| $Q^{*}(s,a)=\mathbb E[r+\gamma\max_{a'}Q^{*}(s',a')]$ | **Bellman optimality:** value = reward now + best value next |
| $\nabla J=\mathbb E[\nabla\log\pi\cdot A]$ | **Policy gradient:** make better-than-average actions more likely |
| $\min\big(rA,\ \mathrm{clip}(r,1\pm\epsilon)A\big)$ | **PPO:** improve, but don't change behaviour too much per update |
| $\hat A_t=\sum(\gamma\lambda)^l\delta_{t+l}$ | **GAE:** blend short- and long-term advantage estimates |
| $\delta=r+\gamma V(s')-V(s)$ | **TD error:** "reality minus expectation" |
| SAC: maximise $\sum r+\alpha H(\pi)$ | **Reward plus a bonus for staying random** (better exploration) |

## Quantum

| Formula | In words |
|---|---|
| $\lvert\psi\rangle=\alpha\lvert0\rangle+\beta\lvert1\rangle$ | **Qubit:** two amplitudes; squares are the odds of 0 and 1 |
| H gate: 0 → equal blend | **Hadamard:** make it 50/50 |
| CNOT after H on two qubits | **Bell pair:** two qubits that always agree |
| Grover rounds $\approx\frac\pi4\sqrt{N/M}$ | **Search speed-up:** square-root instead of linear |
| $\partial f=\frac12[f(\theta+\frac\pi2)-f(\theta-\frac\pi2)]$ | **Parameter-shift:** exact gradient from two circuit runs |
| $E(\theta)\ge E_0$ | **VQE:** any trial state's energy is an upper bound of the true minimum |

## Kinematics and dynamics

| Formula | In words |
|---|---|
| $T=\begin{pmatrix}R&p\\0&1\end{pmatrix}$ | **Pose as one matrix:** rotate, then shift |
| $\dot R=[\omega]_\times R$ | **Rotation changes** according to angular velocity |
| $\dot x=J\dot q$ | **Jacobian:** joint speeds → hand speed |
| $\tau=J^\top F$ | **Hand force → joint torques** |
| $J^\top(JJ^\top+\lambda^2I)^{-1}$ | **Damped inverse:** safe near singularities |
| $M\ddot q+C\dot q+g=\tau$ | **Robot physics:** inertia + coupling + gravity = motor torque |
| $\tau=M(\ddot q_d+K_d\dot e+K_pe)+C\dot q+g$ | **Computed torque:** cancel the physics, then simple PD |
| $\ddot x=\frac{g}{z}(x-p_{zmp})$ | **Walking pendulum:** ahead of your support point → falling forward |
| $v=\frac r2(\omega_R+\omega_L),\ \omega=\frac rL(\omega_R-\omega_L)$ | **Diff-drive:** speed = average, turn = difference |

## Estimation and vision

| Formula | In words |
|---|---|
| $K=P^-H^\top(HP^-H^\top+R)^{-1}$ | **Kalman gain:** how much to trust the sensor |
| $x=x^-+K(z-Hx^-)$ | **Update:** prediction + gain × surprise |
| $u=f_xX/Z+c_x$ | **Pinhole camera:** pixel = focal length × (X/Z) + centre |
| $Z=fB/d$ | **Stereo depth:** big disparity = near |
| $x'^\top Fx=0$ | **Epipolar line:** a point in one image lies on a line in the other |
| $(J^\top J)\delta=-J^\top r$ | **Gauss–Newton:** solve a least-squares problem step by step |
| $l=\log\frac{p}{1-p}$ | **Log-odds:** map updates become simple addition |

## Control

| Formula | In words |
|---|---|
| $u=K_pe+K_i\!\int e+K_d\dot e$ | **PID:** now + accumulated + trend of the error |
| $u=-Kx,\ K=R^{-1}B^\top P$ | **LQR:** optimal feedback; Q = what errors cost, R = what effort costs |
| Stable if poles have negative real part (continuous) or $\lvert z\rvert<1$ (discrete) | **Stability check** |
| $M_d\ddot e+D_d\dot e+K_de=F_{ext}$ | **Impedance:** the robot behaves like a spring-damper |
| $V>0,\ \dot V<0$ | **Lyapunov:** an "energy" that always decreases = stable |

## Planning and simulation

| Formula | In words |
|---|---|
| A\*: $f=g+h$ | **Cost so far + estimated cost to go** |
| RRT\* radius $\propto(\log n/n)^{1/d}$ | **How wide to look when rewiring** |
| UCB: $Q+c\sqrt{\ln N/n}$ | **Explore what you've tried rarely** |
| policy dt = sim dt × decimation | **Control rate bookkeeping** (e.g. 0.005 s × 4 = 50 Hz) |
| $\tau=K_p(q^{*}-q)-K_d\dot q$ | **PD joint controller:** spring to target + damper |
| $\lVert f_t\rVert\le\mu f_n$ | **Friction cone:** sideways force ≤ friction × normal force |
