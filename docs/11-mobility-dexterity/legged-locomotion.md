---
title: Legged & Humanoid Locomotion
---

# Legged & Humanoid Locomotion

:::tip[The 30-second version]
Walking is **controlled falling**: you lean forward, then catch yourself with the next step, over and over. Legged robots must decide *where to step* and *how hard to push the ground*, while staying balanced on a body that nothing directly holds up.
Two schools: **model-based** (planning + MPC with physics models) and **learned** (RL in simulation). Today's best robots mostly use **RL-trained policies** for agility, sometimes wrapped in model-based safety and estimation.
:::

## Walking = controlled falling

![walking pendulum](/img/fig/walking-pendulum-gait.svg)
*Left: the body is like an inverted pendulum that keeps toppling forward; each step catches it. Right: a gait chart; feet alternate between ground and air.*

Vocabulary: **support polygon** (the area under your feet), **stance / swing** phases, **gait** (walk, trot, bound, gallop), **duty factor** (fraction of time a foot is on the ground), **footstep planning**.

**Stability notions:** static (centre of mass over the support polygon), **ZMP** (zero-moment point must stay in the foot), **capture point / DCM** (where to step to stop), centroidal momentum.

## Approach 1: model-based control

| Method | Plain idea |
|---|---|
| **ZMP preview control** (Honda-style) | plan the centre-of-mass motion so the ZMP stays under the foot |
| **Capture-point walking** | adjust the next footstep from the current falling speed |
| **Centroidal / SRBD MPC** | optimise ground forces over the next ~1 s (MIT Cheetah, ANYmal) |
| **Whole-body control (WBC)** | a QP that tracks body, foot and posture goals within torque and friction limits |
| **Trajectory optimisation** | multi-contact planning (Crocoddyl, TOWR, OCS2) |

Strengths: interpretable, constraint-aware. Weaknesses: needs accurate models, hand-tuned gaits, struggles with rough terrain without careful perception.

## Approach 2: learn it with RL in simulation

![policy io](/img/fig/policy-io.svg)
*The learned policy is a small network: sensor readings in, target joint angles out at ~50 Hz. A PD controller turns targets into torques at hundreds of Hz.*

![reward terms](/img/fig/reward-terms.svg)
*Reward = a weighted score of "good" (follow the speed command, rhythmic stepping) and "bad" (energy, jerk, falling).*

**The standard recipe (Isaac Lab / legged_gym):**
- **Observation:** body angular velocity, gravity direction in the body frame, the velocity command, joint positions/velocities, last action, optionally a terrain height scan.
- **Action:** joint position offsets → PD controller → torque.
- **Algorithm:** **PPO** with thousands of parallel simulated robots.
- **Terrain curriculum:** start on flat ground, get harder (stairs, slopes, stepping stones) as the robot succeeds.
- **Domain randomization:** friction, payload, centre of mass, motor strength, PD gains, delays, pushes, sensor noise.
- **Asymmetric actor-critic:** the critic sees privileged simulator data; the actor sees only deployable sensors.

![teacher student](/img/fig/teacher-student.svg)
*Teacher–student: a teacher with perfect knowledge learns easily; a student that only uses real sensors copies it. (RMA, perceptive parkour.)*

**Imitating animals and humans:** DeepMimic, **AMP** (adversarial motion priors), and for humanoids ExBody, H2O, OmniH2O, HumanPlus: retarget human motion-capture to the robot, then RL tracks it, giving one general motion-tracking policy.

**Making it deployable:** actuator model or actuator network, latency randomisation, action-rate penalty (smoothness), symmetry, torque limits, careful PD gains, sim-to-sim check in MuJoCo.

## Humanoid specifics
- Many joints (20–45), narrow feet, floating base → hard to balance, plus arms and hands for **loco-manipulation** (carrying, opening doors).
- Typical stack: **learned whole-body controller** + a high-level VLA/planner giving it targets (e.g. GR00T, Helix).
- Practical issues: motor overheating, battery life, falls (fall detection, protective motion, get-up policies), fragile hands.
- Players: Atlas, Optimus, Figure, Digit, Unitree G1/H1, Apollo, NEO, Booster, Fourier.

## State estimation for legged robots
Detect foot contact (force thresholds or learned), estimate base velocity from stance-leg kinematics, fuse with the IMU (invariant EKF), build a height map for footstep planning (elevation_mapping), add LiDAR to cancel drift.

## Interview Q&A

**What are the assumptions of the LIPM?**
*Simply:* constant body height, massless legs, no angular momentum. That makes the dynamics linear and easy, but it limits rough-terrain use.

**Why does the RL policy output position targets for a PD controller instead of torques?**
*Simply:* it makes exploration smoother, implicitly limits torque, and transfers to hardware more easily.

**Why teacher–student?**
*Simply:* the teacher learns quickly with secret information, the student learns to act with what real sensors provide.

**MPC vs RL for locomotion?**
*Simply:* MPC is explainable and handles constraints but needs good models; RL is agile and robust but needs simulation and reward design. Hybrids are common.

**How do humanoids recover from a push?**
*Simply:* ankle/hip strategies for small pushes, stepping (capture point) for larger ones, momentum control, or learned recovery policies.
