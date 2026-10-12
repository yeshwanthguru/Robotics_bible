---
title: Dynamics & Contact
---

# Robot Dynamics

## Equation of motion (manipulator)
$$M(q)\ddot q+C(q,\dot q)\dot q+g(q)=\tau+J^\top F_{ext}$$
- $M$ symmetric positive-definite inertia matrix; $\dot M-2C$ skew-symmetric (passivity — used in stability proofs).
- Derived by **Lagrange** ($L=T-V$, $\frac{d}{dt}\frac{\partial L}{\partial\dot q}-\frac{\partial L}{\partial q}=\tau$) or **Newton–Euler** (recursive, $O(n)$).

## Algorithms (Featherstone)
- **RNEA** (recursive Newton–Euler): inverse dynamics $\tau=ID(q,\dot q,\ddot q)$ in $O(n)$.
- **CRBA**: compute $M(q)$ in $O(n^2)$.
- **ABA**: forward dynamics $\ddot q=FD(q,\dot q,\tau)$ in $O(n)$.
- Libraries: **Pinocchio**, RBDL, Drake, MuJoCo, Featherstone's spatial vector algebra; autodiff versions (CasADi, Pinocchio-casadi).

## Floating base (legged/humanoid/space)
Generalized coords $q=[q_b\in SE(3),\ q_j]$, dimension $6+n$; actuation only on joints:
$M\ddot q+h=S^\top\tau+J_c^\top\lambda$, $S=[0\ I]$. Contact forces $\lambda$ satisfy friction-cone constraints $\|\lambda_t\|\le\mu\lambda_n$, unilateral $\lambda_n\ge0$, complementarity $\lambda_n\,\phi(q)=0$.
- **Centroidal dynamics:** linear momentum $m\ddot c=\sum f_i+mg$, angular $\dot L=\sum (p_i-c)\times f_i$ (+τ). Basis of centroidal MPC.
- **ZMP / capture point / LIPM:** $\ddot x=\frac{g}{z_c}(x-p_{zmp})$; Zero-Moment Point must stay in support polygon; capture point $\xi=x+\dot x/\omega$, $\omega=\sqrt{g/z_c}$.
- Space robots: momentum conservation, generalized Jacobian, base reaction.

## Contact modelling & simulation
| Approach | Used in | Notes |
|---|---|---|
| Penalty / spring-damper | Gazebo-ODE variants, early sims | stiff, tuning |
| Complementarity (LCP/NCP) | ODE, Bullet, Drake | exact-ish, may be non-unique |
| Convex relaxation (soft constraints) | **MuJoCo** | fast, differentiable-friendly |
| Position-based / XPBD | Isaac Sim (PhysX TGS), Genesis | stable, large timesteps |
| Impulse / PGS solvers | PhysX, Bullet | iterative, solver iteration counts matter |
| Differentiable | Brax, MJX, Warp, Dojo, Genesis | gradient-based policy/system-id |

Sim fidelity pitfalls: penetration, bounce, friction anisotropy, joint damping, motor model, latency.

## Actuator models
DC motor: $\tau=k_ti$, back-EMF $V=iR+k_e\omega$, torque–speed line. Gear ratio $N$: reflected inertia $N^2J_m$, backlash, friction (Coulomb+viscous+Stribeck). Series Elastic Actuator (SEA) gives force control via spring deflection; Quasi-direct drive (low gear ratio, high transparency, used in MIT Cheetah/Unitree) → backdrivable, good for impact. Hydraulic (Atlas legacy), pneumatic/soft, cable-driven (tendons for hands). Actuator network (ANYmal: learned MLP from data) closes sim2real.

## System identification
Estimate inertial parameters via regression $\tau=Y(q,\dot q,\ddot q)\pi$ with excitation trajectories; friction, delay; learned residual dynamics.

## Interview Q&A

**Why is M positive-definite?** Kinetic energy $\tfrac12\dot q^\top M\dot q>0$.

**What is computed-torque control?** $\tau=M(q)(\ddot q_d+K_d\dot e+K_pe)+C\dot q+g$ linearizes dynamics → error obeys $\ddot e+K_d\dot e+K_pe=0$.

**ZMP intuition?** Point on the ground where net horizontal moment of inertial+gravity forces is zero; if inside support polygon, foot doesn't tip.

**Why does low gear ratio help legged robots?** Low reflected inertia and friction → force transparency and impact tolerance.

**Why isn’t floating-base fully actuated?** The base 6 DOF can only be moved via contact forces.
