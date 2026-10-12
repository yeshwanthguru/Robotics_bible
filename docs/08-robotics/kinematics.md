---
title: Spatial Math & Kinematics
---

# Spatial Math & Kinematics

## Rotations and poses
| Representation | Size | Pros | Cons |
|---|---|---|---|
| Rotation matrix $R\in SO(3)$ | 9 | composition = multiply | redundant, drift off manifold |
| Euler angles (RPY) | 3 | intuitive | **gimbal lock**, order ambiguity |
| Axis-angle / rotation vector | 3 | minimal; Lie-algebra $\mathfrak{so}(3)$ | singular at π |
| **Quaternion** $q=(w,x,y,z)$, $\|q\|=1$ | 4 | no gimbal lock, cheap slerp | double cover ($q\equiv-q$) |
| 6D continuous (Zhou et al.) | 6 | best for NN regression | needs Gram–Schmidt |

- **Rodrigues:** $R=I+\sin\theta[\hat k]_\times+(1-\cos\theta)[\hat k]_\times^2$.
- **Homogeneous transform** $T=\begin{pmatrix}R&p\\0&1\end{pmatrix}\in SE(3)$; inverse $\begin{pmatrix}R^\top&-R^\top p\\0&1\end{pmatrix}$.
- **Lie groups:** exp/log maps between $\mathfrak{se}(3)$ and $SE(3)$; twist $\xi=(v,\omega)$; adjoint; used in GTSAM/Sophus/manif for optimization on manifolds.
- Angular velocity: $\dot R=[\omega]_\times R$. Quaternion kinematics $\dot q=\tfrac12 q\otimes(0,\omega)$.
- **Frames:** world, base, link, tool(TCP), camera, sensor. Chain: ${}^{0}T_n={}^0T_1{}^1T_2\cdots$. ROS TF stores these in a tree.
- **Hand–eye calibration** $AX=XB$.

## Forward kinematics (FK)
Joint vector $q\mapsto$ end-effector pose.
- **Denavit–Hartenberg (DH):** 4 params per joint $(a,\alpha,d,\theta)$; $T_i=Rot_z(\theta)Trans_z(d)Trans_x(a)Rot_x(\alpha)$ (standard) — modified DH puts $a,\alpha$ first.
- **Product of Exponentials (PoE):** $T(q)=e^{[S_1]q_1}\cdots e^{[S_n]q_n}M$ — frame-free, preferred in modern robotics (Lynch & Park).
- **URDF/SDF** describe the kinematic tree (links, joints, inertia, visual/collision).

## Jacobian
$\dot x=J(q)\dot q$, $J\in\mathbb R^{6\times n}$. Geometric Jacobian columns: revolute $[z_{i-1}\times(p_e-p_{i-1});\ z_{i-1}]$, prismatic $[z_{i-1};\ 0]$.
- **Statics:** $\tau=J^\top F$.
- **Singularities:** $\det(JJ^\top)=0$ → lost DOF, infinite joint velocities. Manipulability $w=\sqrt{\det(JJ^\top)}$; ellipsoid axes = singular values.
- Redundancy $n>6$: null-space motion $\dot q=J^+\dot x+(I-J^+J)\dot q_0$ (joint-limit avoidance, secondary tasks).

## Inverse kinematics (IK)
| Method | Notes |
|---|---|
| Analytic / closed form | 6R with spherical wrist (Pieper), IKFast; fast, all solutions |
| Jacobian pseudo-inverse | $\Delta q=J^+\Delta x$ |
| **Damped least squares (LM)** | $\Delta q=J^\top(JJ^\top+\lambda^2I)^{-1}\Delta x$ — singularity robust |
| Jacobian transpose | cheap, slow |
| CCD / FABRIK | geometric, for chains/animation |
| Optimization-based | QP w/ limits (TRAC-IK, Pink, CuRobo, IPOPT) |
| Learning-based | IKFlow, NN (multimodal solutions) |

Multiple solutions (elbow up/down, wrist flip); check joint limits & self-collision.

## Velocity / differential drive / mobile kinematics
- Differential drive: $\dot x=v\cos\theta,\ \dot y=v\sin\theta,\ \dot\theta=\omega$; $v=\frac{r(\omega_R+\omega_L)}{2}$, $\omega=\frac{r(\omega_R-\omega_L)}{L}$. Nonholonomic (no sideways).
- Ackermann (car): bicycle model $\dot\theta=\frac vL\tan\delta$.
- Omni / mecanum / swerve: holonomic.
- Unicycle & bicycle used in MPC / Stanley / pure pursuit.

## Interview Q&A

**Why quaternions over Euler?** No gimbal lock, smooth interpolation, compact, numerically stable (renormalize).

**What is a singularity and how handle?** Jacobian rank loss; use DLS, avoid via planning, null-space, switch configurations.

**Forward vs inverse kinematics complexity?** FK is unique and cheap; IK is multi-solution/non-existent, solved numerically.

**Why $\tau=J^\top F$?** Principle of virtual work: $\tau^\top\delta q=F^\top\delta x=F^\top J\delta q$.

**6D rotation representation why?** 3D/4D representations have discontinuities when regressed by NNs; 5D/6D are continuous.
