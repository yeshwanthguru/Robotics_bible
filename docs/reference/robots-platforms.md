---
title: Robots, Hardware & Platforms Catalogue
---

# Robots, Hardware and Platforms

:::tip[How to use]
A quick catalogue of real platforms you will hear about. Specifications change with new releases, so check vendor sites for current numbers.
:::

## Robot arms

| Platform | Type | Notes |
|---|---|---|
| **Universal Robots (UR3e/5e/10e/20)** | 6-DoF collaborative arm | very common cobot; ROS drivers; force-torque on the e-series |
| **Franka Emika / Franka Research 3** | 7-DoF torque-controlled arm | research standard for manipulation learning; joint torque sensing |
| **KUKA LBR iiwa / KR series** | 7-DoF torque-sensing and industrial arms | research and industry |
| **ABB / FANUC / Yaskawa** | industrial arms | high payload, speed, repeatability |
| **xArm / Kinova Gen3 / Jaco** | lightweight arms | assistive and research use |
| **SO-100 / SO-101 (LeRobot)** | low-cost open-source arm | leader–follower teleoperation for learning |
| **ALOHA / Mobile ALOHA** | low-cost bimanual teleoperation system | popular for ACT and diffusion policies |
| **Trossen WidowX/ViperX** | hobby-research arms | used in BridgeData |

## Grippers and hands

| Platform | Type | Notes |
|---|---|---|
| **Robotiq 2F-85/140, 3F** | parallel-jaw and adaptive grippers | industrial standard |
| **Franka Hand** | parallel gripper | for Franka arms |
| **Suction (Schmalz, Piab)** | vacuum grippers | warehouse picking |
| **Shadow Dexterous Hand** | 20-DoF tendon hand | dexterity research |
| **Allegro Hand** | 16-DoF hand | RL for in-hand manipulation |
| **LEAP Hand** | low-cost 16-DoF hand | accessible dexterity research |
| **Inspire / Ability / newer commercial hands** | humanoid hands | integrated in humanoids |
| **GelSight / DIGIT / BioTac** | tactile fingertips | contact geometry and force sensing |

## Mobile robots

| Platform | Type | Notes |
|---|---|---|
| **TurtleBot 3/4** | small differential-drive robot | ROS teaching standard |
| **Clearpath Husky / Jackal** | rugged research bases | outdoor ROS research |
| **Nova Carter (NVIDIA)** | reference AMR | Isaac ROS and Nav2 |
| **Hello Robot Stretch** | mobile manipulator | home assistance research |
| **Fetch / TIAGo** | mobile manipulators | research and service |
| **Warehouse AMRs (Locus, Fetch, MiR, etc.)** | commercial fleets | Open-RMF, VDA5050 interoperability |

## Legged and humanoid

| Platform | Type | Notes |
|---|---|---|
| **Boston Dynamics Spot** | quadruped | inspection; optional arm |
| **Boston Dynamics Atlas** | humanoid | parkour (hydraulic), then electric manipulation version |
| **ANYbotics ANYmal** | quadruped | industrial inspection; ETH research heritage |
| **Unitree Go2 / B2 / G1 / H1** | quadrupeds and humanoids | affordable research platforms |
| **Agility Robotics Digit** | bipedal humanoid | logistics |
| **Figure 02 / 03** | humanoid | Helix VLA |
| **Tesla Optimus** | humanoid | in development |
| **Apptronik Apollo, 1X NEO, Fourier GR-1/GR-3, Booster T1, UBTech Walker S** | humanoids | various commercial and research programmes |
| **MIT Cheetah / Mini Cheetah** | open quadruped research platform | quasi-direct-drive legs |

## Aerial, underwater, space, medical

| Platform | Type | Notes |
|---|---|---|
| **PX4 / ArduPilot autopilots** | flight controllers | open-source drone autonomy |
| **DJI / Skydio** | commercial drones | Skydio with onboard autonomy |
| **BlueROV2** | underwater ROV | research and inspection |
| **Canadarm2 / Dextre** | space manipulators | International Space Station |
| **Astrobee** | free-flying ISS robot | research platform |
| **Perseverance / Ingenuity** | Mars rover and helicopter | autonomous navigation on Mars |
| **da Vinci** | surgical teleoperation system | robot-assisted surgery |

## Sensors (examples)

| Category | Examples |
|---|---|
| **Depth / RGB-D** | Intel RealSense, Orbbec, Stereolabs ZED, Azure Kinect (legacy) |
| **LiDAR** | Velodyne, Ouster, Hesai, Livox, Sick, Hokuyo |
| **IMU** | Xsens, VectorNav, Bosch BNO/BMI series, Epson, Analog Devices |
| **Force/torque** | ATI, Robotiq FT-300, OnRobot |
| **GNSS/RTK** | u-blox, Septentrio, Trimble |
| **Event cameras** | Prophesee, iniVation |
| **Tactile** | GelSight, DIGIT, BioTac, Xela |

## Compute and electronics

| Category | Examples |
|---|---|
| **Edge GPU** | NVIDIA Jetson Orin / Thor |
| **Real-time PCs / SBCs** | industrial x86 PCs with PREEMPT_RT, Raspberry Pi (non-RT) |
| **Microcontrollers** | STM32, ESP32, Teensy (micro-ROS) |
| **Motor drivers** | ODrive, VESC, Moteus, Maxon EPOS, ODrive-style FOC boards |
| **Fieldbus** | EtherCAT, CAN/CAN-FD, RS-485 |

## Picking a platform: questions to ask
1. What task and what payload, reach and speed? 2. Research (open, torque-controlled, ROS drivers) or product (reliable, certified)? 3. Budget and support? 4. Simulation model available (URDF/USD/MJCF) for Isaac Lab/MuJoCo? 5. Safety requirements (collaborative standards)? 6. Data and policy ecosystem (does LeRobot/openpi support it)?
