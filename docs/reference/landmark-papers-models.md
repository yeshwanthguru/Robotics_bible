---
title: Landmark Papers & Models (timeline)
---

# Landmark Papers and Models

:::tip[How to use]
A timeline of the ideas that shaped the field, each with a one-line reason it matters. Good for answering "who introduced X?" and for knowing the history behind modern methods. Years are first publication or release.
:::

## Classics (before 2010)

| Year | Work | Why it matters |
|---|---|---|
| 1958 | **Perceptron** (Rosenblatt) | first trainable neuron model |
| 1960 | **Kalman filter** | optimal recursive estimation for linear-Gaussian systems; still in every robot |
| 1968 | **A\*** (Hart, Nilsson, Raphael) | heuristic shortest-path search |
| 1984 | **BB84** (Bennett, Brassard) | first quantum key distribution protocol |
| 1986 | **Backpropagation** (Rumelhart, Hinton, Williams) | made multi-layer networks trainable |
| 1989 | **Q-learning** (Watkins) | off-policy value learning |
| 1992 | **ICP** (Besl & McKay) | point-cloud registration |
| 1992 | **REINFORCE** (Williams) | the basic policy-gradient method |
| 1994 | **Shor's algorithm** | polynomial-time quantum factoring |
| 1995 | **SVM** (Cortes & Vapnik) | max-margin classifiers with kernels |
| 1996 | **Grover's algorithm** | quadratic quantum search speed-up |
| 1996 | **PRM** (Kavraki et al.) | sampling-based roadmap planning |
| 1997 | **LSTM** (Hochreiter & Schmidhuber) | gated recurrent memory |
| 1998 | **LeNet-5** (LeCun) | practical convolutional networks |
| 1998–2001 | **RRT** (LaValle; LaValle & Kuffner) | rapidly-exploring random trees |
| 1999 | **Monte-Carlo Localization** (Dellaert, Fox, Burgard, Thrun) | particle-filter localisation |
| 2001 | **Random forests** (Breiman) | robust tree ensembles |
| 2002 | **FastSLAM** (Montemerlo et al.) | Rao-Blackwellised particle SLAM |
| 2006 | **GraphSLAM** (Thrun & Montemerlo) | graph-based SLAM formulation |
| 2008 | **HHL** (Harrow, Hassidim, Lloyd) | quantum linear-systems algorithm |
| 2009 | **ROS** (Quigley et al.) | the robot operating system |

## Deep learning and generative models (2012–2019)

| Year | Work | Why it matters |
|---|---|---|
| 2012 | **AlexNet** | deep CNNs win ImageNet; start of the deep-learning era |
| 2012 | **MuJoCo** | fast, accurate contact physics for control research |
| 2013 | **VAE** (Kingma & Welling) | latent-variable generative model with the reparameterisation trick |
| 2013–2015 | **DQN** (Mnih et al.) | deep RL reaches human level on Atari |
| 2014 | **GAN** (Goodfellow et al.) | adversarial generative models |
| 2014 | **Adam** | adaptive optimiser used everywhere |
| 2014 | **Dropout; VGG; GoogLeNet** | regularisation and deeper CNNs |
| 2014 | **Seq2seq and attention** (Sutskever; Bahdanau) | neural machine translation with attention |
| 2014 | **VQE; QAOA** | hybrid quantum algorithms for NISQ devices |
| 2014 | **LOAM** (Zhang & Singh) | LiDAR odometry and mapping |
| 2015 | **ResNet** | residual connections enable very deep nets |
| 2015 | **Batch Normalization** | faster, more stable training |
| 2015 | **TRPO; DDPG** | trust-region and continuous-control RL |
| 2015 | **ORB-SLAM** (Mur-Artal et al.) | robust feature-based visual SLAM |
| 2016 | **AlphaGo** | deep RL plus tree search beats a world champion |
| 2016 | **A3C; XGBoost** | asynchronous RL; scalable gradient boosting |
| 2017 | **PPO** (Schulman et al.) | the workhorse policy-gradient algorithm |
| 2017 | **Transformer** ("Attention Is All You Need") | architecture behind LLMs, VLMs, VLAs |
| 2017 | **Domain randomization** (Tobin et al.) | sim-to-real via randomisation |
| 2017 | **AlphaZero** | self-play RL without human data |
| 2018 | **SAC; TD3** | sample-efficient off-policy actor-critics |
| 2018 | **BERT; GPT-1** | pretrained language models |
| 2018 | **Dactyl** (OpenAI) | in-hand manipulation learned in simulation |
| 2018 | **Dequantisation** (Tang) | classical match for a claimed quantum speed-up |
| 2019 | **ANYmal learned locomotion** (Hwangbo et al.) | RL policies with actuator networks run on real legged robots |
| 2019 | **GPT-2; Quantum "supremacy" (Sycamore)** | scaled LMs; random-circuit sampling demonstration |
| 2019–2020 | **Dreamer** | latent world-model RL |

