---
title: "Q&A 6: Kinematics, Dynamics & Control"
---

# Interview Q&A: Kinematics, Dynamics and Control

:::tip[How to use]
Chapters: [Kinematics](../08-robotics/kinematics.md) · [Dynamics](../08-robotics/dynamics.md) · [Control](../10-planning-control/control.md).
:::

## Kinematics

### Q: Forward versus inverse kinematics?
**Short answer:** FK: joint angles to hand pose (one answer). IK: hand pose to joint angles (zero, one or many answers). **Go deeper:** IK is solved analytically for 6R arms with spherical wrists, or numerically with Jacobian methods or optimisation.

### Q: Why quaternions instead of Euler angles?
**Short answer:** No gimbal lock, smooth interpolation, compact. **Go deeper:** Unit quaternions double-cover SO(3) (q and −q are the same rotation); renormalise after integration.

### Q: What is gimbal lock?
**Short answer:** Two Euler axes align and one rotational degree of freedom is lost. **Go deeper:** For roll-pitch-yaw it happens at pitch = ±90°.

### Q: What is a homogeneous transformation?
**Short answer:** A 4×4 matrix combining rotation and translation so poses compose by multiplication. **Go deeper:** Inverse is [Rᵀ, −Rᵀp; 0, 1].

### Q: DH parameters versus product of exponentials?
**Short answer:** DH uses four numbers per joint with frame conventions; PoE uses screw axes in a single base frame. **Go deeper:** PoE avoids frame-assignment ambiguity and is common in modern texts.

### Q: What is the Jacobian and what does it tell you?
**Short answer:** It maps joint velocities to end-effector velocity (and force to torque via its transpose). **Go deeper:** Its rank and singular values reveal singularities and manipulability.

### Q: What is a kinematic singularity and how do you handle it?
**Short answer:** A pose where the Jacobian loses rank, so some motion is impossible. **Go deeper:** Use damped least squares, plan around it, use redundancy, or switch IK branches.

### Q: How do redundant manipulators use the null space?
**Short answer:** Extra joints can move without moving the hand. **Go deeper:** q̇ = J⁺ẋ + (I − J⁺J)q̇₀ with q̇₀ pushing away from joint limits or obstacles.

### Q: What is damped least squares IK?
**Short answer:** Pseudo-inverse with a damping term for stability near singularities. **Go deeper:** Δq = Jᵀ(JJᵀ + λ²I)⁻¹Δx.

### Q: Why τ = Jᵀ F?
**Short answer:** Energy balance (virtual work): joint work equals hand work. **Go deeper:** τᵀδq = Fᵀδx = FᵀJδq.

### Q: Describe differential-drive kinematics.
**Short answer:** Forward speed is the average of wheel speeds; turn rate is their difference over the wheel separation. **Go deeper:** Non-holonomic: cannot move sideways.

### Q: What is a non-holonomic constraint?
**Short answer:** A velocity constraint that can't be integrated into a position constraint. **Go deeper:** The robot can reach any pose but not move in every direction instantaneously.

### Q: What is hand–eye calibration?
**Short answer:** Finding the camera's pose relative to the robot hand or base. **Go deeper:** Solve AX = XB from several robot motions and observed target poses.

### Q: Why use the 6-D rotation representation in neural nets?
**Short answer:** It is continuous, unlike Euler, axis-angle or quaternion outputs. **Go deeper:** Recover a rotation with Gram–Schmidt on two predicted columns.

## Dynamics

### Q: Write the manipulator equation of motion and explain each term.
**Short answer:** M(q)q̈ + C(q,q̇)q̇ + g(q) = τ: inertia, velocity coupling, gravity. **Go deeper:** M is symmetric positive-definite; Ṁ − 2C is skew-symmetric (used in stability proofs).

### Q: Inverse versus forward dynamics?
**Short answer:** Inverse: motion to torques (control). Forward: torques to motion (simulation). **Go deeper:** RNEA computes inverse dynamics in O(n); ABA computes forward dynamics in O(n).

### Q: Lagrange versus Newton–Euler?
**Short answer:** Lagrange derives equations from energy; Newton–Euler balances forces link by link. **Go deeper:** The recursive Newton–Euler form is more efficient for implementation.

### Q: What is a floating-base robot?
**Short answer:** A robot whose base isn't fixed (legged, flying, space). **Go deeper:** The 6 base DoF are unactuated and driven only through contact forces.

### Q: Explain ZMP.
**Short answer:** The ground point where the net tipping moment is zero. **Go deeper:** If it stays inside the support polygon, the foot doesn't rotate; used in flat-ground walking.

### Q: What is the capture point?
**Short answer:** The point where the robot must step to come to rest. **Go deeper:** ξ = x + ẋ/ω with ω = √(g/z_c) in the LIPM.

