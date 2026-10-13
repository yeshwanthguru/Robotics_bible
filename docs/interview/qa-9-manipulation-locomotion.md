---
title: "Q&A 9: Manipulation, Dexterity & Locomotion"
---

# Interview Q&A: Manipulation, Dexterity, Legged and Humanoid Robots

:::tip[How to use]
Chapters: [Manipulation & dexterity](../11-mobility-dexterity/manipulation-dexterity.md) · [Legged locomotion](../11-mobility-dexterity/legged-locomotion.md) · [Space & other robots](../11-mobility-dexterity/space-humanoid-other.md) · [Imitation learning](../07-physical-ai/imitation-robot-learning.md).
:::

## Grasping and manipulation

### Q: Force closure versus form closure?
**Short answer:** Form closure traps an object by geometry; force closure uses friction to resist any disturbance. **Go deeper:** Force closure needs contact forces inside the friction cones that span the wrench space.

### Q: What is the friction cone?
**Short answer:** The set of contact forces that don't slip: tangential ≤ μ × normal. **Go deeper:** Grasp planning keeps contact forces inside it; soft fingers add torsional friction.

### Q: How do you evaluate grasp quality?
**Short answer:** By how large a disturbance the grasp can resist (Ferrari–Canny metric), plus robustness to pose error. **Go deeper:** Learned metrics (Dex-Net GQ-CNN) predict success probability.

### Q: What is the grasp matrix?
**Short answer:** It maps contact forces to the net wrench on the object: w = Gf. **Go deeper:** Its rank and the cone constraints determine whether a grasp is force-closure.

### Q: Describe a bin-picking system end to end.
**Short answer:** RGB-D perception → segmentation → grasp proposals → collision-free approach → force-aware close and lift check → place → retry or ask for help. **Go deeper:** Track picks/hour, success rate, intervention rate; handle shiny/transparent objects with stereo or learned depth.

### Q: What makes peg-in-hole hard?
**Short answer:** Clearance is smaller than the position uncertainty. **Go deeper:** Use compliance (RCC, impedance), search patterns, force feedback or learned residual policies.

### Q: Why is tactile sensing important?
**Short answer:** Vision is occluded at contact; touch gives contact location, force and slip. **Go deeper:** GelSight/DIGIT images, e-skin; used for in-hand rotation and slip detection.

### Q: Impedance control in manipulation?
**Short answer:** Make the arm behave like a spring-damper so contact is gentle. **Go deeper:** Stiffness chosen per axis; admittance used on stiff arms.

### Q: Underactuated hands: pros and cons?
**Short answer:** Simple and adaptive but less precise and harder to model. **Go deeper:** Good for robust grasping; dexterous in-hand manipulation needs more actuation.

### Q: What are the main dexterous hands?
**Short answer:** Shadow (20 DoF), Allegro (16), LEAP (16, low cost), plus newer commercial hands. **Go deeper:** Trade-offs: tendon versus direct drive, reliability, cost, tactile coverage.

### Q: How is in-hand manipulation learned?
**Short answer:** RL in simulation with domain randomisation (Dactyl, DeXtreme), or tactile/teacher–student pipelines. **Go deeper:** Challenges: contact fidelity, reward design, partial observability.

### Q: How do you collect demonstrations for manipulation?
**Short answer:** Teleoperation (leader–follower arms, VR, gloves), handheld grippers (UMI), human video, simulation generation. **Go deeper:** Consistency and diversity matter more than count.

### Q: ACT versus Diffusion Policy?
**Short answer:** ACT predicts action chunks with a CVAE transformer; Diffusion Policy denoises action sequences. **Go deeper:** ACT is fast and works with ~50 demos; diffusion handles multimodality and precision with more inference steps.

### Q: How many demonstrations do you need?
**Short answer:** About 50 for a simple single-task policy; hundreds or more to generalise. **Go deeper:** Diversity (positions, objects, lighting) drives generalisation.

### Q: What is bimanual manipulation's special difficulty?
**Short answer:** Coordination and closed kinematic chains when both arms hold one object. **Go deeper:** Needs synchronised control and often joint action prediction (ALOHA/ACT).

### Q: Camera placement for manipulation?
**Short answer:** A wrist camera plus a fixed scene camera. **Go deeper:** Wrist view greatly helps grasping and alignment.

### Q: How do you recover from a failed grasp?
**Short answer:** Detect (gripper width, weight, vision), retreat, re-perceive, regrasp. **Go deeper:** Behavior-tree fallbacks and recovery demonstrations.

