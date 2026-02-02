# ROS2 Coding Challenge

This repo contains a small coding challenge in which a conversion node is created to convert commands for a differential drive robot to Ackermann steering commands.

## Quick Start

### Build and source the workspace
```bash
colcon build && source intstall/setup.bash
```

### Install diffdrive_2_acker systemd service
To have the diffdrive to Ackermann converter start automatically on boot:
```bash
sudo /workspace/install_systemd_service.sh
```

This enables the `diffdrive_2_acker` service to run automatically in the background.

---

## Differential Drive Conversion Node

The challenge in the conversion of the commands arises when trying to handle any commands that require a smaller turning radius than the minimum turning radius of the robot since the Ackermann system cannot rotate around its own axis. Ideally this would be handled by implementing a u-turn method which would make the robot move back and forward while rotating the wheel angles from one extreme to the other and thus emulating a rotation around its own axis as close as possible while mostly staying in one point in space. However, this approach would require a history of commands, tracking the distance driven or at least tracking the time between the command changes and would also have to handle sudden changes in the input from the user. 

Therefore I opted for the simpler approach of turning the robot with the maximum steering angle while still moving forwards. Thus a rotation around its own axis is converted into a tight circle. This is suboptimal since it could lead to obstacle collisions. Another approach would be to halt robot movement completely in case the minimum turning radius is surpassed, however this could lead to deadlocks if the control algorithm does not consider this limitation.

My implementation is not able to do turns that are thighter than the minimum vehicle turning radius. In an attempt to vaguely adhere to the angular velocity under tight radii, I scaled the turning velocity by the desired angular velocity. In my implementation I assumed that the maximum steering angle is 45 degrees, the maximum angular velocity it 10 rad/s and the wheelbase is 0.5 meters. These parameters can however be changed when  starting the node via the ros parameters. Finally, I assumed that it is acceptable to adhere to the trajectory within a deviation approximately equal to twice the minimum turning radius (which is the worst case scenario when the robot should rotate around its own axis but in fact rotates around the minimum turning radius circle)

As for the automatic systemd service installation, I decided to create a separate script that can be executed in order to install and start the service since it has to be run with sudo rights anyways, differently from the package build.