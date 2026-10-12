---
title: VLM, VLA & Robot Foundation Models
---

# Vision-Language Models → Vision-Language-Action Models

:::tip[The 30-second version]
A **VLM** can *look at a picture and talk about it* ("there's a red mug on the left").
A **VLA** goes one step further: given the camera image and an instruction like *"put the mug in the sink"*, it outputs **robot actions**. Think of it as an LLM with eyes *and hands*.
The big promise: one model that follows natural-language instructions across many tasks and robots.
:::

## VLM: a language model that can see

![VLA architecture](/img/fig/vla-architecture.svg)
*A VLA is built from the same parts as a VLM (vision encoder + language model) plus an action head on the end.*

A VLM has three parts: a **vision encoder** (CLIP / SigLIP / DINOv2) that turns the image into tokens, a **connector** (a small MLP or Q-Former) that translates image tokens into the language model's "language", and an **LLM** that reasons over both.

| Model | Notes |
|---|---|
| **CLIP / SigLIP** | match images with captions; the "eyes" of most VLMs |
| **LLaVA** | CLIP + MLP + an LLM, tuned on visual instructions |
| **PaliGemma, Qwen-VL, InternVL, Gemini** | modern general VLMs |
| **Molmo** | open model good at *pointing* to things |

Open-vocabulary perception for robots: **GroundingDINO, OWL-ViT, SAM/SAM 2** ("find and cut out the blue box").
Common weaknesses: hallucinating objects, weak spatial reasoning, OCR and charts, too many tokens from video.

## VLA: from words and pixels to motor commands

The policy is $\pi(\text{actions}_{t:t+H}\mid \text{image},\ \text{instruction},\ \text{joint state})$.

### How are actions represented?

| Method | Plain idea | Examples | Trade-off |
|---|---|---|---|
| **Action tokens** | chop each joint value into bins and "say" them like words | RT-2, OpenVLA, π0-FAST | reuses the LLM head; coarse and slow |
| **Regression head** | predict numbers directly | RT-1, Octo (option) | simple, but averages multiple valid options |
| **Diffusion / flow-matching head** | denoise a whole short action sequence | **π0**, GR00T N1, Diffusion Policy | smooth and multimodal, a few extra steps |
| **Action chunking** | predict the next ~50 steps at once | ACT, π0 | smoother, fewer model calls |

### The dual-system idea: slow brain, fast body

![dual system](/img/fig/dual-system.svg)
*Big models are too slow to control motors directly, so the reasoning model runs a few times per second and a small fast policy executes smooth motion.*

Examples: **Figure Helix**, **NVIDIA GR00T N1** (Eagle VLM + diffusion transformer action head).

### Landmark systems (timeline)
- **SayCan**: an LLM picks from skills the robot can actually do.
- **RT-1** → **RT-2**: web knowledge transfers to control by treating actions as text tokens.
- **Open X-Embodiment / RT-X**: one dataset pooled from ~22 robot types.
- **Octo**, **OpenVLA** (7B, open), **π0 / π0.5** (flow-matching action expert), **GR00T N1**, **Gemini Robotics**, **SmolVLA** (small and cheap).

### How they are trained
1. Start from a web-pretrained VLM. 2. **Co-train** on robot demos *and* web question-answering (so it doesn't forget language). 3. **Fine-tune** on your task with a few hundred demos (LoRA). 4. Optionally **RL fine-tune** or add human corrections. 5. Deploy with quantisation and asynchronous action chunks.

### Where the data comes from
Teleoperation (VR, leader-follower arms like ALOHA/GELLO), **UMI** handheld grippers, human video (egocentric), and **simulation + synthetic generation** (MimicGen, Isaac Lab Mimic, Cosmos). Mixed-embodiment data needs a shared action space and per-robot normalisation.

### How do you evaluate one?
Success rate over many trials (≥ 20–50 per task) with error bars, tested on **new objects, new scenes, new phrasing**; benchmarks LIBERO, SimplerEnv, CALVIN, RoboCasa, ManiSkill. Report failure types too.

## World models: imagination for robots
A world model predicts what happens next (video or latent state). Used for planning, synthetic data and **evaluating policies without hardware**. Examples: Dreamer, **NVIDIA Cosmos**, V-JEPA 2, Genie.

## Open problems (good talking points)
Latency, long-horizon memory, millimetre-precise contact-rich tasks, touch/force inputs, safety guarantees, reproducible evaluation, scaling laws for robot data.

## Interview Q&A

**VLM vs VLA?**
*Simply:* a VLM outputs text; a VLA outputs robot actions.

**Why not let the LLM output motor torques directly?**
*Simply:* it is too slow (a few Hz) and imprecise for a 100+ Hz control loop, so we output action chunks that a fast controller tracks.

**Why use diffusion / flow matching for actions?**
*Simply:* demonstrations are multimodal (left or right around the box); averaging fails, sampling a whole smooth chunk works.

**How did RT-2 get web knowledge into control?**
*Simply:* trained on web VQA and robot data together, with actions written as tokens, so "pick the extinct animal" reuses language knowledge.

**Typical VLA failure modes?**
*Simply:* ignores the instruction (follows visual habit), poor spatial precision, breaks under new lighting or objects, compounding errors, slow recovery.

**How would you add touch to a VLA?**
*Simply:* feed tactile or force history as extra tokens, and keep a low-level compliance controller underneath for safe contact.
