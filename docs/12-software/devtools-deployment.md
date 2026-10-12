---
title: Dev Tools, Docker, CI, Deployment
---

# Tooling for Robotics Engineering

## Linux & shell
Processes/signals, `systemd` services, `journalctl`, permissions/udev rules (serial, USB cameras), networking (`ip`, `ss`, `tcpdump`, `iperf3`, NTP/chrony/PTP time sync), `tmux`, `ssh`/`scp`/`rsync`, `ssh -L` port-forward, `htop`/`nvidia-smi`/`tegrastats`, `dmesg`, `strace`, `perf`, cgroups.

## Git
Branching (trunk-based, feature), rebase vs merge, `git bisect`, `cherry-pick`, submodules vs `vcs import` (`.repos` files), `git lfs` for models/bags, conventional commits, code review practice.

## Docker for robotics
```dockerfile
FROM ros:jazzy-ros-base
RUN apt-get update && apt-get install -y ros-jazzy-nav2-bringup python3-colcon-common-extensions && rm -rf /var/lib/apt/lists/*
WORKDIR /ws
COPY src src
RUN . /opt/ros/jazzy/setup.sh && colcon build --symlink-install
CMD ["bash","-lc",". install/setup.bash && ros2 launch my_pkg bringup.launch.py"]
```
GPU: NVIDIA Container Toolkit (`--gpus all`), X11/Wayland forwarding for rviz, `--network host` for DDS discovery, devcontainers, multi-stage builds, `docker compose`, image caching, Isaac Sim/Lab containers from NGC, Kubernetes/ k3s for fleets, Balena/ OTA.

## CI/CD
GitHub Actions: lint (`ament_lint`, clang-format, ruff), build matrix (distros), unit/integration tests (`launch_testing`), simulation-in-the-loop tests (headless Gazebo/Isaac), static analysis (clang-tidy, cppcheck), sanitizers, coverage, container publishing, hardware-in-the-loop self-hosted runners, release automation (`bloom`), docs (Doxygen/Sphinx/MkDocs/Docusaurus).

## Data & experiment infrastructure
rosbag2 (MCAP), Foxglove, LeRobot datasets (Parquet + MP4), HDF5/Zarr, W&B / MLflow, DVC, Hydra configs, TensorBoard, cloud GPU (spot instances, SLURM clusters), model registry, evaluation harnesses.

## Edge deployment
Jetson (JetPack, L4T), TensorRT engine build (`trtexec`, FP16/INT8 calibration), ONNX Runtime, Triton Inference Server, power modes (`nvpmodel`), thermal throttling, watchdog/ supervisor processes, A/B partitions for safe updates, remote logging, secure boot & SROS2, monitoring (Prometheus/Grafana).

## Design patterns & architecture
Layered architecture (hardware abstraction → skills → behaviour → mission), hexagonal ports/adapters, observer (pub/sub), state machine/ BT, factory, strategy, dependency injection, plugins (`pluginlib`), message schemas as contracts, versioning, fail-safe defaults, graceful degradation, observability (metrics/logs/traces).

## Interview Q&A

**How structure a robot software stack?** Drivers → state estimation → perception → planning → control, with lifecycle management, diagnostics, and a safety supervisor independent of AI components.

**Why host networking for ROS 2 in Docker?** DDS multicast discovery doesn't traverse bridge networks easily.

**How to test robot code without hardware?** Unit tests with mocks, simulation (headless), rosbag replay, HIL for final validation.
