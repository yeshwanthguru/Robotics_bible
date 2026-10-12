---
title: Legged & Humanoid Locomotion
---

# Legged & Humanoid Locomotion

## Concepts
- **Support polygon**, static vs dynamic stability, gait (walk, trot, pace, bound, gallop), duty factor, swing/stance, contact schedule, Raibert hopper heuristic (foot placement $p=\frac{T_s}{2}v+k(v-v_d)$).
- **Models:** LIPM (point mass at constant height), SLIP (spring-loaded inverted pendulum, running), single rigid body (SRBD), centroidal dynamics, full-body floating-base dynamics.
- **Stability criteria:** ZMP (flat ground), capture point / DCM (divergent component of motion) $\xi=c+\dot c/\omega$, centroidal momentum, FWS, viability.

## Control approaches
| Approach | Details |
|---|---|
| ZMP preview control (Kajita) | LIPM + LQ preview of ZMP reference → CoM trajectory; classic Honda/HRP |
| Capture-point / DCM walking | footstep adjustment via DCM error (Atlas-DARPA, TORO) |
| **Centroidal / SRBD MPC** | QP over GRFs with friction pyramids (MIT Cheetah 3, ANYmal) |
| **Whole-body control (WBC)** | QP tracks CoM, swing foot, torso; respects dynamics & contact |
| Trajectory optimization (contact-implicit, multi-contact) | Crocoddyl, TOWR, Drake, OCS2 |
| **Model-free RL** | PPO with massively-parallel sim; velocity-command tracking policy, terrain curriculum; transferred zero-shot (ANYmal, Cheetah, Unitree, Digit) |
| **Teacher–student / privileged learning** (RMA, "Learning to walk in minutes") | teacher with ground-truth terrain/friction, student infers latent from history |
| Imitation of animals/humans motion | AMP (adversarial motion priors), DeepMimic, ASE, PHC, **ExBody/H2O/OmniH2O/HumanPlus/GMT** for humanoids |
| Hybrid | RL policy + MPC/foot-placement prior, residual RL on model-based |
| Parkour / perceptive locomotion | height maps, depth cam, ViT; "Extreme Parkour", ANYmal parkour |

### Typical RL locomotion setup (Isaac Lab / legged_gym)
- **Observation:** base ang vel, projected gravity, commands $(v_x,v_y,\omega_z)$, joint pos/vel, previous action, (height scan). **Action:** joint position targets → PD ($\tau=K_p(q^*-q)-K_d\dot q$) at 200–1000 Hz, policy at 50 Hz.
- **Rewards:** velocity tracking (exp), −orientation, −torque², −joint acc, −action rate, foot air-time, feet slip, joint-limit & collision penalties, termination on fall.
- **Domain randomization:** friction, mass, COM, motor strength, PD gains, latency, push perturbations, terrain roughness.
- **Curriculum:** terrain difficulty by performance.
- Actuator net/DR for sim2real; symmetry augmentation; Lipschitz constraints / smoothness regularization to avoid jitter.

## Humanoid specifics
- High DOF (≈ 20–45), underactuated floating base, narrow support, hands/arms for manipulation → **loco-manipulation**.
- Teleop/whole-body retargeting via human MoCap (SMPL → robot), then RL tracking in sim for a general motion tracker.
- Foundation efforts: GR00T, Helix, Figure 02/03, Optimus, Atlas (Boston Dynamics electric + LBM), Digit (Agility), Unitree G1/H1, Apollo, NEO, Booster T1, Fourier GR-1/GR-3, UBTech Walker S, Xpeng Iron.
- Hardware issues: thermal limits, battery (~2–4 h), falls (damage → fall detection, protective motions, get-up policies), hand reliability.

## Estimation for legged
Contact detection (force thresholds / learned), base velocity from leg kinematics (stance leg zero-velocity), IMU fusion (InEKF), terrain mapping (elevation_mapping, GridMap), footstep planning on height map.

## Interview Q&A

**LIPM assumptions?** Constant CoM height, massless legs, no angular momentum → linear dynamics; fast to plan, limited for rough terrain.

**Why PD at the joint with RL policy outputting position targets?** Smooths exploration, implicit torque limits, easier sim2real than raw torque.

**Why privileged teacher-student?** Teacher learns faster using unobservable terrain/friction; student distills using only proprioceptive history → deployable.

**MPC vs RL for locomotion?** MPC: interpretable, constraints, needs accurate model/terrain; RL: robust agile skills, needs sim and reward engineering; hybrids are common.

**How do humanoids recover from pushes?** Ankle/hip strategy, stepping (capture point), momentum control, learned recovery policies.
