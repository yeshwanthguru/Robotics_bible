---
title: Dynamics & Contact
---

# Robot Dynamics

:::tip[The 30-second version]
Kinematics says *where* a robot moves; **dynamics** says *what forces and torques make it move that way*. A heavy arm needs more torque to swing fast; a leg needs to push on the ground to move the body. Dynamics is the physics inside every controller and simulator.
:::

## The equation of motion

$$ M(q)\,\ddot q+C(q,\dot q)\,\dot q+g(q)=\tau $$

Read it as three costs of motion added up:

| Term | Plain meaning |
|---|---|
| $M(q)\ddot q$ | **inertia**: it takes torque to accelerate mass (depends on the arm's posture) |
| $C(q,\dot q)\dot q$ | **Coriolis / centrifugal**: swinging one joint pushes on the others |
| $g(q)$ | **gravity**: the torque just to hold the arm up |
| $\tau$ | what your motors supply (plus external forces $J^\top F_{ext}$) |

> **In words:** "motor torque = (mass × acceleration) + (velocity-coupling forces) + (gravity)."

Handy facts: $M$ is always positive-definite (kinetic energy is positive); the matrix $\dot M-2C$ is skew-symmetric, which control proofs exploit.

**Two directions:** *inverse dynamics* (given the motion you want, what torques?) is used in **computed-torque control**; *forward dynamics* (given torques, what motion?) is what a **simulator** computes.

### Fast algorithms (Featherstone)
**RNEA** (inverse dynamics, O(n)), **CRBA** (the mass matrix), **ABA** (forward dynamics, O(n)). Libraries: **Pinocchio**, Drake, RBDL, MuJoCo.

## Legged robots: the floating base

A walking robot's body is not bolted down, so its base has 6 extra degrees of freedom that **no motor drives directly**. It can only be pushed *through contact forces* from the feet.

$$ M\ddot q+h=S^\top\tau+J_c^\top\lambda $$

> **In words:** "the joint motors act on the joints only; the ground's push $\lambda$ is the only thing that moves the body."

**Contact rules:** the ground can only push (not pull), and friction is limited, a **friction cone**, $\|f_t\|\le\mu f_n$.

### Simple models that make walking tractable

| Model | Idea | Used for |
|---|---|---|
| **LIPM** (inverted pendulum) | a point mass on a stick at constant height | classic walking planners |
| **ZMP** | the point on the ground where tipping torque is zero; must stay inside the feet | stable walking on flat ground |
| **Capture point / DCM** | where to step to come to rest | push recovery |
| **Centroidal dynamics** | total momentum of the whole robot | modern MPC for legged robots |
| **Whole-body dynamics** | every joint | whole-body control (QP) |

$$ \ddot x=\frac{g}{z_c}\,(x-p_{zmp}) $$

> **In words:** "if your centre of mass is ahead of your support point, gravity accelerates you forward: walking is controlled falling."

*Space robots:* with no fixed base, moving the arm pushes the whole satellite the other way (momentum conservation).

## Contact and simulation: why it is hard

Contact is the hard part of physics: things touch or don't, stick or slide, bounce or not. Different simulators model it differently:

| Approach | Used in | Character |
|---|---|---|
| **Penalty (spring-damper)** | simple sims | stiff, needs tiny steps |
| **Complementarity (LCP)** | ODE, Bullet, Drake | physically principled, can be non-unique |
| **Convex soft contact** | **MuJoCo** | smooth, fast, good for gradients and control research |
| **Iterative impulse solvers (PGS/TGS)** | **PhysX (Isaac)** | robust at scale, tune solver iterations |
| **Differentiable** | MJX, Warp, Brax, Genesis | gradients through physics |

**Typical simulation pitfalls:** objects interpenetrating, jitter from stiff contacts, wrong friction, joint damping and motor models omitted, latency ignored.

## Actuators: what makes torque

| Actuator | Plain idea | Notes |
|---|---|---|
| **BLDC + FOC** | efficient electric motor with smart current control | the standard |
| **Harmonic drive** | tiny, huge gear ratio | precise, but friction and compliance |
| **Quasi-direct drive (QDD)** | low gearing | **backdrivable, great for legs and impact** (Unitree, MIT Cheetah) |
| **Series elastic (SEA)** | a spring in series | force control, shock absorption |
| **Hydraulic** | fluid power | highest power density, leaks |
| **Tendon-driven** | cables pull fingers | light hands, friction and stretch |

Gear ratio $N$ makes the motor's inertia feel $N^2$ times bigger at the joint, which is why high-gear robots can't feel contact well. Real motors saturate (torque-speed curve), have friction (Coulomb + viscous), delay, and heat limits. **Actuator networks** (a neural net trained from real data) capture this and close part of the sim-to-real gap.

## System identification
Estimate masses, inertias, friction and delays by driving the robot with exciting trajectories and fitting $\tau=Y(q,\dot q,\ddot q)\pi$ (linear in the unknown parameters $\pi$). Better dynamics = better control and a smaller sim-to-real gap.

## Interview Q&A

**Why is the inertia matrix positive definite?**
*Simply:* kinetic energy can't be negative or zero for real motion.

**What is computed-torque control?**
*Simply:* use the dynamics to cancel the robot's own physics, then apply a simple PD controller to what's left. *Result:* error behaves like a simple damped spring.

**Intuition for ZMP?**
*Simply:* the point where the floor would have to push to keep the robot from tipping. If it's inside the foot, the robot stays flat.

**Why do legged robots use low gear ratios?**
*Simply:* for backdrivability: the legs can feel and absorb impacts instead of fighting them.

**Why can't a floating-base robot control its body directly?**
*Simply:* nothing pushes the base except contact with the world.
