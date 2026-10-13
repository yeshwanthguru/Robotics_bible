---
title: "Dictionary: C"
sidebar_position: 3
sidebar_label: "C  (98)"
---

# Dictionary: C

[A](./a.md) · [B](./b.md) · [C](./c.md) · [D](./d.md) · [E](./e.md) · [F](./f.md) · [G](./g.md) · [H](./h.md) · [I](./i.md) · [J](./j.md) · [K](./k.md) · [L](./l.md) · [M](./m.md) · [N](./n.md) · [O](./o.md) · [P](./p.md) · [Q](./q.md) · [R](./r.md) · [S](./s.md) · [T](./t.md) · [U](./u.md) · [V](./v.md) · [W](./w.md) · [X](./x.md) · [Y](./y.md) · [Z](./z.md) · [0-9](./0-9.md)

:::tip[Tip]
Use the search box (Ctrl+K). Every term below is its own searchable heading.
:::

### Cache (CPU)

**CS** · Small fast memory close to the processor; contiguous data layouts exploit it.

*Read more:* [CS & algorithms](../01-foundations/cs-dsa-complexity.md)

### Calibration

**ML** · Whether predicted probabilities match real frequencies; fixed with temperature scaling or isotonic regression.

*Read more:* [ML fundamentals](../02-machine-learning/ml-fundamentals.md)

### Callback group

**Software** · Controls which ROS 2 callbacks may run concurrently (mutually exclusive or reentrant).

*Read more:* [ROS 2](../12-software/ros2.md)

### Camera calibration

**Perception** · Estimating a camera's intrinsic parameters and distortion (and extrinsics relative to other sensors).

*Read more:* [Sensors & actuators](../08-robotics/sensors-actuators.md) · [Robot perception](../09-perception-localization/computer-vision-3d.md)

### Camera extrinsics

**Perception** · The pose of a camera relative to another frame (robot base, another sensor).

*Read more:* [Robot perception](../09-perception-localization/computer-vision-3d.md) · [Sensors & actuators](../08-robotics/sensors-actuators.md)

### Camera intrinsics

**Perception** · Focal lengths, principal point and distortion coefficients of a camera.

*Read more:* [Robot perception](../09-perception-localization/computer-vision-3d.md)

### Canadarm2

**Platform** · The Space Station's robotic arm.

*Read more:* [Space & other robots](../11-mobility-dexterity/space-humanoid-other.md) · [Robots & platforms](../reference/robots-platforms.md)

### Canary release

**MLOps** · Rolling out a change to a small fraction of users or robots first.

*Read more:* [MLOps & data engineering](../12-software/mlops-data-engineering.md)

### CAN bus

**Hardware** · Controller Area Network: a robust two-wire serial bus used in vehicles and robot joints.

*Read more:* [Embedded & real-time systems](../12-software/embedded-realtime-microros.md) · [Sensors & actuators](../08-robotics/sensors-actuators.md)

### CAN-FD

**Hardware** · CAN with flexible data rate, giving larger frames and higher speed.

*Read more:* [Embedded & real-time systems](../12-software/embedded-realtime-microros.md)

### Canny edge detector

**Perception** · A multi-step edge detector using gradients, non-maximum suppression and hysteresis thresholds.

*Read more:* [Classical vision & image processing](../09-perception-localization/classical-vision-image-processing.md)

### Capsule network

**DL** · A network design using vectors (capsules) to represent object parts and their pose; mostly research.

*Read more:* [DL architectures](../03-deep-learning/architectures.md)

### Capture point (DCM)

**Robotics** · The point where a robot should step to come to rest; the divergent component of motion.

*Read more:* [Dynamics](../08-robotics/dynamics.md) · [Legged locomotion](../11-mobility-dexterity/legged-locomotion.md)

### Cartesian space

**Robotics** · Task space described by position and orientation in 3-D, as opposed to joint space.

*Read more:* [Kinematics](../08-robotics/kinematics.md)

### Cartographer

**Perception** · Google's real-time 2-D/3-D SLAM system with submaps and loop closure.

*Read more:* [SLAM & localization](../09-perception-localization/slam-localization.md)

### CasADi

**Software** · A symbolic framework for nonlinear optimisation and optimal control with automatic differentiation.

*Read more:* [Control](../10-planning-control/control.md) · [Python](../12-software/python-for-robotics.md)

