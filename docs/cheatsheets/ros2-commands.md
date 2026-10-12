---
title: ROS 2 / Isaac / Docker Command Cheat Sheet
---

# Commands

## ROS 2
```bash
ros2 run <pkg> <exe>              ros2 launch <pkg> <file.launch.py> arg:=val
ros2 node list|info /n            ros2 topic list|echo|hz|bw|info -v|pub /t type "{...}"
ros2 service list|call /s type "{}"   ros2 action list|send_goal /a type "{}" --feedback
ros2 param list|get|set|dump /n   ros2 interface show std_msgs/msg/String
ros2 bag record -a -s mcap        ros2 bag play bag --clock
ros2 doctor --report              ros2 lifecycle set /n configure|activate
ros2 control list_controllers     ros2 run tf2_ros tf2_echo map base_link
ros2 run tf2_tools view_frames    rqt_graph    rviz2
colcon build --symlink-install --packages-select X --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo
colcon test --packages-select X && colcon test-result --verbose
rosdep install --from-paths src -y --ignore-src
export ROS_DOMAIN_ID=7 RMW_IMPLEMENTATION=rmw_cyclonedds_cpp ROS_LOCALHOST_ONLY=0
```

## Isaac Lab
```bash
./isaaclab.sh -p scripts/environments/list_envs.py
./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/train.py --task <ID> --num_envs 4096 --headless [--video] [--seed 1]
./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/play.py --task <ID> --num_envs 32 --checkpoint path.pt
tensorboard --logdir logs/
```

## Docker / GPU
```bash
docker run --rm -it --gpus all --network host -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix image
nvidia-smi -l 1      tegrastats (Jetson)      nvpmodel -m 0 ; jetson_clocks
```

## Git
```bash
git switch -c feat/x ; git rebase -i HEAD~3 ; git bisect start/good/bad ; git stash -u ; git worktree add ../w branch
```

## Debug
`gdb -ex run --args`, `valgrind --leak-check=full`, `perf top`, `strace -f -p PID`, `ros2 run --prefix 'gdb -ex run --args' pkg exe`, ASAN: `-fsanitize=address,undefined`.