## Foundation-model era (2020–2023)

| Year | Work | Why it matters |
|---|---|---|
| 2020 | **GPT-3** | in-context learning at scale |
| 2020 | **Scaling laws** (Kaplan et al.) | predictable loss versus size, data, compute |
| 2020 | **DDPM** (Ho et al.) | modern diffusion models |
| 2020–2021 | **ViT** | transformers for images |
| 2021 | **CLIP** | joint image–text embeddings, zero-shot vision |
| 2021 | **LoRA** | cheap fine-tuning with low-rank adapters |
| 2021 | **Isaac Gym; Learning to walk in minutes** | massively parallel GPU RL |
| 2021 | **RMA** (Kumar et al.) | rapid motor adaptation for legged robots |
| 2021 | **DINO; MAE** | strong self-supervised vision features |
| 2022 | **Chinchilla** | compute-optimal data/parameter balance |
| 2022 | **InstructGPT (RLHF)** | aligning language models with human feedback |
| 2022 | **Latent diffusion / Stable Diffusion** | accessible high-quality image generation |
| 2022 | **Flow matching** (Lipman et al.) | simple, fast generative training |
| 2022 | **FlashAttention** | fast exact attention |
| 2022 | **Flamingo; SayCan; RT-1** | multimodal LMs, LLM-grounded robot planning, robot transformers |
| 2023 | **LLaMA** | strong open LLM weights |
| 2023 | **DPO** | preference tuning without a reward model |
| 2023 | **SAM; SigLIP; LLaVA; BLIP-2** | segmentation foundation model, better CLIP loss, open VLM recipes |
| 2023 | **ACT / ALOHA; Diffusion Policy** | action chunking and diffusion for imitation |
| 2023 | **PaLM-E; RT-2; Open X-Embodiment (RT-X)** | embodied LMs, web knowledge into control, cross-robot data |
| 2023 | **MimicGen; Extreme Parkour; 3D Gaussian Splatting** | demo generation, agile legged parkour, fast neural scene rendering |
| 2023 | **Mamba** | selective state-space sequence model |

## Recent (2024–2025)

| Year | Work | Why it matters |
|---|---|---|
| 2024 | **Octo; OpenVLA** | open generalist robot policies |
| 2024 | **π0** | VLM + flow-matching action expert |
| 2024 | **Mixtral and open MoE models** | sparse expert models go mainstream |
| 2024 | **Quantum error correction below threshold** (Google, surface code) | logical error falls as code size grows |
| 2024 | **Cosmos and world foundation models** | generated physical-world video for robots |
| 2025 | **π0.5; GR00T N1; Helix; Gemini Robotics; SmolVLA** | generalist and dual-system VLAs |
| 2025 | **DeepSeek-R1 and RL-trained reasoning models** | reinforcement learning with verifiable rewards for reasoning |
| 2025 | **Isaac Sim open-source; Newton physics engine; MuJoCo Warp** | open GPU physics ecosystem |
| 2025 | **RSA-2048 resource estimate under one million qubits** (Gidney) | lowered the estimated quantum cost of breaking RSA |

## How to use this list in an interview
Pick two or three works per area you can explain in one sentence each (the idea, why it mattered, its limit). For example: *"Diffusion Policy models multimodal demonstrations by denoising action sequences; its limit is the extra inference steps, which flow matching in π0 reduces."*