### Cascade control

**Control** · Nested control loops (current inside velocity inside position).

*Read more:* [Control](../10-planning-control/control.md)

### CatBoost

**ML** · A gradient-boosting library with built-in handling of categorical features.

*Read more:* [ML fundamentals](../02-machine-learning/ml-fundamentals.md)

### Categorical feature

**ML** · A feature taking values from a fixed set of categories; encoded as one-hot, ordinal or target encodings.

*Read more:* [ML fundamentals](../02-machine-learning/ml-fundamentals.md)

### catkin

**Software** · The ROS 1 build system.

*Read more:* [ROS 1](../12-software/ros1.md)

### Causal mask

**DL** · A mask that stops a token attending to later tokens, used in autoregressive language models.

*Read more:* [DL architectures](../03-deep-learning/architectures.md) · [LLMs](../05-foundation-models/llm.md)

### Central limit theorem

**Math** · The average of many independent random samples is approximately Gaussian, whatever the original distribution.

*Read more:* [Math foundations](../01-foundations/linear-algebra-probability.md)

### Centre of mass (CoM)

**Robotics** · The point where a body's mass can be considered concentrated; central to balance.

*Read more:* [Dynamics](../08-robotics/dynamics.md) · [Legged locomotion](../11-mobility-dexterity/legged-locomotion.md)

### Centroidal dynamics

**Robotics** · The dynamics of a robot's total linear and angular momentum about its centre of mass; the basis of legged MPC.

*Read more:* [Dynamics](../08-robotics/dynamics.md) · [Legged locomotion](../11-mobility-dexterity/legged-locomotion.md)

### Chain-of-thought (CoT)

**LLM** · Prompting or training a model to write out reasoning steps before the answer.

*Read more:* [LLMs](../05-foundation-models/llm.md)

### Chain rule

**Math** · The derivative of a composed function is the product of the derivatives of its parts; the mathematical basis of backpropagation.

*Read more:* [Math foundations](../01-foundations/linear-algebra-probability.md) · [DL fundamentals](../03-deep-learning/dl-fundamentals.md)

### Chinchilla scaling

**LLM** · The finding that, for a fixed compute budget, parameters and training tokens should grow together (about 20 tokens per parameter).

*Read more:* [LLMs](../05-foundation-models/llm.md)

### Cholesky decomposition

**Math** · Factoring a symmetric positive-definite matrix A as L times L-transpose with L lower-triangular; used for fast solves and sampling Gaussians.

*Read more:* [Math foundations](../01-foundations/linear-algebra-probability.md)

### CHSH inequality

**Quantum** · A Bell inequality whose violation (up to 2√2) rules out local hidden-variable explanations.

*Read more:* [Quantum basics](../06-quantum/quantum-basics.md)

### Chunking

**NLP** · Splitting documents into pieces for indexing in retrieval.

*Read more:* [NLP, embeddings & retrieval](../05-foundation-models/nlp-embeddings-retrieval.md) · [LLMs](../05-foundation-models/llm.md)

### Circuit depth

**Quantum** · The number of sequential gate layers in a quantum circuit; limits feasibility on noisy hardware.

*Read more:* [Quantum basics](../06-quantum/quantum-basics.md) · [Quantum algorithms](../06-quantum/quantum-algorithms.md)

### Classification

**ML** · Predicting a discrete label.

*Read more:* [ML fundamentals](../02-machine-learning/ml-fundamentals.md)

### Class imbalance

**ML** · One class is far rarer than others; handled with reweighting, resampling, focal loss and PR-AUC.

*Read more:* [ML fundamentals](../02-machine-learning/ml-fundamentals.md)

### Clearpath Husky / Jackal

**Platform** · Rugged research mobile robots.

*Read more:* [Robots & platforms](../reference/robots-platforms.md) · [Mobile navigation](../11-mobility-dexterity/mobile-navigation.md)

### Clifford gates

**Quantum** · The gate set (H, S, CNOT) that maps Pauli operators to Pauli operators; classically simulable.

*Read more:* [Quantum basics](../06-quantum/quantum-basics.md)

### CLIP

**DL** · A model trained to match images with captions; gives a shared image–text embedding space.

*Read more:* [DL architectures](../03-deep-learning/architectures.md) · [VLM & VLA](../05-foundation-models/vlm-vla.md)

