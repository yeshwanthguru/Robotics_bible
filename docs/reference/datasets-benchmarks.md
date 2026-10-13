---
title: Datasets & Benchmarks
---

# Datasets and Benchmarks Directory

:::tip[How to use]
Where to find data and how the field measures progress. Always check each dataset's licence before use.
:::

## Vision and perception

| Name | Domain | What it is |
|---|---|---|
| **ImageNet** | classification | 1.28 M training images, 1000 classes; the classic pretraining set |
| **COCO** | detection, segmentation, captions | everyday scenes with boxes, masks, captions |
| **LVIS** | long-tail instance segmentation | 1000+ categories with rare classes |
| **Open Images** | detection | large web-scale annotated set |
| **ADE20K / Cityscapes** | semantic segmentation | scenes and urban driving |
| **Objaverse / Objaverse-XL** | 3-D objects | millions of 3-D assets for synthetic data |
| **BOP benchmark** | 6-D object pose | standard datasets and metrics for pose estimation |
| **YCB / YCB-Video** | objects for manipulation | common household object set and video data |

## 3-D, SLAM and driving

| Name | Domain | What it is |
|---|---|---|
| **KITTI** | driving, odometry | stereo, LiDAR, GPS/IMU driving data; detection and SLAM benchmarks |
| **nuScenes / Waymo Open / Argoverse** | autonomous driving | multi-sensor driving datasets |
| **EuRoC MAV** | visual-inertial SLAM | drone sequences with ground truth |
| **TUM RGB-D / TUM VI** | RGB-D and visual-inertial SLAM | indoor sequences with motion-capture truth |
| **Hilti SLAM Challenge** | construction SLAM | handheld/robot sequences |
| **Newer College** | LiDAR SLAM | outdoor/campus LiDAR-inertial |
| **ScanNet / Replica / Matterport3D** | indoor 3-D scenes | RGB-D scans and meshes |
| **SPEED+** | spacecraft pose | satellite pose estimation images |

## Robot learning and manipulation

| Name | Domain | What it is |
|---|---|---|
| **Open X-Embodiment (RT-X)** | cross-embodiment robot data | pooled datasets from ~22 robots |
| **DROID** | real manipulation | large in-the-wild Franka demonstrations |
| **BridgeData V2** | manipulation | WidowX demonstrations across many scenes |
| **AgiBot World** | manipulation | large-scale humanoid/robot dataset |
| **LeRobot community datasets** | low-cost arms | many SO-100/SO-101 datasets on the Hugging Face Hub |
| **RoboMimic / MimicGen datasets** | imitation learning | benchmark tasks with human and generated demos |
| **LIBERO** | language-conditioned manipulation | 130 tasks in suites (Spatial, Object, Goal, Long) |
| **CALVIN** | long-horizon language tasks | tabletop manipulation benchmark |
| **RLBench / Meta-World / ManiSkill3 / RoboCasa** | simulated manipulation | many tasks for RL/IL |
| **SimplerEnv** | real-to-sim evaluation | simulated evaluation correlating with real results |
| **BEHAVIOR-1K** | household activities | 1000 everyday-activity benchmark in simulation |
| **GraspNet-1B / Dex-Net** | grasping | large grasp datasets |
| **DexMV / Bi-DexHands** | dexterous manipulation | hand benchmarks |
| **Ego4D / EPIC-Kitchens / EgoDex** | human video | egocentric activity data for learning from humans |
| **IsaacLab tasks / Factory / IndustReal** | simulated skills | locomotion, manipulation and assembly environments |

## Language, LLM and VLM benchmarks

| Name | Measures |
|---|---|
| **MMLU / MMLU-Pro** | broad knowledge across subjects |
| **GSM8K / MATH** | grade-school and competition maths |
| **HumanEval / MBPP / SWE-bench** | coding (functions; real GitHub issues) |
| **GPQA** | graduate-level science questions |
| **HellaSwag / ARC / WinoGrande** | commonsense reasoning |
| **BIG-bench / BBH** | diverse hard tasks |
| **TruthfulQA** | truthfulness |
| **AlpacaEval / MT-Bench / Chatbot Arena** | instruction following and human preference |
| **tau-bench** | tool-using agents |
| **VQAv2 / GQA** | visual question answering |
| **TextVQA / DocVQA / ChartQA / OCRBench** | reading text in images |
| **POPE** | object hallucination |
| **MMBench / MME / MMMU / RealWorldQA** | broad multimodal ability |
| **RefCOCO / BLINK / CV-Bench** | grounding and spatial perception |

## RL and control benchmarks

| Name | What it is |
|---|---|
| **Gymnasium classic control / MuJoCo envs** | standard RL tasks (CartPole, HalfCheetah, Humanoid) |
| **DeepMind Control Suite** | continuous control tasks |
| **Atari (ALE) / Procgen** | discrete-action benchmarks |
| **D4RL / Minari** | offline RL datasets |
| **Isaac Lab locomotion/manipulation tasks** | massively parallel tasks |
| **MuJoCo Playground** | JAX/MJX environments with sim-to-real recipes |
| **Real-world robot suites** | task-specific evaluations on real hardware |

## Quantum benchmarks and resources

| Name | What it is |
|---|---|
| **Quantum volume / randomised benchmarking** | device quality metrics |
| **Application-oriented benchmarks (QED-C, QASMBench)** | circuit suites for comparing hardware |
| **QML datasets (MNIST-style subsets, synthetic)** | small tasks used to test quantum models |

## How to choose and report

1. Pick the benchmark closest to your real task; add your own held-out set.
2. Report **success rates with confidence intervals** and the number of trials.
3. State splits (seen versus unseen scenes/objects), seeds and compute used.
4. Check licences and avoid training on test sets (contamination).