### Q: LIPM assumptions?
**Short answer:** Constant centre-of-mass height, massless legs, no angular momentum. **Go deeper:** This makes dynamics linear and planning fast but limits rough-terrain walking.

### Q: Why do legged robots favour quasi-direct-drive actuators?
**Short answer:** Low gear ratio gives backdrivability and impact tolerance. **Go deeper:** Reflected inertia scales with N², so high-ratio gearboxes feel stiff and can't sense contact.

### Q: What does a gear ratio do to inertia and torque?
**Short answer:** Multiplies torque by N and reflected inertia by N². **Go deeper:** Also adds friction and backlash.

### Q: How would you identify a robot's dynamic parameters?
**Short answer:** Drive it along exciting trajectories and fit τ = Y(q,q̇,q̈)π by least squares. **Go deeper:** Include friction and motor models; use optimal excitation and check consistency.

### Q: What is a series elastic actuator?
**Short answer:** A motor with a spring in series, giving force sensing and shock tolerance. **Go deeper:** Trade-off: lower bandwidth.

## Control

### Q: What do P, I and D do?
**Short answer:** P pushes toward the target, I removes steady-state error, D damps. **Go deeper:** D amplifies noise (filter it); I can wind up.

### Q: What is integral windup and how do you prevent it?
**Short answer:** The integral keeps growing while the actuator is saturated. **Go deeper:** Clamp the integrator or use back-calculation; conditional integration.

### Q: Why derivative on the measurement?
**Short answer:** To avoid a spike when the setpoint steps. **Go deeper:** D acts on −ẏ instead of the error derivative.

### Q: How do you tune a PID?
**Short answer:** Start with P, add D to damp, add I to remove offset. **Go deeper:** Ziegler–Nichols, relay auto-tuning, loop shaping from Bode margins.

### Q: What are gain and phase margins?
**Short answer:** How much gain or phase lag you can add before instability. **Go deeper:** Read from Bode plots at crossover.

### Q: How do you test stability?
**Short answer:** Check pole locations (left half-plane / inside the unit circle) or find a Lyapunov function. **Go deeper:** Nyquist and Routh–Hurwitz are alternatives for linear systems.

### Q: What is LQR?
**Short answer:** Optimal state feedback minimising ∫(xᵀQx + uᵀRu). **Go deeper:** Gain from the Riccati equation; Q says which errors hurt, R what effort costs.

### Q: LQR versus MPC?
**Short answer:** LQR is an unconstrained linear formula; MPC re-solves a constrained problem each step. **Go deeper:** MPC handles non-linearity and constraints at compute cost.

### Q: Explain MPC.
**Short answer:** Predict the future with a model, choose the cheapest action sequence respecting limits, apply the first action, repeat. **Go deeper:** Needs terminal cost/constraints for stability, warm starts and fast solvers (OSQP, acados).

### Q: What is computed-torque control?
**Short answer:** Cancel the robot dynamics with the model and add PD on what's left. **Go deeper:** τ = M(q̈_d + K_d ė + K_p e) + Cq̇ + g gives linear error dynamics.

### Q: Impedance versus admittance control?
**Short answer:** Impedance: motion in, force out (needs torque control). Admittance: force in, motion out (works on stiff arms). **Go deeper:** Impedance is more transparent for backdrivable robots.

### Q: What is operational-space control?
**Short answer:** Controlling the hand in task space using the dynamics projected there. **Go deeper:** F = Λẍ_d + μ + p, τ = JᵀF plus null-space terms.

### Q: What is whole-body control?
**Short answer:** A QP that tracks several tasks under dynamics, contact and torque limits. **Go deeper:** Tasks are prioritised (hierarchical QP); used in humanoids and legged robots.

### Q: What is a control barrier function?
**Short answer:** A constraint that keeps the system inside a safe set. **Go deeper:** CBF-QP filters a nominal control input minimally to remain safe.

### Q: Why is gravity compensation useful?
**Short answer:** It removes posture-dependent load so gains can stay low and safe. **Go deeper:** Compute g(q) from the model and add it as feedforward.

### Q: Why feedforward plus feedback?
**Short answer:** Feedforward does most of the work from a model; feedback cleans up the rest. **Go deeper:** It reduces tracking error without high gains.

### Q: What is cascaded control?
**Short answer:** Nested loops, e.g. current inside velocity inside position. **Go deeper:** Inner loops are faster; their bandwidth separation simplifies tuning.

### Q: What is visual servoing?
**Short answer:** Controlling motion directly from image error. **Go deeper:** IBVS uses the image Jacobian (interaction matrix); PBVS uses estimated 3-D pose.

### Q: How do digital control effects matter?
**Short answer:** Sampling, delay and quantisation reduce stability margins. **Go deeper:** Discretise (Tustin/ZOH) and compensate for delay.