### Clipped surrogate objective

**RL** · PPO's loss that limits how far the new policy's action probabilities may move from the old ones.

*Read more:* [RL foundations](../04-reinforcement-learning/rl-foundations.md)

### Closed kinematic chain

**Robotics** · A mechanism where links form loops (parallel robots, a hand holding an object).

*Read more:* [Kinematics](../08-robotics/kinematics.md)

### Clustering

**ML** · Grouping unlabelled data into similar clusters (k-means, DBSCAN, GMM).

*Read more:* [ML fundamentals](../02-machine-learning/ml-fundamentals.md)

### CMake

**Software** · A cross-platform build-system generator for C++ projects.

*Read more:* [C++](../12-software/cpp-for-robotics.md) · [ROS 2](../12-software/ros2.md)

### CNN (convolutional neural network)

**DL** · A network built from convolutions that share small filters across an image; good for vision.

*Read more:* [DL architectures](../03-deep-learning/architectures.md)

### CNOT gate

**Quantum** · A two-qubit gate that flips the target qubit if the control qubit is 1.

*Read more:* [Quantum basics](../06-quantum/quantum-basics.md)

### Cobot

**Robotics** · A collaborative robot designed to work safely near people (force-limited).

*Read more:* [Space & other robots](../11-mobility-dexterity/space-humanoid-other.md)

### Coherence time

**Quantum** · How long a qubit keeps its quantum state (T1 energy relaxation, T2 dephasing).

*Read more:* [Quantum basics](../06-quantum/quantum-basics.md)

### colcon

**Software** · The command-line tool that builds ROS 2 workspaces.

*Read more:* [ROS 2](../12-software/ros2.md)

### Cold-atom interferometer

**Quantum** · A quantum sensor using matter-wave interference of cooled atoms for ultra-precise acceleration and rotation measurement.

*Read more:* [Sensors & actuators](../08-robotics/sensors-actuators.md) · [Space & other robots](../11-mobility-dexterity/space-humanoid-other.md)

### Collaborative filtering

**ML** · Recommending items based on the behaviour of similar users.

*Read more:* [More ML topics](../02-machine-learning/ml-more-topics.md)

### Collision checking

**Planning** · Testing whether a configuration or path intersects obstacles (FCL, GJK, signed distance fields).

*Read more:* [Motion planning](../10-planning-control/motion-planning.md)

### COLMAP

**Perception** · A structure-from-motion and multi-view stereo pipeline.

*Read more:* [Robot perception](../09-perception-localization/computer-vision-3d.md)

### Colour space (HSV, Lab)

**Perception** · Alternative ways to represent colour that separate brightness from hue.

*Read more:* [Classical vision & image processing](../09-perception-localization/classical-vision-image-processing.md)

### Compliance

**Robotics** · The ability to yield to external forces; the inverse of stiffness.

*Read more:* [Control](../10-planning-control/control.md) · [Manipulation & dexterity](../11-mobility-dexterity/manipulation-dexterity.md)

### Composable node

**Software** · A ROS 2 node loaded into a shared process for intra-process zero-copy communication.

*Read more:* [ROS 2](../12-software/ros2.md)

### Computed-torque control

**Control** · Cancelling the robot's dynamics with the model and adding a PD law on the error.

*Read more:* [Control](../10-planning-control/control.md) · [Dynamics](../08-robotics/dynamics.md)

### Concept drift

**ML** · The relationship between inputs and outputs changes over time, degrading a deployed model.

*Read more:* [ML fundamentals](../02-machine-learning/ml-fundamentals.md) · [Evaluate, deploy, debug](../build-your-own/04-evaluate-deploy-debug.md)

### Conditional probability

**Math** · The probability of an event given that another event has occurred, written p(a given b).

*Read more:* [Math foundations](../01-foundations/linear-algebra-probability.md)

### Condition number

**Math** · The ratio of largest to smallest singular value of a matrix; large values mean the problem is nearly singular and noise gets amplified.

*Read more:* [Math foundations](../01-foundations/linear-algebra-probability.md) · [Kinematics](../08-robotics/kinematics.md)

### Confidence interval

**Math** · A range computed from data that would contain the true value a stated fraction (e.g. 95 percent) of the time over repeated experiments.

*Read more:* [Math foundations](../01-foundations/linear-algebra-probability.md) · [Evaluate, deploy, debug](../build-your-own/04-evaluate-deploy-debug.md)

