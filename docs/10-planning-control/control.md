---
title: Control Theory (PID → MPC → Impedance)
---

# Control

:::tip[The 30-second version]
**Control** = making a system do what you want, *continuously*, using feedback. Think of a thermostat or cruise control: measure, compare with the goal, adjust, repeat many times a second.
- **PID** is the everyday tool (simple, works on most things).
- **LQR / MPC** are smarter: they use a *model* of the system to plan the best correction.
- **Impedance control** makes a robot act like a soft spring so it can safely touch things.
:::

## 🎮 Try it yourself

<div class="simbox"><div class="simhead"><span>Interactive: PID controller</span><a href="/Robotics_bible/sim/pid.html" target="_blank">open full screen ↗</a></div><iframe src="/Robotics_bible/sim/pid.html" height="560" loading="lazy" title="PID controller"></iframe></div>

<div class="simbox"><div class="simhead"><span>Interactive: Balancing a pole (feedback control)</span><a href="/Robotics_bible/sim/cartpole.html" target="_blank">open full screen ↗</a></div><iframe src="/Robotics_bible/sim/cartpole.html" height="560" loading="lazy" title="Balancing a pole (feedback control)"></iframe></div>


## Feedback in one picture

Error = goal − measurement. The controller turns error into a command; the plant (robot) responds; the sensor feeds back. **Feedforward** (a prediction like "holding this arm up needs gravity-compensation torque") does the heavy lifting; **feedback** cleans up the rest.

## PID: the workhorse

$$ u = K_p\,e + K_i\!\int e\,dt + K_d\,\dot e $$

- **P** (proportional): push in proportion to the error now.
- **I** (integral): keep pushing while any error *remains* (removes steady-state error).
- **D** (derivative): brake based on how fast the error is changing (adds damping).

![PID response](/img/fig/pid-response.svg)
*Same target, four controllers. P alone stops short; too much P oscillates; adding D calms it; adding I removes the leftover gap.*

**Practical tips:** limit the integrator (*anti-windup*) when the motor saturates; apply the derivative to the **measurement** (not the setpoint) to avoid a "kick"; filter the D term (noise); add **gravity/friction feedforward** so gains can stay low and safe. Tune with Ziegler–Nichols or relay auto-tune. Use cascaded loops (current → velocity → position).

**Classical theory to name-drop:** poles and stability (all poles in the left half-plane), Bode plots and gain/phase margin, Nyquist, root locus, settling time/overshoot, discretisation (Tustin), delay compensation.

## State-space and optimal control

Describe the system as $\dot x=Ax+Bu$. **Controllable** (you can steer it anywhere) and **observable** (you can infer the state from the output) are the key properties.

**LQR** chooses the feedback gain that best trades "keep the state near zero" against "don't use too much effort":
$$ \min \int x^\top Q x + u^\top R u\,dt \;\Rightarrow\; u=-Kx $$

> **In words:** "Q says what errors hurt, R says what effort costs; LQR finds the gain that balances the two optimally." Used for balancing robots, humanoid walking previews, drones.

**LQG** = LQR + Kalman filter. **iLQR / DDP** extend this to non-linear trajectories. **Lyapunov** analysis proves stability by finding an energy-like function that always decreases.

## Robot-specific controllers

| Controller | Plain idea | Use |
|---|---|---|
| **Computed torque / inverse dynamics** | cancel the robot's physics, then PD | precise arm tracking |
| **Impedance control** | robot behaves like a mass-spring-damper | **safe contact**, human interaction |
| **Admittance control** | measure force, output motion | stiff position-controlled arms with a F/T sensor |
| **Hybrid force/position** | position along some axes, force along others | polishing, insertion, wiping |
| **Operational-space control** | control the hand directly, using the dynamics | arms and humanoid hands |
| **Whole-body control (WBC)** | one QP solving all tasks under contact and torque limits | humanoids, legged robots |
| **Visual servoing** | drive the image error to zero | camera-guided approach |
| **Sliding mode / adaptive** | robust to model errors / learn parameters | uncertain dynamics |
| **CBF / CLF-QP** | safety and stability as constraints | provable safety filters |

$$ M_d\ddot e + D_d\dot e + K_d e = F_{ext} $$

> **Impedance in words:** "if you push the robot, it gives way like a spring of stiffness $K_d$ and damping $D_d$." Softer = safer; stiffer = more precise. Choose per task.

## Model Predictive Control (MPC)

![MPC horizon](/img/fig/mpc-horizon.svg)
*At each step MPC plans the best sequence of actions over a short horizon, executes **only the first**, then re-plans with fresh measurements.*

$$ \min_{u_{0:N-1}}\ \sum_{k}\ell(x_k,u_k)+V_f(x_N)\quad\text{s.t. }x_{k+1}=f(x_k,u_k),\ x\in\mathcal X,\ u\in\mathcal U $$

> **In words:** "predict the future with a model, choose the cheapest sequence of moves that respects all limits, do the first move, repeat."

Why it's loved: handles **constraints** (joint limits, friction cones, obstacles) naturally. Solvers: QP (OSQP, HPIPM), nonlinear (acados, CasADi+IPOPT), **iLQR/DDP** (Crocoddyl), sampling-based **MPPI / CEM** (GPU-friendly). Applications: **centroidal MPC for legged robots**, car and drone tracking, contact-implicit planning.

## Trajectory generation
Cubic/quintic polynomials, trapezoidal velocity profiles, jerk-limited S-curves, minimum-snap for drones, time-optimal path parameterisation (TOPP-RA), **Ruckig** (online, jerk-limited).

## How a whole robot's control stack nests

![control hierarchy](/img/fig/control-hierarchy.svg)
*Fast loops sit near the motors; slow, smart loops sit at the top.*

In ROS 2, `ros2_control` implements the real-time layer (controllers like `joint_trajectory_controller` plus hardware interfaces).

## Interview Q&A

**What is integral windup?**
*Simply:* the I term keeps growing while the motor is stuck at its limit, then overshoots badly. *Fix:* clamp the integrator or back-calculate.

**LQR vs MPC?**
*Simply:* LQR is a fixed formula for unconstrained, linear systems; MPC re-solves a constrained problem every step, handles non-linearity, but costs compute.

**Impedance vs admittance control?**
*Simply:* impedance: motion in → force out (needs torque-controlled, backdrivable robot). Admittance: force in → motion out (works on stiff position-controlled arms).

**Why is gravity compensation useful?**
*Simply:* it removes the posture-dependent load so PID gains can be small, safe and accurate.

**How do you prove a controller is stable?**
*Simply:* find a Lyapunov function whose value always decreases; for linear systems check eigenvalues/poles.

**How do you pick an MPC horizon?**
*Simply:* long enough to "see" the dynamics and constraints (about the settling time), short enough to solve in real time; add a terminal cost to cover the rest.
