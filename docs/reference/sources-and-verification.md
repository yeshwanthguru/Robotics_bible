---
title: Sources & Verification Log
---

# Sources and Verification Log

:::tip[Why this page exists]
This handbook is meant to last, but AI and robotics tools change every few months. This page records **what was checked, against which sources, on which date**, and **which claims remain unverified**, so you know how far to trust each part and where to look when something has changed.
:::

**Last audit: 13 October 2026.** The audit had two parts: (1) every code snippet in the book was parsed, and most were executed or compiled; (2) the most version-sensitive facts were checked against documentation and papers.

## 1. Code that was executed or compiled

| Item | How it was checked | Result |
|---|---|---|
| `examples/01_tiny_gpt.py`, `02_tiny_vlm.py`, `03_tiny_vla.py` | run end to end on CPU with PyTorch | work; results quoted in the Build It Yourself chapters; code printed in the chapters is byte-identical to the files |
| All 39 Python snippets | parsed with the Python parser | no syntax errors |
| A\* search, Kalman filter step, damped-least-squares IK, Wilson interval | executed with tests (A\* compared with breadth-first search; Kalman filter tracking test; IK convergence) | pass |
| Coding-challenge snippets (quaternion to matrix, odometry, PID with anti-windup, systematic resampling, Kabsch alignment, attention, PPO loss, GAE, diffusion loss) | executed with unit tests (attention compared with PyTorch's reference, including the causal mask; Kabsch recovers a known rotation) | pass |
| Gymnasium environment example | passed Gymnasium's `check_env` | pass |
| Qiskit Bell-pair and Grover snippets | executed; Grover output state checked | pass (Grover gives |11⟩ with probability ≈ 1) |
| PennyLane VQE snippet | executed; compared with the exact ground energy from diagonalisation | pass (−1.1179 versus exact −1.1180) |
| OpenCV red-blob snippet | executed on a synthetic image | pass |
| C++ `SafeQueue` and lock-free `Spsc` ring buffer | compiled with `-Wall -Wextra` (C++20) and run under ThreadSanitizer with producer/consumer threads | pass, no warnings or races |
| PDDL domain and problem | solved with the `pyperplan` planner | returns the plan shown in the book (move, pick, move, place) |
| TRL `SFTConfig`, PEFT `LoraConfig`, TRL `DPOConfig` arguments | constructed with TRL 1.15, transformers 5.19, PEFT 0.21 | **found and fixed:** `warmup_ratio` is no longer accepted; the book now uses `warmup_steps` |

**Not executable here (reviewed by reading against documented APIs only):** ROS 2 Python and C++ nodes, launch files and the action server; Isaac Sim, Isaac Lab and Isaac Gym snippets; MuJoCo viewer loop; MATLAB and R snippets; the real-model Hugging Face fine-tuning code (needs model downloads); LeRobot commands.

## 2. Facts checked against sources

| Claim in the book | Verdict | Source |
|---|---|---|
| ISO/TS 15066 content is part of the collaborative-robot requirements | **Updated.** ISO 10218-1 and -2 were revised in 2025 and absorbed the TS 15066 content; the book now says so | [Automate (A3)](https://www.automate.org/robotics/news/updated-iso-10218-major-advancements-in-industrial-robot-safety-standards-now-available/aph), [Control Design](https://www.controldesign.com/industry-news/news/55268769/iso-10218-update-makes-functional-safety-requirements-more-explicit) |
| Cyclone DDS is the default ROS 2 middleware in Jazzy | **Corrected.** Fast DDS is the default in Jazzy and Kilted; rmw_zenoh is Tier 1 in Kilted but not the default | [ROS 2 Jazzy RMW docs](https://docs.ros.org/en/jazzy/Installation/RMW-Implementations.html), [Kilted RMW docs](https://docs.ros.org/en/kilted/Installation/RMW-Implementations.html) |
| LLaVA-1.5 recipe (stage 1: lr 1e-3, batch 256; stage 2: lr 2e-5, batch 128; 558K and 665K samples) | **Confirmed** | [Improved Baselines with Visual Instruction Tuning (arXiv 2310.03744)](https://arxiv.org/pdf/2310.03744) |
| SmolVLA: about 450M parameters, open, flow-matching action expert, asynchronous inference, about 20k fine-tuning steps | **Confirmed** (the docs quote roughly 4 hours on one A100 for 20k steps) | [SmolVLA blog](https://huggingface.co/blog/smolvla), [paper listing](https://huggingface.co/papers/2506.01844), [LeRobot SmolVLA guide](https://huggingface.co/docs/lerobot/smolvla) |
| π0: PaliGemma backbone with a ~300M-parameter action expert trained with flow matching, action horizon 50 | **Confirmed** (the exact control frequency in Hz is *not* confirmed, so the book says "roughly 20–50 Hz") | [π0 (arXiv 2410.24164)](https://arxiv.org/pdf/2410.24164), [π0.5 (arXiv 2504.16054)](https://arxiv.org/pdf/2504.16054) |
| Isaac Sim 5.0 is open source on GitHub; pip install `isaacsim[all,extscache]` | **Confirmed, with nuance:** Isaac Sim's own extensions are open; parts of Omniverse Kit stay closed | [NVIDIA announcement](https://developer.nvidia.com/blog/announcing-general-availability-for-nvidia-isaac-sim-5-0-and-nvidia-isaac-lab-2-2), [install docs](https://docs.isaacsim.omniverse.nvidia.com/5.0.0/installation/install_python.html) |
| Isaac Lab training script path `scripts/reinforcement_learning/rsl_rl/train.py` | **Confirmed** (a newer v3 early-access docs set introduces a unified CLI) | [Isaac Lab RL scripts](https://isaac-sim.github.io/IsaacLab/main/source/overview/reinforcement-learning/rl_existing_scripts.html) |
| Isaac Lab-Arena is a policy-evaluation framework that works with GR00T | **Confirmed** | [Isaac Lab-Arena docs](https://isaac-sim.github.io/IsaacLab-Arena/main/pages/example_workflows/agentic_env_gen/eval_with_gr00t.html) |
| Newton is a GPU physics engine from NVIDIA, Google DeepMind and Disney Research, under the Linux Foundation, built on Warp with a MuJoCo Warp backend | **Confirmed** | [Linux Journal](https://www.linuxjournal.com/content/linux-foundation-welcomes-newton-next-open-physics-engine-robotics), [PyPI](https://pypi.org/project/newton/) |
| Gazebo Classic reached end of life in January 2025 and is not supported on ROS 2 Jazzy | **Confirmed** | [OSRF Discourse](https://discourse.openrobotics.org/t/gazebo-classic-end-of-life-ros-2-jazzy/36239) |
| RSA-2048 resource estimate: under one million noisy qubits, under a week | **Confirmed** as an estimate (newer proposals claim lower counts, so treat any such number as moving) | [Gidney, arXiv 2505.15917](https://arxiv.org/abs/2505.15917v1) |
| Surface-code error correction below threshold on Google's Willow chip | **Confirmed** (preprint August 2024, Nature publication December 2024) | [arXiv 2408.13687](https://arxiv.org/pdf/2408.13687) |
| ACT default chunk size 100 and KL weight 10; Diffusion Policy horizon 16 with 8 executed steps | **Partly confirmed:** seen in LeRobot configs and examples, but learning-rate defaults come from early configs, so the book calls them "typical starting points" | [LeRobot docs](https://huggingface.co/docs/lerobot/en) |
| LeRobot commands | **Version-dependent.** The docs show both `python -m lerobot.record` style and `lerobot-train` / `lerobot-record` console commands, so the book shows both forms and tells you to run `--help` | [LeRobot real-robot guide](https://huggingface.co/docs/lerobot/getting_started_real_world_robot) |

## 3. Still unverified (treat with care)

| Claim | Why it is unverified | What to do |
|---|---|---|
| π0 GPU memory needs (LoRA fine-tuning about 24 GB, full fine-tuning about 70 GB) | I could not find the figures in a source during the audit; the book now gives only a soft statement | read the `openpi` README for current numbers |
| Exact Isaac Lab task ID `Isaac-Velocity-Rough-Anymal-D-v0` | the docs I found show the Flat Anymal-D task; the Rough variant is believed to exist but was not confirmed | run `list_envs.py` in your installed version |
| `omni.isaac.*` renamed to `isaacsim.*` in Isaac Sim 4.5/5.0 | not found in a source during the audit; reflected in my own experience and in the 5.0 pip package naming | check the Isaac Sim migration notes |
| LeRobot learning-rate and step defaults | taken from early configs and example commands | check `configuration_*.py` in the installed version |
| Dictionary, Q&A and reference tables in general | written from broad knowledge; the audit above covered the items listed, not every line | correct any entry you find wrong (edit `tools/glossary/src/*.txt` or the page) |

## 4. How to re-verify when something changes

1. **ROS 2:** [docs.ros.org](https://docs.ros.org) (releases, RMW, tier tables).
2. **Isaac Sim / Lab:** the official Isaac Sim and Isaac Lab documentation sites; run `list_envs.py` for task IDs.
3. **LeRobot / SmolVLA / π0:** the Hugging Face LeRobot docs and the `openpi` repository README.
4. **Papers:** read the arXiv abstract page for hyper-parameters and numbers.
5. **Standards:** the ISO catalogue page and your national standards body (editions change).
6. **Libraries:** run the snippet in a clean environment; if an argument is rejected, read the library's current changelog.

When you correct something, add the source here so the next reader can trust it.