### Configuration space (C-space)

**Planning** · The space of all joint configurations of a robot; planning is a path search in it.

*Read more:* [Motion planning](../10-planning-control/motion-planning.md)

### Conformal prediction

**ML** · A method that wraps any model to give prediction sets with guaranteed coverage.

*Read more:* [More ML topics](../02-machine-learning/ml-more-topics.md) · [Robot perception](../09-perception-localization/computer-vision-3d.md)

### Confusion matrix

**ML** · A table of true/false positives and negatives for a classifier.

*Read more:* [ML fundamentals](../02-machine-learning/ml-fundamentals.md)

### Conjugate gradient

**Math** · An iterative solver for symmetric positive-definite linear systems.

*Read more:* [More math: numerics & graphical models](../01-foundations/more-math-numerics-graphical-models.md)

### Conjugate prior

**Math** · A prior that keeps the same form after a Bayesian update (Beta with Bernoulli, Dirichlet with categorical).

*Read more:* [More math: numerics & graphical models](../01-foundations/more-math-numerics-graphical-models.md)

### Connector (projector)

**VLA** · The module that maps vision-encoder features into the language model's embedding space (an MLP, Q-Former or resampler).

*Read more:* [VLM & VLA](../05-foundation-models/vlm-vla.md) · [Build a VLM](../build-your-own/02-build-a-vlm.md)

### Consensus (multi-robot)

**HRI** · Agents agreeing on a shared value through local communication.

*Read more:* [HRI & multi-agent systems](../07-physical-ai/hri-multi-agent.md)

### Conservative Q-learning (CQL)

**RL** · An offline RL method that penalises Q-values for actions absent from the data.

*Read more:* [RL foundations](../04-reinforcement-learning/rl-foundations.md)

### Constitutional AI

**LLM** · Aligning models using a written set of principles and AI-generated feedback.

*Read more:* [LLMs](../05-foundation-models/llm.md)

### Context window

**LLM** · The maximum number of tokens a model can attend to at once.

*Read more:* [LLMs](../05-foundation-models/llm.md)

### Continuous batching

**LLM** · Serving technique that adds and removes requests from a running batch at every decoding step.

*Read more:* [LLMs](../05-foundation-models/llm.md)

### Continuous integration (CI)

**Software** · Automatically building and testing code on every change.

*Read more:* [Dev tools](../12-software/devtools-deployment.md)

### Contrastive learning

**DL** · Training embeddings so that matching pairs are close and non-matching pairs are far apart.

*Read more:* [DL architectures](../03-deep-learning/architectures.md)

### Control barrier function (CBF)

**Control** · A function used to enforce safety constraints by limiting control inputs so the state stays in a safe set.

*Read more:* [Control](../10-planning-control/control.md)

### Controlled gate

**Quantum** · A gate applied to a target qubit only when a control qubit is in state 1.

*Read more:* [Quantum basics](../06-quantum/quantum-basics.md)

### Convex function

**Math** · A function whose line between any two points lies above its graph; every local minimum is a global minimum.

*Read more:* [Math foundations](../01-foundations/linear-algebra-probability.md)

### Convex optimization

**Math** · Minimising a convex function over a convex set; reliably solvable. Includes LP, QP, SOCP and SDP.

*Read more:* [Math foundations](../01-foundations/linear-algebra-probability.md)

### Convolution (neural)

**DL** · Sliding a small filter over an input and computing weighted sums at each position.

*Read more:* [DL architectures](../03-deep-learning/architectures.md)

### Coriolis force

**Robotics** · Velocity-dependent coupling forces between joints in the equation of motion.

*Read more:* [Dynamics](../08-robotics/dynamics.md)

### Correlation

**Math** · A normalised measure (between −1 and 1) of how linearly two variables move together.

*Read more:* [Math foundations](../01-foundations/linear-algebra-probability.md)

### Correspondence

**Perception** · A matched pair of points or features between two images or point clouds.

*Read more:* [SLAM & localization](../09-perception-localization/slam-localization.md) · [Robot perception](../09-perception-localization/computer-vision-3d.md)

### Cosine learning-rate schedule

**DL** · A learning rate that decays along a half cosine curve, typically after a warm-up.

*Read more:* [DL fundamentals](../03-deep-learning/dl-fundamentals.md)

