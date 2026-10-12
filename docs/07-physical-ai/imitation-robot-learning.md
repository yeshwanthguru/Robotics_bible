---
title: Imitation Learning & Robot Learning
---

# Imitation & Robot Learning

## Behavior cloning (BC)
Supervised: $\min_\theta E_{(o,a)\sim D}\|\pi_\theta(o)-a\|$. Problems:
- **Covariate shift / compounding error** – error $O(\epsilon T^2)$.
- **Multimodality** – averaging two valid modes gives an invalid action (go left vs right around obstacle). Fixes: mixture density, discretization, energy-based (IBC), **diffusion/flow**, VQ-BeT.
- **Temporal correlation / pauses** – action chunking.

## Methods
| Method | Idea |
|---|---|
| DAgger | roll out learner, expert relabels visited states |
| HG-DAgger / HIL | human intervenes on failure, data aggregated |
| GAIL / AIRL | discriminator-based reward; RL inner loop |
| Inverse RL / MaxEnt IRL | infer reward that explains demos |
| **ACT** (Action Chunking Transformer) | CVAE transformer predicting k-step chunks; temporal ensembling; ALOHA low-cost bimanual |
| **Diffusion Policy** | denoise action sequence conditioned on obs (CNN-UNet or transformer); receding-horizon execution |
| **3D Diffusion Policy / DP3** | point-cloud conditioned |
| **VQ-BeT, BAKU, MDT** | tokenized/ multitask transformers |
| **Flow-matching policies (π0)** | velocity-field regression |
| **One-shot / in-context** | MimicPlay, ICRT, prompt-conditioned |
| **Goal-conditioned** | language / image goals, hindsight relabeling (HER) |

## Teleoperation & data collection
Leader–follower arms (ALOHA, GELLO), VR/haptics (Apple Vision Pro, Quest), SpaceMouse, exoskeleton gloves (DexCap, AnySkin), **UMI** handheld gripper (embodiment-agnostic), video from human demos (retargeting hand pose → robot), motion capture for humanoids (**H2O, OmniH2O, ExBody, HumanPlus**), simulation generation (**MimicGen** turns ~10 demos into 1000s by transforming object-centric segments).

Data quality matters more than count: consistent strategies, diverse initial states, recover-from-failure examples, synchronized timestamps, calibration, action space choice (joint position vs end-effector delta vs absolute pose).

## Reinforcement learning on robots
- **Sim RL + sim2real** (locomotion, in-hand rotation). See [Sim2Real](../13-simulation/sim2real.md).
- **Real-world RL**: SERL / HIL-SERL (sample-efficient RL with human interventions and reward classifier), residual RL (learn correction on top of base controller), RL fine-tuning of BC/VLA policies (PA-RL, DSRL, PPO on diffusion, "RL token").
- **Reward sources**: hand-designed, success classifier, VLM reward (Eureka, RoboCLIP), learned from videos (VIP, LIV), preference.
- **Safety**: action clipping, impedance limits, CBF filter, workspace bounds, e-stop.

## Representation & perception for policies
Pretrained visual encoders (R3M, VC-1, DINOv2, SigLIP), 3D (point cloud, voxels, Gaussian splats, depth), multi-view + wrist cam, proprioception history, tactile (GelSight, DIGIT), language. Observation normalization & augmentation (random crop/shift, color jitter) strongly improve BC.

## Action spaces
| Space | Pros | Cons |
|---|---|---|
| Joint position targets | simple, robot-specific | not transferable |
| End-effector delta pose | embodiment-agnostic-ish | needs IK, singularities |
| Joint velocity/torque | low-level control | hard to learn |
| Impedance targets (pose + stiffness) | contact-rich safe | more params |
| Keypoints / waypoints (VoxPoser, ReKep) | high-level | needs tracking controller |

## Evaluation protocol
≥20–50 trials per task, fixed initial-state sets, report success ± CI (Wilson/Clopper–Pearson), A/B randomization, stage-wise success, failure categories, time-to-complete.

## Interview Q&A

**Why does diffusion policy beat MSE BC?** Models multimodal action distributions and produces temporally consistent chunks; stable training.

**What does action chunking buy?** Reduces effective horizon (compounding error), smoother motion, handles pauses, lower inference frequency.

**DAgger vs BC?** DAgger trains on the learner's own state distribution with expert labels → $O(T\epsilon)$ error.

**How to make BC robust?** Data augmentation, noise injection into demos, recovery data, DART, ensembling, closed-loop re-planning.

**When RL over IL?** When you can't demonstrate (agile locomotion, super-human speed), reward is clear, and sim is available.
