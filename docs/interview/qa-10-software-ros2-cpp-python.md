---
title: "Q&A 10: Software (ROS 2, C++, Python, MATLAB, R, PDDL, DevOps)"
---

# Interview Q&A: Robotics Software

:::tip[How to use]
Chapters: [ROS 2](../12-software/ros2.md) · [ROS 1](../12-software/ros1.md) · [C++](../12-software/cpp-for-robotics.md) · [Python](../12-software/python-for-robotics.md) · [MATLAB](../12-software/matlab-simulink.md) · [R](../12-software/r-for-robotics-stats.md) · [Dev tools](../12-software/devtools-deployment.md).
:::

## ROS 2

### Q: What is ROS 2 and why was it created?
**Short answer:** Middleware and tools for robot software, redesigned with DDS, QoS and real-time/security support. **Go deeper:** ROS 1's central master was a single point of failure with no QoS or real-time story.

### Q: Topic versus service versus action?
**Short answer:** A topic streams data many-to-many; a service is request/response; an action is a long-running goal with feedback and cancel. **Go deeper:** Actions are built on topics and services.

### Q: Explain QoS and common incompatibilities.
**Short answer:** QoS sets delivery rules (reliability, durability, history, deadline). **Go deeper:** A reliable subscriber can't match a best-effort publisher; `/map` and `/tf_static` use transient-local durability; check with `ros2 topic info -v`.

### Q: Why can't my subscriber see a topic?
**Short answer:** Usually QoS mismatch, different ROS_DOMAIN_ID, namespaces/remaps or blocked multicast. **Go deeper:** Check RMW implementation and `use_sim_time` too.

### Q: What is a lifecycle node?
**Short answer:** A node with managed states (unconfigured, inactive, active, finalised). **Go deeper:** Gives deterministic bring-up; Nav2 uses a lifecycle manager.

### Q: What are executors and callback groups?
**Short answer:** Executors schedule callbacks; callback groups decide which may run concurrently. **Go deeper:** Use reentrant groups with a multi-threaded executor when a callback calls a service to avoid deadlock.

### Q: What is composition?
**Short answer:** Running several nodes in one process for intra-process zero-copy transport. **Go deeper:** Use composable nodes and `unique_ptr` messages.

### Q: How does TF2 work and what is the classic error?
**Short answer:** It stores a tree of timestamped transforms. **Go deeper:** "Extrapolation into the future" means timestamps/clock mismatch; fix use_sim_time, waitForTransform timeouts, and publication rates.

### Q: What is ros2_control?
**Short answer:** A real-time framework with hardware interfaces and controllers. **Go deeper:** Controller manager loop at e.g. 1 kHz; controllers claim command/state interfaces exclusively.

### Q: How do you make ROS 2 real-time?
**Short answer:** PREEMPT_RT kernel, SCHED_FIFO, memory locking, pre-allocation, static executor, no dynamic allocation in the loop. **Go deeper:** Keep the RT loop in ros2_control or a dedicated thread.

### Q: Which middleware options exist?
**Short answer:** Fast DDS, Cyclone DDS, Connext, and Zenoh. **Go deeper:** Choose by performance, discovery behaviour and ecosystem; set `RMW_IMPLEMENTATION`.

### Q: How do you record and replay data?
**Short answer:** `ros2 bag record` (MCAP) and `ros2 bag play --clock`. **Go deeper:** Use sim time; visualise in Foxglove.

### Q: How do you debug a ROS 2 system?
**Short answer:** `ros2 doctor`, topic hz/echo/info, `view_frames`, rqt_graph, bag replay, gdb, tracing. **Go deeper:** `ros2_tracing` for latency analysis.

### Q: ROS 1 to ROS 2 migration?
**Short answer:** Use ros1_bridge for staged migration, port packages and launch files, redesign for composition and lifecycle. **Go deeper:** catkin→ament, `rospy`→`rclpy`, actionlib→native actions.

### Q: What is a URDF and what are Xacro and SRDF?
**Short answer:** URDF describes links, joints and inertia; Xacro adds macros; SRDF adds planning groups and collision pairs for MoveIt. **Go deeper:** `robot_state_publisher` turns URDF + joint states into TF.

## C++

### Q: What is RAII?
**Short answer:** A resource's lifetime is tied to an object's scope. **Go deeper:** Smart pointers, lock guards and file handles release automatically even on exceptions.

### Q: unique_ptr versus shared_ptr versus weak_ptr?
**Short answer:** unique_ptr is sole ownership, shared_ptr is shared reference-counted ownership, weak_ptr observes without owning. **Go deeper:** Use weak_ptr to break cycles; shared_ptr has atomic-count overhead.

### Q: What is move semantics?
**Short answer:** Transferring resources instead of copying. **Go deeper:** `std::move` is a cast to rvalue; the move constructor does the work; rule of 0/3/5.

### Q: Why a virtual destructor?
**Short answer:** Deleting a derived object through a base pointer is undefined without it. **Go deeper:** Also mark overrides `override`/`final`.

### Q: What is undefined behaviour? Examples?
**Short answer:** Code the standard doesn't define, so anything can happen. **Go deeper:** Dangling references, signed overflow, data races, out-of-bounds access, uninitialised reads.

