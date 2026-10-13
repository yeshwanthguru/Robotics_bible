---
title: Tools & Libraries Directory
---

# Tools & Libraries Directory

:::tip[How to use]
A lookup table of the software you will meet in robotics and AI, grouped by purpose. Search (Ctrl+K) for a name to jump here. For concepts, see the [Dictionary](../glossary/index.md).
:::

## Deep learning and ML frameworks

| Tool | What it is | Use it for |
|---|---|---|
| **PyTorch** | dynamic-graph deep-learning framework | research and most production training |
| **JAX** | array library with autodiff, JIT and `vmap` | fast research, physics (MJX), large-scale TPU/GPU |
| **TensorFlow / Keras** | Google's DL framework | legacy and mobile (TFLite) |
| **scikit-learn** | classic ML in Python | baselines, preprocessing, tabular models |
| **XGBoost / LightGBM / CatBoost** | gradient-boosted trees | best-in-class tabular models |
| **Hugging Face Transformers** | model zoo and training APIs | LLMs, VLMs, vision, audio |
| **Hugging Face Datasets / Hub** | dataset and model hosting | sharing and versioning |
| **PEFT** | parameter-efficient fine-tuning (LoRA, QLoRA) | fine-tuning large models cheaply |
| **TRL** | SFT, DPO, GRPO trainers | alignment and post-training |
| **Accelerate / DeepSpeed / FSDP** | multi-GPU and sharded training | large models |
| **bitsandbytes** | 8/4-bit quantisation for training | QLoRA |
| **Optuna** | hyper-parameter optimisation | tuning with pruning |
| **Weights & Biases / TensorBoard / MLflow** | experiment tracking | metrics, artefacts, comparison |
| **Hydra / OmegaConf** | configuration composition | reproducible experiments |

## LLM, VLM and retrieval tooling

| Tool | What it is | Use it for |
|---|---|---|
| **vLLM / SGLang / TGI** | high-throughput LLM serving | production inference |
| **llama.cpp / GGUF / MLC** | CPU and edge inference | laptops, phones, small devices |
| **TensorRT-LLM** | NVIDIA-optimised LLM inference | GPU deployment |
| **lm-evaluation-harness** | benchmark runner for LLMs | MMLU, GSM8K, etc. |
| **lmms-eval** | benchmark runner for VLMs | VQA, OCR, hallucination tests |
| **FAISS / HNSWlib / pgvector / Milvus / Qdrant** | vector search and databases | RAG retrieval |
| **LangChain / LlamaIndex** | LLM application frameworks | agents and RAG pipelines |
| **Model Context Protocol (MCP)** | tool-connection standard | connecting LLMs to tools |
| **sentence-transformers** | text embedding models | semantic search |

## Robot learning

| Tool | What it is | Use it for |
|---|---|---|
| **LeRobot** | Hugging Face robotics library | datasets, ACT, Diffusion Policy, SmolVLA, π0, low-cost arms |
| **openpi** | Physical Intelligence's π0/π0.5 code | fine-tuning and serving π0 |
| **robomimic** | imitation-learning framework | BC, BC-RNN, offline datasets |
| **Stable-Baselines3 / CleanRL / skrl / RLlib / rsl_rl / rl_games** | RL libraries | PPO, SAC, TD3 |
| **Gymnasium** | RL environment API | custom environments |
| **Isaac Lab** | NVIDIA robot-learning framework | massively parallel RL/IL |
| **GR00T (Isaac GR00T)** | NVIDIA humanoid foundation model and tools | humanoid VLAs |
| **MimicGen / Isaac Lab Mimic** | demonstration generation | scaling demos |
| **Octo / OpenVLA codebases** | open generalist robot policies | fine-tuning baselines |

## Simulators and physics

| Tool | What it is | Use it for |
|---|---|---|
| **Isaac Sim** | Omniverse robot simulator with RTX sensors | photoreal sensors, digital twins, ROS 2 |
| **Isaac Gym (deprecated)** | older GPU RL simulator | legacy code (legged_gym) |
| **MuJoCo / MJX / MuJoCo Warp / Playground** | accurate contact physics; GPU/JAX versions | control research, RL |
| **Gazebo (gz sim)** | ROS-native simulator | integration tests |
| **PyBullet** | Bullet physics in Python | simple prototypes |
| **Genesis** | GPU multi-physics simulator | fast RL, soft bodies |
| **ManiSkill3 / SAPIEN** | GPU manipulation simulator | manipulation benchmarks |
| **Drake** | model-based design toolbox | optimisation-based control |
| **Brax** | JAX physics | very fast RL |
| **Webots / CoppeliaSim** | general robot simulators | education, offline programming |
| **CARLA / AirSim** | driving and drone simulators | autonomy testing |
| **NVIDIA Warp** | GPU kernel language in Python | custom simulation kernels |

