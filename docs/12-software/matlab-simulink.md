---
title: MATLAB & Simulink for Robotics
---

# MATLAB / Simulink

## Why it shows up
Prototyping control, estimation, dynamics, signal processing; Simulink model-based design with code generation to embedded/ROS; used heavily in academia and aerospace/automotive. Toolboxes: **Robotics System Toolbox** (rigidBodyTree, IK, trajectory, ROS/ROS2 integration, Gazebo co-sim), **Navigation Toolbox** (SLAM, AMCL, planners), **Control System Toolbox**, **Optimization**, **Model Predictive Control Toolbox**, **Simscape Multibody**, **Computer Vision**, **Deep Learning**, **Reinforcement Learning Toolbox**, **Sensor Fusion & Tracking**, **UAV Toolbox**, **Symbolic Math**, **Parallel Computing**, **MATLAB Coder / Embedded Coder / GPU Coder**.

## Language essentials
- 1-based indexing, column-major, matrices are default type; vectorization over loops; `.*` element-wise vs `*` matrix product; `A\b` solves linear systems (QR/LU); `end`, logical indexing `x(x>0)`; `cellfun/arrayfun`; structs, tables, function handles `@(x)`, `containers.Map`; implicit expansion (broadcasting).
- Pre-allocate arrays (`zeros(n,1)`) to avoid growth cost; `tic/toc`, Profiler.

## Examples
```matlab
% Forward kinematics + IK with Robotics System Toolbox
robot = loadrobot("universalUR5e", DataFormat="column");
ik = inverseKinematics(RigidBodyTree=robot);
tform = trvec2tform([0.4 0.2 0.5]) * eul2tform([0 pi 0]);
[cfg, info] = ik("tool0", tform, ones(1,6), homeConfiguration(robot));

% Kalman filter
F=[1 dt;0 1]; H=[1 0]; Q=0.01*eye(2); R=0.1;
x=[0;0]; P=eye(2);
for k=1:N
    x=F*x; P=F*P*F'+Q;
    K=P*H'/(H*P*H'+R);
    x=x+K*(z(k)-H*x); P=(eye(2)-K*H)*P;
end

% LQR
A=[0 1;0 -0.1]; B=[0;1];
[K,S,e] = lqr(A,B,diag([10 1]),0.1);

% ODE simulation
f=@(t,x)[x(2); -9.81/L*sin(x(1))];
[t,x]=ode45(f,[0 10],[0.5;0]);
```

## ROS from MATLAB
```matlab
node = ros2node("/matlab_node");
sub = ros2subscriber(node,"/scan","sensor_msgs/LaserScan",@(m) disp(numel(m.ranges)));
pub = ros2publisher(node,"/cmd_vel","geometry_msgs/Twist");
msg = ros2message(pub); msg.linear.x = 0.2; send(pub,msg);
```
Simulink ROS blocks (Subscribe/Publish/Call Service), generate C++ ROS node via Embedded Coder (`rosgenmsg`, `roscodegen`), deploy to remote Linux/Jetson.

## Simulink / model-based design
Continuous/discrete solvers (fixed-step for codegen, ode45/ode15s variable), Stateflow (state machines), Simscape (physical networks), signal buses, S-Functions, HIL/SIL/PIL testing, requirements traceability (ISO 26262/DO-178C workflows), Simulink Test.

## MATLAB vs Python
| | MATLAB | Python |
|---|---|---|
| Cost | licensed | free |
| Toolbox depth for control/sim | excellent, integrated | scattered but growing |
| Deep learning / LLM ecosystem | smaller | dominant |
| Code generation to embedded | Embedded Coder (mature) | limited |
| Deployment at scale | harder | easy (Docker, cloud) |
`matlab.engine` lets Python call MATLAB; `scipy.io.loadmat` reads .mat files.

## Interview Q&A

**`A\b` vs `inv(A)*b`?** Backslash uses factorization, more accurate/faster, handles least squares.

**Why fixed-step solver for code generation?** Deterministic real-time execution.

**How do you validate a controller before hardware?** MIL → SIL → PIL → HIL pipeline.

**Convert quaternion order in MATLAB?** Robotics Toolbox uses `[w x y z]`, ROS uses `[x y z w]` — classic bug.
