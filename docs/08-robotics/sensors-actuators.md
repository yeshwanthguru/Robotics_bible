---
title: Sensors, Actuators, Hardware
---

# Sensors, Actuators & Hardware

## Proprioceptive
| Sensor | Measures | Notes |
|---|---|---|
| Encoders (incremental/absolute, magnetic, optical) | joint angle | resolution, quantization; absolute avoids homing |
| IMU (gyro + accel [+mag]) | ω, specific force | bias random walk, noise density, temperature drift; integrate carefully; MEMS vs FOG |
| Joint torque / current sensing | τ | strain gauge or motor current estimate |
| 6-axis F/T sensor | wrench at wrist/ankle | key to force control, contact detection |
| Foot/contact sensors | contact state | legged state estimation |

## Exteroceptive
| Sensor | Principle | Strengths / weaknesses |
|---|---|---|
| RGB camera | intensity | rich semantics; lighting, no scale |
| Stereo | triangulation $Z=fB/d$ | passive depth; textureless fail |
| ToF / structured light (RealSense, Kinect, Orbbec) | active depth | indoor, sun interference |
| **LiDAR** (spinning, solid-state, FMCW) | ranging | accurate geometry; cost, rain/glass |
| Radar (mmWave) | Doppler | all-weather, velocity; low resolution |
| Sonar/ultrasonic | acoustic | cheap, wide beam |
| Event camera | async brightness change | µs latency, HDR; needs special algorithms |
| Thermal | IR | night, SAR |
| GNSS/RTK, UWB | global position | outdoors cm-level (RTK); multipath |
| Tactile (GelSight/DIGIT, BioTac, e-skin, taxels) | contact geometry/force | dexterity, slip detection |
| Microphone arrays | audio | speech, localization |

**Calibration:** camera intrinsics $K=\begin{pmatrix}f_x&0&c_x\\0&f_y&c_y\\0&0&1\end{pmatrix}$ + distortion (checkerboard/Kalibr), extrinsics (camera–LiDAR, camera–IMU), hand–eye, time sync (PTP/hardware trigger). Mis-calibration is a top real-world failure.

## Actuators
| Type | Pros | Cons |
|---|---|---|
| BLDC/PMSM + FOC | efficient, high torque density | needs driver & encoder |
| Harmonic drive | zero-backlash, compact | friction, compliance |
| Planetary / cycloidal / QDD | backdrivable, robust | lower torque density |
| SEA / VSA | force control, safe, energy storage | bandwidth |
| Hydraulic | highest power density | leaks, noise |
| Pneumatic / soft | compliant, light | hard to control |
| Tendon-driven | remote actuation (hands) | friction, stretch |
| Piezo / SMA / EAP | tiny, precise | niche |

Control loops: current (≈10–40 kHz) → velocity (~kHz) → position/torque (1 kHz) → whole-body/MPC (100–500 Hz) → planner (10 Hz) → VLM (1–10 Hz).

## Compute & communication
MCU (STM32, real-time, micro-ROS), SBC (RPi), edge GPU (Jetson Orin/Thor), x86 RT PC; buses: **CAN/CAN-FD, EtherCAT** (deterministic, ≤µs jitter), RS485, USB, Ethernet/TSN, SPI/I²C; wireless: Wi-Fi 6, 5G, mesh. Power: battery chemistry (Li-ion/LiFePO₄), BMS, regenerative braking, brown-out protection. Safety: e-stop, STO, ISO 10218 / ISO 13482 / ISO 26262, speed & separation monitoring, power & force limiting (ISO/TS 15066 collaborative).

## Interview Q&A

**IMU drift?** Double-integrating accelerometer bias gives quadratic position error; fuse with vision/LiDAR/GNSS (EKF/factor graph).

**Why EtherCAT?** Deterministic cycle with distributed clocks, 1 kHz+ for many axes.

**Event camera use cases?** High-speed tracking, HDR, low-power; not good for static scenes.

**Rolling vs global shutter?** Rolling causes distortion under motion; important for VIO — calibrate readout time or use global shutter.