## Robotics middleware and software

| Tool | What it is | Use it for |
|---|---|---|
| **ROS 2 (rclcpp, rclpy)** | robot middleware and tools | nearly everything |
| **Nav2** | navigation stack | mobile robots |
| **MoveIt 2** | manipulation planning | arms |
| **ros2_control** | real-time controller framework | joint control |
| **slam_toolbox / Cartographer** | 2-D/3-D SLAM | mapping |
| **robot_localization** | EKF/UKF sensor fusion | GNSS+IMU+odometry |
| **BehaviorTree.CPP / py_trees / Groot** | behavior trees | task logic |
| **PlanSys2 / ROSPlan / Fast Downward** | symbolic planning | PDDL planning |
| **micro-ROS** | ROS 2 on microcontrollers | embedded |
| **Open-RMF** | multi-fleet interoperability | warehouses, buildings |
| **Foxglove / PlotJuggler / RViz2 / rqt** | visualisation | debugging |
| **Isaac ROS** | GPU-accelerated ROS packages | perception on Jetson |
| **Autoware** | autonomous driving stack | research vehicles |
| **PX4 / ArduPilot** | flight controllers | drones |

## Math, kinematics, dynamics, optimisation

| Tool | What it is | Use it for |
|---|---|---|
| **NumPy / SciPy** | numerical Python | everything |
| **Eigen** | C++ linear algebra | fast robotics code |
| **Sophus / manif** | Lie group libraries | pose optimisation |
| **Pinocchio** | rigid-body dynamics | FK, Jacobians, RNEA/ABA |
| **KDL / Orocos** | kinematics library | ROS arms |
| **CasADi** | symbolic NLP and OCP | MPC, trajectory optimisation |
| **acados** | embedded NMPC solvers | fast MPC |
| **OSQP / qpOASES / HPIPM / ECOS** | QP and conic solvers | MPC, whole-body control |
| **IPOPT** | nonlinear interior-point solver | trajectory optimisation |
| **Ceres / g2o / GTSAM** | nonlinear least squares and factor graphs | SLAM, calibration |
| **Crocoddyl / OCS2 / ALTRO** | optimal-control libraries | legged-robot MPC |
| **cuRobo / cuMotion** | GPU motion generation | fast collision-free planning |
| **OMPL** | sampling-based planners | RRT, PRM family |
| **FCL / HPP-FCL** | collision checking | planning |
| **TOPP-RA / Ruckig** | trajectory time-parameterisation | smooth motion |

## Vision, 3-D and perception

| Tool | What it is | Use it for |
|---|---|---|
| **OpenCV** | classic computer vision | calibration, features, I/O |
| **Open3D / PCL** | point-cloud processing | registration, filtering |
| **COLMAP** | structure from motion | reconstruction |
| **Kalibr** | camera/IMU calibration | sensor setup |
| **Ultralytics YOLO / Detectron2 / MMDetection** | detection frameworks | object detection |
| **Segment Anything (SAM/SAM 2)** | promptable segmentation | masks, labelling |
| **Depth Anything / Metric3D / UniDepth** | monocular depth | depth from RGB |
| **FoundationPose / MegaPose** | 6-D pose estimators | grasping unknown objects |
| **evo** | trajectory evaluation | SLAM metrics |
| **TensorRT / ONNX Runtime / DeepStream** | inference runtimes | edge deployment |

## Quantum

| Tool | What it is | Use it for |
|---|---|---|
| **Qiskit** | IBM's quantum SDK | circuits, transpiler, IBM hardware |
| **PennyLane** | differentiable quantum programming | QML, VQE |
| **Cirq** | Google's quantum SDK | NISQ circuits |
| **CUDA-Q** | NVIDIA quantum platform | GPU simulation, hybrid workflows |
| **Amazon Braket / Azure Quantum** | cloud access | multiple hardware vendors |
| **D-Wave Ocean** | annealing SDK | QUBO problems |
| **tket / OpenQASM** | compiler and IR | cross-platform compilation |

## Languages and engineering tools

| Tool | What it is | Use it for |
|---|---|---|
| **Python / C++ / MATLAB / R** | main languages | see the software chapters |
| **CMake / colcon / Bazel** | build systems | C++ and ROS builds |
| **Docker / NVIDIA Container Toolkit** | containers with GPUs | reproducible environments |
| **GitHub Actions / GitLab CI** | automation | tests and deployments |
| **uv / conda / pip** | Python environments | dependency management |
| **DVC / Git LFS** | data and model versioning | large files |
| **Slurm / Kubernetes** | cluster scheduling | training jobs, fleets |
| **gdb / valgrind / sanitizers / perf** | debugging and profiling | C++ performance and bugs |
| **Jetson tools (JetPack, tegrastats, trtexec)** | NVIDIA edge platform | deployment |
