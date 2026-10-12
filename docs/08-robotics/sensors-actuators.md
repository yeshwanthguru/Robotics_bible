---
title: Sensors, Actuators, Hardware
---

# Sensors, Actuators & Hardware

:::tip[The 30-second version]
A robot is **senses + brain + muscles**. Sensors tell it about the world (*exteroceptive*: cameras, LiDAR) and about itself (*proprioceptive*: joint angles, IMU, motor current). Every sensor lies a little in its own way, so robots **fuse several sensors** to get one trustworthy picture.
:::

![sensors overview](/img/fig/sensors-overview.svg)
*The usual sensor suite and what each is good at.*

## Sensing the robot itself (proprioceptive)

| Sensor | Measures | Gotchas |
|---|---|---|
| **Encoders** (optical / magnetic, absolute) | joint or wheel angle | resolution; absolute encoders avoid "homing" |
| **IMU** (gyro + accelerometer, ± magnetometer) | rotation rate and acceleration | **drifts**: integrating a biased accelerometer gives position error growing with time² |
| **Motor current / torque sensors** | effort | current only estimates torque (friction!) |
| **6-axis force/torque sensor** | push and twist at a wrist or ankle | key for contact and compliant control |
| **Foot / contact sensors** | is the foot on the ground? | legged state estimation |

## Sensing the world (exteroceptive)

| Sensor | How it works | Strengths | Weaknesses |
|---|---|---|---|
| **RGB camera** | light intensity | rich semantics, cheap | no direct depth, lighting-sensitive |
| **Stereo camera** | triangulate two views: depth $Z=fB/d$ | passive, long range | fails on blank surfaces |
| **RGB-D (ToF / structured light)** | measures depth actively | dense indoors | sunlight, shiny things |
| **LiDAR** | laser time-of-flight | accurate geometry | cost, glass, rain |
| **Radar (mmWave)** | radio + Doppler | all-weather, velocity | low resolution |
| **Ultrasonic** | sound echo | cheap | wide beam |
| **Event camera** | per-pixel brightness *changes* | microsecond latency, HDR | needs special algorithms |
| **Thermal** | infrared | night, search & rescue | low resolution |
| **GNSS / RTK, UWB** | satellite / radio ranging | global position | multipath, indoors |
| **Tactile (GelSight, DIGIT, e-skin)** | contact image / pressure | slip and shape for dexterity | fragile, calibration |

**Calibration is half the job:** camera intrinsics (focal length, centre, distortion), extrinsics (where each sensor sits on the body), hand–eye, and **time synchronisation** (PTP/hardware triggers). A bad calibration or a 30 ms timing offset is a top cause of "the algorithm works in sim but not on the robot".

## Actuators (muscles)

See the table in [Dynamics](./dynamics.md). In short: BLDC motors with field-oriented control, harmonic or planetary gearboxes, quasi-direct drive for legs, series-elastic for safe force control, tendons for hands, and hydraulics for raw power.

**Nested control loops** run from tens of kHz (motor current) up to a few Hz (high-level AI): see [Control](../10-planning-control/control.md).

## Compute, communication and safety

| Topic | Notes |
|---|---|
| **Compute** | microcontrollers (real-time, micro-ROS), edge GPU (Jetson Orin/Thor), x86 real-time PC |
| **Buses** | **CAN / CAN-FD**, **EtherCAT** (deterministic, ~1 kHz for many axes), USB, Ethernet/TSN |
| **Power** | Li-ion / LiFePO₄, battery management, regenerative braking, brown-out protection |
| **Safety standards** | ISO 10218 (industrial robots), ISO/TS 15066 (collaborative), ISO 13482 (personal care), ISO 26262 (automotive) |
| **Safety functions** | e-stop, safe torque off, speed-and-separation monitoring, power and force limiting |

## Interview Q&A

**Why does an IMU drift?**
*Simply:* tiny biases get integrated, and double integration makes position error grow quickly. *Fix:* fuse with vision, LiDAR or GNSS using an EKF or factor graph.

**Why is EtherCAT popular in robots?**
*Simply:* deterministic, low-jitter communication for many motors at ~1 kHz.

**When would you pick an event camera?**
*Simply:* very fast motion or extreme lighting; not for static scenes.

**Rolling vs global shutter?**
*Simply:* rolling-shutter cameras read rows at different times, which distorts fast motion; global shutter exposes all at once and is better for visual-inertial odometry.

**Proprioceptive vs exteroceptive?**
*Simply:* sensing the robot's own body versus sensing the outside world.
