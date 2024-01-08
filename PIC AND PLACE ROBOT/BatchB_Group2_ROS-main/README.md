# BatchB_Group2_ROS
**DESCRIPTION:**
This project begins with the idea of designing a pick and place robot that can do obstacle avoidance within a stipulated world filled with walls. Additionally a rover capable of performing mapping and navigating itself through the map is made.


**System and packages required:**
All these packages are created and tested through Ubuntu 22.04 with ROS 2 humble 
Gazebo is used for stimulating the files
Rviz is used for visualization

**BUILD AND RUN OBSTACLE AVOIDANCE***
After creating packages using mkdir and having pasted the src folder above, running these codes will work;

~~~
jd@jd-virtual-machine:~/workspace$ colcon build
d@jd-virtual-machine:~/workspace$ source install/setup.bash 
jd@jd-virtual-machine:~/workspace$ ros2 launch mobile_arm_gripper_spawner_pkg gazebo_world.launch.py 
~~~

After running this, thw world with robot is launched, then run this

~~~
jd@jd-virtual-machine:~/workspace$ colcon build
d@jd-virtual-machine:~/workspace$ source install/setup.bash
jd@jd-virtual-machine:~/workspace$ ros2 launch warehouse_robot_controller_pkg controller_estimator.launch.py 

~~~

After running this the robot starts moving and it will automatically avoid obstacles,i.e walls in our world.




https://github.com/Jaidev04/BatchB_Group2_ROS/assets/95011033/60347135-60f1-4a31-bd86-e50988647e79



**MAPPING AND NAVIGATION OF MOBILE ROBOT**

*MAPPING*
~~~
source ~/rover_ws/install/setup.bash
ros2 launch rover launch_sim.launch.py world:=./src/rover/worlds/obstacles.world
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=./src/rover/config/mapper_params_online_async.yaml use_sim_time:=true
rviz2 -d src/rover/config/mapping.rviz
ros2 run teleop_twist_keyboard teleop_twist_keyboard -r /cmd_vel:=/diff_cont/cmd_vel_unstamped
~~~

https://github.com/Jaidev04/BatchB_Group2_ROS/assets/95011033/b1c4a355-ebfa-47a0-980c-531b8b76f4dd

*NAVIAGATION*
~~~
cd ~/rover_ws && source ~/rover_ws/install/setup.bash
ros2 launch rover launch_sim.launch.py world:=./src/rover/worlds/obstacles.world
rviz2 -d src/rover/config/navigation.rviz
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=./src/rover/config/mapper_params_online_async.yaml use_sim_time:=true
~~~




![image](https://github.com/Jaidev04/BatchB_Group2_ROS/assets/95011033/7c231f8d-3799-44a1-8fa9-ad7be38ba384)

FOR THE PICK AND PLACE ROBOT, TO RUN THE ROBOT
~~~
ccolcon build
source install/setup.bash
ros2 launch pick_place rsp_sim_launch.py
ros2 run pick_place rsp.launch.py
~~~
![image](https://github.com/Jaidev04/BatchB_Group2_ROS/assets/95011033/30ab7cfd-ffeb-4f97-95c5-50a39c077a24)



