---
title: Formula Cheat Sheet
---

# One-Page Formulas

## Math / ML
- Bayes $p(a|b)=p(b|a)p(a)/p(b)$ · Gaussian conditioning $\mu_{a|b}=\mu_a+\Sigma_{ab}\Sigma_{bb}^{-1}(b-\mu_b)$
- Softmax CE gradient: $\partial L/\partial z=p-y$
- Adam: $m=\beta_1m+(1-\beta_1)g$, $v=\beta_2v+(1-\beta_2)g^2$, $\theta-=\eta\hat m/(\sqrt{\hat v}+\epsilon)$
- Attention $\mathrm{softmax}(QK^\top/\sqrt{d})V$ · params per transformer layer ≈ $12d^2$ · training FLOPs ≈ $6ND$
- KL(N(μ₁,σ₁²)‖N(μ₂,σ₂²)) = $\log\frac{\sigma_2}{\sigma_1}+\frac{\sigma_1^2+(\mu_1-\mu_2)^2}{2\sigma_2^2}-\tfrac12$

## RL
- $G_t=\sum\gamma^kr_{t+k}$ · $Q^*(s,a)=E[r+\gamma\max Q^*(s',a')]$
- PG: $E[\nabla\log\pi\,A]$ · PPO: $\min(rA,\mathrm{clip}(r,1\pm\epsilon)A)$ · GAE: $\sum(\gamma\lambda)^l\delta_{t+l}$
- SAC: $\max E[\sum r+\alpha H(\pi)]$ · TD error $\delta=r+\gamma V(s')-V(s)$

## Quantum
- $|\psi\rangle=\alpha|0\rangle+\beta|1\rangle$ · $H=\frac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$ · CNOT creates Bell pair
- Grover iterations $\approx\frac\pi4\sqrt{N/M}$ · Parameter-shift $\partial f=\frac12[f(\theta+\pi/2)-f(\theta-\pi/2)]$ · VQE $E(\theta)\ge E_0$

## Kinematics / dynamics
- $T=\begin{pmatrix}R&p\\0&1\end{pmatrix}$, $T^{-1}=\begin{pmatrix}R^\top&-R^\top p\\0&1\end{pmatrix}$ · $\dot R=[\omega]_\times R$
- $\dot x=J\dot q$ · $\tau=J^\top F$ · DLS: $J^\top(JJ^\top+\lambda^2I)^{-1}$
- $M\ddot q+C\dot q+g=\tau$ · computed torque $\tau=M(\ddot q_d+K_d\dot e+K_pe)+C\dot q+g$
- LIPM $\ddot x=\frac{g}{z}(x-p_{zmp})$, $\omega=\sqrt{g/z}$ · diff-drive $v=\frac{r}{2}(\omega_R+\omega_L)$, $\omega=\frac rL(\omega_R-\omega_L)$

## Estimation
- KF: $K=P^-H^\top(HP^-H^\top+R)^{-1}$ · $x=x^-+K(z-Hx^-)$ · $P=(I-KH)P^-$
- Pinhole: $u=f_xX/Z+c_x$ · stereo depth $Z=fB/d$ · Epipolar $x'^\top Fx=0$
- Gauss–Newton $(J^\top J)\delta=-J^\top r$ · LM adds $\lambda I$
- Occupancy log-odds $l=\log\frac{p}{1-p}$

## Control
- PID $u=K_pe+K_i\int e+K_d\dot e$ · LQR $K=R^{-1}B^\top P$ (CARE) · Stability: Re(poles)<0 / |poles|<1
- Impedance $M_d\ddot e+D_d\dot e+K_de=F_{ext}$ · Lyapunov $V>0,\ \dot V<0$

## Planning
- A* $f=g+h$ (h admissible) · RRT* radius $r\propto(\log n/n)^{1/d}$ · UCB $Q+c\sqrt{\ln N/n}$

## Sim
- policy_dt = sim_dt × decimation · PD torque $\tau=K_p(q^*-q)-K_d\dot q$ · friction cone $\|f_t\|\le\mu f_n$
