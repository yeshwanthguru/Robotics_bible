---
title: ROS 1 (Noetic) Essentials
---

# ROS 1

ROS 1 Noetic (Ubuntu 20.04) reached EOL in May 2025, but legacy codebases and interviews still reference it.

## Architecture
- **roscore** = master (name service) + parameter server + rosout. Nodes register; peers connect directly via TCPROS (TCP) / UDPROS.
- **Topics** (pub/sub), **services**, **actions** (`actionlib`), **parameters** (`rosparam`), **bags** (`rosbag`), **nodelets** (zero-copy in a process), **tf / tf2**.
- Build: `catkin_make` / `catkin build`; `package.xml` + `CMakeLists.txt` with `find_package(catkin REQUIRED COMPONENTS ...)`, `catkin_package()`, `add_executable`, `target_link_libraries(... ${catkin_LIBRARIES})`.
- Launch: XML `.launch` with `<node>`, `<arg>`, `<param>`, `<include>`, `<remap>`, `<group ns="">`.

## Commands
```bash
roscore
rosrun pkg node             roslaunch pkg file.launch
rostopic list|echo|hz|pub   rosservice call /srv "{...}"
rosnode info /n             rosparam get/set
rosbag record -a            rosbag play --clock bag.bag
rqt_graph    rqt_console    rviz    rosrun tf view_frames
```

## Minimal node (rospy)
```python
#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
rospy.init_node('talker')
pub = rospy.Publisher('chatter', String, queue_size=10)
r = rospy.Rate(10)
while not rospy.is_shutdown():
    pub.publish('hello'); r.sleep()
```

## Key differences to articulate in interviews
Single point of failure (master), no QoS, TCP-only streaming issues over lossy Wi-Fi, no lifecycle, `rospy` GIL/threading peculiarities, `roscpp` callbacks queue with `ros::spin()`/`AsyncSpinner`, network config `ROS_MASTER_URI`/`ROS_IP`.

## Ecosystem legacy
`move_base` (global+local planner + recovery) → Nav2; `gmapping`, `hector_slam`, `amcl`; MoveIt 1; `gazebo_ros`; `ros_control`; `rosserial`; `rosbridge`.

## Migration pointers
`ros1_bridge`, rewrite `catkin→ament`, `ros::NodeHandle→rclcpp::Node`, params must be declared, services callbacks async, actionlib → native actions, nodelet → composable node, tf → tf2 only, launch → Python.
