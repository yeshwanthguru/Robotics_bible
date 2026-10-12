---
title: Control Theory (PID → MPC → Impedance)
---

# Control

## Classical
- **Open vs closed loop**, plant $G(s)$, transfer function, poles/zeros, stability (all poles in LHP), Routh–Hurwitz, Nyquist, Bode (gain/phase margin), root locus.
- Time-domain specs: rise time, overshoot, settling time, steady-state error.
- **PID:** $u=K_pe+K_i\int e+K_d\dot e$. P speeds response; I removes steady-state error (windup → anti-windup clamp/back-calculation); D damps (noise → filtered derivative, derivative-on-measurement). Tuning: Ziegler–Nichols, relay auto-tune, loop-shaping. Cascaded loops (current→velocity→position), feedforward ($\tau_{ff}$ gravity/friction compensation) reduces error massively.
- Discretization (Tustin, ZOH), sample-time effects, delay compensation (Smith predictor), saturation.

## State-space & optimal
$\dot x=Ax+Bu,\ y=Cx$. Controllability $[B\ AB\cdots]$ full rank; observability $[C;CA;\ldots]$ full rank. Pole placement $u=-Kx$.
- **LQR:** $\min\int x^\top Qx+u^\top Ru$; $u=-Kx$, $K=R^{-1}B^\top P$, P solves the Riccati equation (CARE/DARE). Guaranteed margins (SISO); used for balancing, humanoid ZMP preview.
- **LQG** = LQR + Kalman (separation principle); **iLQR/DDP** for nonlinear trajectory optimization.
- **H∞ / μ-synthesis** robust control; **Lyapunov** stability $V>0,\dot V<0$; **LaSalle**; passivity.

## Nonlinear & robot control
| Method | Idea |
|---|---|
| Computed torque / inverse dynamics | cancel dynamics + PD in task/joint space |
| Sliding mode | switching surface, robust to bounded disturbance; chattering |
| Adaptive control (Slotine–Li) | estimate inertial parameters online |
| **Impedance control** | $M_d\ddot e+D_d\dot e+K_de=F_{ext}$ — robot behaves as mass-spring-damper; safe contact |
| **Admittance control** | measure force, output motion ($\dot x$ command) — for position-controlled robots w/ F/T sensor |
| Hybrid position/force | split task space into force-/position-controlled directions |
| Operational-space control (Khatib) | $F=\Lambda\ddot x_d+\mu+p$, $\tau=J^\top F+N^\top\tau_0$ |
| Task-priority / null-space | hierarchical tasks via projectors |
| **Whole-body control (WBC)** | QP: minimize task errors s.t. dynamics, contact cone, torque/joint limits (e.g. HQP, TSID) |
| Passivity/energy shaping, CBF/CLF-QP | provable safety/stability |
| Visual servoing (IBVS/PBVS) | image-feature error drives velocity via interaction matrix |
| Iterative learning, repetitive control | repeated tasks |

## Model Predictive Control (MPC)
At each step solve finite-horizon problem, apply first input, repeat:
$$\min_{u_{0:N-1}}\ \sum_{k=0}^{N-1}\ell(x_k,u_k)+V_f(x_N)\ \ \text{s.t. } x_{k+1}=f(x_k,u_k),\ x\in\mathcal X,\ u\in\mathcal U$$
- Linear MPC → QP (OSQP, qpOASES, HPIPM, ECOS); nonlinear → SQP/RTI (acados, CasADi+IPOPT, ACADOS, FORCES Pro), **iLQR/DDP** (Crocoddyl, ALTRO), sampling-based **MPPI/CEM** (GPU-friendly, handles non-differentiable costs).
- Stability via terminal cost/set; recursive feasibility; soft constraints; warm start; real-time iteration scheme.
- Applications: **centroidal MPC for legged robots** (MIT Cheetah, ANYmal), car/path tracking, drone racing, contact-implicit MPC.

## Trajectory generation
Polynomial (cubic/quintic), trapezoidal velocity profile, S-curve (jerk-limited), minimum-snap for quadrotors (differentially flat), time-optimal path parameterization **TOPP-RA**, splines, Ruckig online trajectory generator.

## Controller stack for robot arm (typical)
`trajectory → IK/OSC → joint impedance/torque control @1 kHz → motor FOC`; use `ros2_control` hardware interface + controllers (joint_trajectory_controller, forward_command, admittance, cartesian_impedance).

## Interview Q&A

**Integral windup?** Integrator accumulates while actuator saturates; clamp or back-calculate.

**Why derivative on measurement?** Avoids derivative kick on setpoint step.

**LQR vs MPC?** LQR unconstrained, infinite horizon, offline gain; MPC handles constraints & nonlinearity online at compute cost.

**Impedance vs admittance?** Impedance: motion in → force out (needs torque control, back-drivable). Admittance: force in → motion out (works on stiff position-controlled arms, less transparent).

**Why is gravity compensation important?** Removes configuration-dependent load so PID gains can be low (safer, less steady-state error).

**How to prove stability?** Find Lyapunov function; for linear check eigenvalues; for sampled systems check discrete poles inside unit circle.

**How to choose MPC horizon?** Long enough to capture dynamics/constraints (≥ settling time), short enough for real-time; use terminal cost to compensate.