### Cosine similarity

**NLP** · The cosine of the angle between two vectors; the standard similarity for embeddings.

*Read more:* [NLP, embeddings & retrieval](../05-foundation-models/nlp-embeddings-retrieval.md) · [Math foundations](../01-foundations/linear-algebra-probability.md)

### Cosmos

**Sim** · NVIDIA's world foundation models for generating and augmenting physical-world video.

*Read more:* [Isaac Sim](../13-simulation/isaac-sim.md) · [VLM & VLA](../05-foundation-models/vlm-vla.md)

### Costmap

**Planning** · A grid of costs (obstacles, inflation) used by navigation planners.

*Read more:* [Mobile navigation](../11-mobility-dexterity/mobile-navigation.md) · [SLAM & localization](../09-perception-localization/slam-localization.md)

### Costmap layer

**Perception** · One component (static map, obstacles, inflation) combined into a navigation costmap.

*Read more:* [Mobile navigation](../11-mobility-dexterity/mobile-navigation.md)

### Co-training (robot + web data)

**VLA** · Training a VLA on robot demonstrations together with web vision-language data to keep language skills.

*Read more:* [VLM & VLA](../05-foundation-models/vlm-vla.md)

### Covariance

**Math** · How two variables vary together; the covariance matrix describes the shape of an uncertainty cloud.

*Read more:* [Math foundations](../01-foundations/linear-algebra-probability.md) · [State estimation](../09-perception-localization/state-estimation.md)

### Coverage path planning

**Planning** · Planning a path that visits every part of an area (mowing, cleaning, inspection).

*Read more:* [Motion planning](../10-planning-control/motion-planning.md) · [Mobile navigation](../11-mobility-dexterity/mobile-navigation.md)

### Cross-embodiment learning

**VLA** · Training one model on data from many different robots.

*Read more:* [VLM & VLA](../05-foundation-models/vlm-vla.md)

### Cross-entropy

**Math** · The expected log-loss when using one distribution to code another; the standard classification loss.

*Read more:* [Math foundations](../01-foundations/linear-algebra-probability.md) · [DL fundamentals](../03-deep-learning/dl-fundamentals.md)

### Cross-entropy loss

**DL** · The negative log-probability assigned to the correct class; standard for classification and language modelling.

*Read more:* [DL fundamentals](../03-deep-learning/dl-fundamentals.md)

### Cross product

**Math** · A 3-D vector perpendicular to two input vectors with length equal to the area they span; appears in torque and angular velocity.

*Read more:* [Math foundations](../01-foundations/linear-algebra-probability.md) · [Kinematics](../08-robotics/kinematics.md)

### Cross-validation

**ML** · Splitting data into k folds and rotating which fold is held out, to estimate generalisation.

*Read more:* [ML fundamentals](../02-machine-learning/ml-fundamentals.md)

### CUDA-Q

**Quantum** · NVIDIA's platform for GPU-accelerated quantum simulation and hybrid quantum–classical programming.

*Read more:* [Quantum software](../06-quantum/quantum-software.md)

### Curiosity (intrinsic motivation)

**RL** · A bonus reward for novel or surprising states that drives exploration.

*Read more:* [RL foundations](../04-reinforcement-learning/rl-foundations.md)

### cuRobo

**Planning** · NVIDIA's GPU-accelerated motion generation library.

*Read more:* [Motion planning](../10-planning-control/motion-planning.md) · [Isaac Sim](../13-simulation/isaac-sim.md)

### Curriculum learning

**RL** · Training on tasks of gradually increasing difficulty.

*Read more:* [RL foundations](../04-reinforcement-learning/rl-foundations.md) · [Legged locomotion](../11-mobility-dexterity/legged-locomotion.md)

### Curse of dimensionality

**ML** · In high dimensions data becomes sparse and distances lose meaning, so models need exponentially more data.

*Read more:* [ML fundamentals](../02-machine-learning/ml-fundamentals.md)

### Cycloidal drive

**Hardware** · A compact high-ratio gearbox with high shock tolerance.

*Read more:* [Mechanics & electronics](../08-robotics/mechanics-electronics.md) · [Dynamics](../08-robotics/dynamics.md)

### Cyclone DDS

**Software** · An open-source DDS implementation used as a ROS 2 middleware.

*Read more:* [ROS 2](../12-software/ros2.md)