### Q: Data race versus race condition?
**Short answer:** A data race is unsynchronised conflicting access (undefined); a race condition is timing-dependent behaviour. **Go deeper:** Use mutexes or atomics.

### Q: Explain memory orders (acquire/release).
**Short answer:** A release store publishes earlier writes; an acquire load observes them. **Go deeper:** Use them for lock-free queues; relaxed ordering gives no synchronisation.

### Q: How do you write real-time-safe C++?
**Short answer:** No allocation, exceptions or blocking locks in the loop; pre-allocate; pin threads. **Go deeper:** Lock-free SPSC queues, `std::pmr`, bounded loops.

### Q: Why are Eigen alignment issues a thing?
**Short answer:** Fixed-size vectorisable types need aligned memory. **Go deeper:** Use `EIGEN_MAKE_ALIGNED_OPERATOR_NEW` or C++17 aligned new; avoid by-value passing.

### Q: What do CMake's PUBLIC, PRIVATE and INTERFACE mean?
**Short answer:** Whether dependencies are used by the target, its consumers, or both. **Go deeper:** Use targets rather than raw variables.

### Q: `vector::reserve` versus `resize`?
**Short answer:** reserve allocates capacity; resize changes size and constructs elements. **Go deeper:** Reserve avoids reallocations in hot paths.

### Q: What is `constexpr` for?
**Short answer:** Computing values at compile time. **Go deeper:** C++20 `consteval` forces it; useful for tables and templates.

### Q: What tools find C++ bugs?
**Short answer:** Sanitizers (ASan, UBSan, TSan), valgrind, clang-tidy, cppcheck, gdb. **Go deeper:** Run sanitizer builds in CI.

## Python

### Q: What is the GIL and what does it affect?
**Short answer:** Only one thread executes Python bytecode at a time. **Go deeper:** Threads help I/O-bound work; use multiprocessing or native extensions for CPU-bound work; free-threaded builds are emerging.

### Q: Why vectorise with NumPy?
**Short answer:** Loops run in C with SIMD, far faster than Python loops. **Go deeper:** Broadcasting avoids explicit loops; JIT with Numba/JAX otherwise.

### Q: List versus tuple versus set versus dict?
**Short answer:** Mutable ordered, immutable ordered, unique unordered, key-value (insertion-ordered). **Go deeper:** Sets and dicts use hashing for O(1) average lookup.

### Q: What are generators for?
**Short answer:** Lazy iteration with O(1) memory. **Go deeper:** Good for streaming sensor data and datasets.

### Q: Shallow versus deep copy?
**Short answer:** Shallow copies references; deep copies recursively. **Go deeper:** NumPy views share memory; use `.copy()`; PyTorch uses `.clone()`.

### Q: How do you avoid blocking in rclpy callbacks?
**Short answer:** Keep callbacks short and offload heavy work to threads/processes or async futures. **Go deeper:** Use callback groups and multi-threaded executors.

### Q: Typical quaternion convention gotchas?
**Short answer:** ROS and SciPy use (x, y, z, w); Eigen's constructor and MATLAB use (w, x, y, z). **Go deeper:** Always check when converting between libraries.

## MATLAB, R, PDDL, DevOps

### Q: MATLAB versus Python for control work?
**Short answer:** MATLAB has integrated control toolboxes, Simulink and code generation; Python dominates ML and deployment. **Go deeper:** `matlab.engine` bridges them.

### Q: `A\b` versus `inv(A)*b` in MATLAB?
**Short answer:** Backslash is faster and more accurate and also handles least squares. **Go deeper:** It uses factorisation; avoid explicit inverses.

### Q: What is Simulink code generation for?
**Short answer:** Turning models into C/C++ for embedded targets or ROS nodes. **Go deeper:** Use fixed-step solvers and MIL/SIL/HIL testing.

### Q: Why use R in robotics?
**Short answer:** Statistics and publication-quality plots for trial data. **Go deeper:** Mixed-effects models (lme4), survival analysis, ggplot2.

### Q: Why mixed-effects models for robot trials?
**Short answer:** Trials grouped by operator or object are not independent. **Go deeper:** Random effects model that grouping.

### Q: What does PDDL describe?
**Short answer:** Planning domains and problems with actions, preconditions and effects. **Go deeper:** See the PDDL chapter and Fast Downward usage.

### Q: Why Docker for robotics?
**Short answer:** Reproducible environments across machines. **Go deeper:** Use `--network host` for DDS discovery and the NVIDIA container toolkit for GPUs.

### Q: How would you test robot code without hardware?
**Short answer:** Unit tests with mocks, simulation (headless), bag replay, then HIL. **Go deeper:** Run in CI with `launch_testing`.

### Q: Describe a CI pipeline for a ROS 2 repo.
**Short answer:** Lint, build on target distros, unit and launch tests, sanitizers, simulation tests, container publish. **Go deeper:** Cache dependencies; self-hosted runners for hardware.

### Q: How do you structure a robot software stack?
**Short answer:** Drivers → state estimation → perception → planning → control, with lifecycle management, diagnostics and an independent safety supervisor. **Go deeper:** Keep AI components behind well-defined interfaces and monitors.
