---
title: Sim-to-Real Transfer
---

# Sim-to-Real

## Sources of the reality gap
1. **Dynamics:** inertial params, friction/restitution, contact model, joint damping, backlash, cable forces.
2. **Actuation:** motor torque-speed limits, PD latency, bandwidth, thermal limits, gearbox compliance.
3. **Sensing:** noise, bias, latency, quantization, calibration errors, rolling shutter, depth artefacts.
4. **Appearance:** textures, lighting, reflections.
5. **System:** control-loop jitter, communication delays, battery voltage sag, wear.
6. **Unmodelled:** deformables, cables, slippage, wind.

## Techniques
| Technique | Idea |
|---|---|
| **Domain randomization (DR)** | randomize physics & visuals over wide ranges so reality ≈ one more sample; risk: conservative policies, wasted capacity |
| **Automatic DR (ADR)** | widen ranges automatically while performance holds (OpenAI Rubik's cube) |
| **System identification** | fit sim parameters to real data (least squares, Bayesian, CMA-ES); **SimOpt / BayesSim / DROPO** adapt DR distribution from real rollouts |
| **Actuator networks** | learn torque from (position error, velocity history) using real data (ANYmal) |
| **Domain adaptation** | image-to-image translation (CycleGAN, RetinaGAN), feature alignment, **Cosmos Transfer** style augmentation |
| **Teacher–student / privileged distillation** | student uses only deployable sensors |
| **Rapid Motor Adaptation (RMA)** | adaptation module infers latent env params from history |
| **Residual / hybrid** | learn correction on top of analytic controller or learned residual dynamics |
| **Real-world fine-tuning** | few real rollouts, RL/IL fine-tuning, human-in-the-loop |
| **Sim2Sim validation** | transfer between engines first |
| **Digital twin / real2sim** | scan real scene (NeRF/3DGS/photogrammetry) → simulation assets (e.g. Real2Sim eval for VLAs) |
| **Latency & noise modelling** | randomize obs/action delay 0–20 ms |
| **Regularization for smoothness** | action rate penalty, Lipschitz constraint, low-pass filter, symmetry |
| **Safety layers** | torque/velocity limits, CBF filter, fall detection |

## Checklist for a locomotion/manipulation sim2real
1. Match joint ordering, zero offsets, units, control frequency, PD gains between sim and robot.
2. Log real data → compare to sim (torque, velocity, contact timing).
3. Fit motor model; apply delay.
4. Randomize: friction (0.3–1.5), payload mass (±20 %), COM shift, PD gains (±20 %), motor strength, ground compliance, push perturbations, sensor noise & bias.
5. Observation hygiene: no privileged info to actor, clip & normalize identically, same filter (e.g. low-pass IMU).
6. Test with robot on a gantry/harness; start with low gains/speeds; staged rollouts.
7. Measure: success rate, tracking error, cost of transport, falls per km, intervention rate.

## Evaluating policies
Real-to-sim correlation of policy rankings (SIMPLER), world-model-based evaluation (Cosmos, 1X world model), statistical rigor with limited hardware trials.

## Interview Q&A

**Why can DR hurt?** Too-wide ranges make the task unsolvable or the policy overly conservative; use curricula/ADR and system-ID to narrow ranges.

**How do you decide what to randomize?** Sensitivity analysis: perturb each parameter in sim, check policy degradation; prioritize parameters that vary on hardware (friction, mass, latency, motor gains).

**Zero-shot vs fine-tuned transfer?** Locomotion often zero-shot; contact-rich manipulation typically needs real data, force-control layers or fine-tuning.

**What is real2sim2real?** Reconstruct the environment into simulation, train/evaluate there, deploy back—reduces visual/geometric gap.
