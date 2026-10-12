---
title: Imitation Learning & Robot Learning
---

# Imitation & Robot Learning

:::tip[The 30-second version]
**Imitation learning** = teach the robot by *showing* it. A human demonstrates the task (by tele-operating the robot), the robot records what it saw and what the human did, and a neural network learns "when I see this, do that".
It's the fastest way to get a robot doing a *new task*; the catch is that the robot can drift into situations the human never showed it.
:::

## The pipeline

![imitation pipeline](/img/fig/imitation-pipeline.svg)
*Demonstrate → record → train → deploy → collect more data where it fails → retrain.*

## Behavior cloning (BC) and its big problem

BC is plain supervised learning: input = observation, label = the expert's action.

$$ \min_\theta\ \mathbb E_{(o,a)\sim\mathcal D}\,\|\pi_\theta(o)-a\| $$

> **In words:** "make the robot's action match the human's action in every demonstrated situation."

![BC compounding](/img/fig/bc-compounding.svg)
*A tiny mistake puts the robot in a state the demos never covered, so the next mistake is bigger, and so on (compounding error). **DAgger** fixes this by letting the expert correct the learner's own states.*

Compounding error grows like $T^2\epsilon$ for BC but $T\epsilon$ for DAgger, with horizon $T$.

Two more BC problems:
- **Multimodality:** two valid ways to do something (left or right). An average of them is invalid. Fix with diffusion/flow policies, mixture models or discretisation.
- **Jitter / pauses:** fix with **action chunking** (predict several steps at once).

## Methods at a glance

| Method | Plain idea |
|---|---|
| **DAgger / HG-DAgger** | run the learner; the expert relabels (or takes over) where it goes wrong |
| **GAIL / AIRL** | a discriminator learns to tell expert from robot; the robot tries to fool it |
| **Inverse RL** | infer the reward the expert must have been optimising |
| **ACT** | transformer that predicts a chunk of future actions (the ALOHA system) |
| **Diffusion Policy** | denoise a short action sequence conditioned on observations |
| **VQ-BeT, BAKU, MDT** | tokenised multi-task transformer policies |
| **π0 (flow matching)** | big VLM + flow-matching action expert |
| **Goal-conditioned / language-conditioned** | one policy, many goals; hindsight relabelling |

## Where do demonstrations come from?

| Source | Pros | Cons |
|---|---|---|
| **Teleop with leader-follower arms** (ALOHA, GELLO) | precise, natural | needs a second robot arm |
| **VR / hand tracking** | intuitive, great for humanoids/hands | calibration and latency |
| **SpaceMouse / gamepad** | cheap | clumsy for dexterous tasks |
| **UMI handheld gripper** | collect anywhere, no robot | embodiment gap |
| **Human video** | huge volume | no actions; needs retargeting |
| **Simulation (MimicGen, Isaac Lab Mimic)** | turns ~10 demos into thousands | needs simulated scene |

**Data quality beats quantity:** consistent strategy, varied start positions, a few "recover from mistake" demos, synchronised timestamps, calibrated cameras, and a well-chosen action space.

## Robot RL (when imitation isn't enough)
- **Sim RL → real:** locomotion, in-hand rotation. See [Sim-to-real](../13-simulation/sim2real.md).
- **Real-world RL:** HIL-SERL (human-in-the-loop sample-efficient RL), **residual RL** (learn a small correction on top of a base controller), RL fine-tuning of a BC/VLA policy.
- **Rewards from:** hand design, a learned success classifier, a VLM judge (Eureka, RoboCLIP), or human preferences.
- **Safety:** clip actions, cap forces (impedance), stay inside a workspace, always have an e-stop.

## Perception and action choices

| Choice | Notes |
|---|---|
| **Vision encoder** | pretrained (R3M, VC-1, DINOv2, SigLIP) helps a lot with small data |
| **Observations** | wrist camera + a third-person camera + joint state; sometimes depth, point clouds, tactile |
| **Augmentation** | random crops/shifts and colour jitter greatly improve robustness |

| Action space | Pros | Cons |
|---|---|---|
| **Joint positions** | simple | robot-specific |
| **End-effector delta pose** | transfers across arms | needs IK, singularities |
| **Joint velocity/torque** | low-level | hard to learn |
| **Pose + stiffness (impedance)** | safe contact | more outputs |

## How to evaluate honestly
At least 20–50 trials per task from fixed starting conditions, report success rate **with confidence intervals**, note the failure modes, and randomise the order when comparing policies.

## Interview Q&A

**Why does diffusion policy beat plain MSE regression?**
*Simply:* it can represent several valid behaviours and produces smooth, consistent sequences.

**What does action chunking buy you?**
*Simply:* fewer decisions to get wrong (shorter effective horizon), smoother motion, and less model-call frequency.

**BC vs DAgger?**
*Simply:* BC trains only on expert states; DAgger also trains on the states the learner actually visits, fixing drift.

**How do you make BC more robust?**
*Simply:* augmentation, noise injection, recovery demos, ensembles, closed-loop re-planning.

**When RL instead of imitation?**
*Simply:* when you can't demonstrate (agile locomotion, superhuman speed), you can simulate cheaply, and the reward is clear.