## Legged and humanoid locomotion

### Q: How does a legged robot balance?
**Short answer:** By controlling ground reaction forces and foot placement so the centre of mass stays over the support. **Go deeper:** Model-based: ZMP/DCM, centroidal MPC, WBC. Learned: RL policies on joint targets.

### Q: Model-based versus RL for locomotion?
**Short answer:** Model-based is interpretable and constraint-aware; RL gives agile robust behaviour but needs simulation and reward design. **Go deeper:** Hybrids and RL with model-based safety are common.

### Q: Typical observations and actions in an RL locomotion policy?
**Short answer:** Observations: body angular velocity, gravity direction, velocity command, joint positions/velocities, last action (+height scan). Actions: joint position targets for a PD controller. **Go deeper:** Policy ~50 Hz, PD at 200–1000 Hz.

### Q: Why do policies output position targets rather than torques?
**Short answer:** It stabilises exploration and transfers better to hardware. **Go deeper:** The PD controller acts as an implicit torque limiter.

### Q: Typical locomotion reward terms?
**Short answer:** Track commanded velocity, penalise energy, jerk, falling, reward foot air time. **Go deeper:** Weights are tuned; terminate on falls.

### Q: What is a terrain curriculum?
**Short answer:** Increasing terrain difficulty as the robot succeeds. **Go deeper:** Prevents early failure on hard terrain and speeds training.

### Q: Which parameters do you randomise for sim-to-real locomotion?
**Short answer:** Friction, payload, centre of mass, motor strength, PD gains, delay, pushes, sensor noise. **Go deeper:** Pick by sensitivity analysis; add an actuator network.

### Q: What is teacher–student training in locomotion?
**Short answer:** A teacher with privileged terrain/physics information is distilled into a student that uses only onboard sensors. **Go deeper:** RMA infers environment parameters from history.

### Q: How do humanoids recover from pushes?
**Short answer:** Ankle/hip strategies for small pushes, stepping for large ones. **Go deeper:** Capture-point control or learned recovery policies.

### Q: How are humanoid whole-body motions learned from humans?
**Short answer:** Retarget motion-capture to the robot and train an RL tracker. **Go deeper:** ExBody, H2O, OmniH2O, HumanPlus; AMP gives style priors.

### Q: What is loco-manipulation?
**Short answer:** Locomotion and manipulation together, such as walking while carrying. **Go deeper:** Needs whole-body coordination and a robust base controller under changing payloads.

### Q: State estimation for legged robots?
**Short answer:** Fuse leg kinematics (stance foot at rest), IMU and contact detection. **Go deeper:** Invariant EKF; add LiDAR/vision for drift; height maps for footstep planning.

### Q: Why are falls a design concern for humanoids?
**Short answer:** Falls damage expensive hardware. **Go deeper:** Fall detection, protective motions, torque limits and get-up policies.

### Q: Hardware issues in humanoids?
**Short answer:** Thermal limits, battery life, joint backlash and hand reliability. **Go deeper:** Quasi-direct drive, cooling and actuator modelling mitigate.

### Q: What is a gait and what gaits do quadrupeds use?
**Short answer:** A pattern of leg timing: walk, trot, pace, bound, gallop. **Go deeper:** Characterised by duty factor and phase offsets between legs.

### Q: How would you evaluate a locomotion policy on hardware?
**Short answer:** Velocity tracking error, falls per distance, cost of transport, performance across terrains and disturbances. **Go deeper:** Compare simulation and hardware logs of torques and contact timing.

## Space, soft and other

### Q: Why is manipulation in space different?
**Short answer:** The base floats so arm motion moves the satellite. **Go deeper:** Use the generalised Jacobian and plan for base reaction; no gravity to hold objects.

### Q: How do you handle large communication delay?
**Short answer:** Send goals not joystick commands and rely on onboard autonomy and verification. **Go deeper:** Rehearse in simulation; supervised autonomy.

### Q: What is a soft robot?
**Short answer:** A robot made of compliant materials. **Go deeper:** Modelled with Cosserat rods or FEM; hard to sense and control precisely.

### Q: What changes for a surgical robot?
**Short answer:** Safety and precision dominate. **Go deeper:** Remote centre of motion, tremor filtering, strict verification and regulation (IEC 60601).

### Q: What is shared autonomy?
**Short answer:** Human and robot jointly control motion. **Go deeper:** The robot infers intent and assists while the human keeps authority.
