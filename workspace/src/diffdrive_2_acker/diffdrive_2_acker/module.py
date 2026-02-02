#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from math import atan, tan
from geometry_msgs.msg import Twist


class DiffDriveConverter(Node):
    def __init__(self):
        super().__init__('diff_converter')

        # Declare parameters for robot settings with default values
        self.declare_parameter('wheelbase', 0.5)
        self.declare_parameter('max_steering_angle', 45*(2*math.pi)/360)  # 45 deg
        self.declare_parameter('max_angular_velocity', 10.0)

        self.wheelbase = float(self.get_parameter('wheelbase').value)
        self.max_steering_angle = float(self.get_parameter('max_steering_angle').value)
        self.max_angular_velocity = float(self.get_parameter('max_angular_velocity').value)

        # minimum turning radius derived from maximum steering angle: R = L / tan(delta)
        self.min_turning_radius = (self.wheelbase / tan(self.max_steering_angle)
                                   if abs(tan(self.max_steering_angle)) > 1e-6 else float('inf'))

        # Publisher for ackermann commands on 'cmd_vel' topic which is used by the hunter_se robot
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)

        # Subscriber for differential drive commands on 'twist_angle' topic
        self.sub = self.create_subscription(Twist, 'twist_angle', self.diffdrive_callback, 10)

        self.get_logger().info(f'Initialized DiffDriveConverter L={self.wheelbase} max_delta={self.max_steering_angle}')

    def diffdrive_callback(self, twist_angle_msg):
        """Callback function to convert diff drive commands to ackermann commands """
        # Extract linear and angular velocities from the incoming message according to convention
        v = float(twist_angle_msg.linear.x)
        w = float(twist_angle_msg.angular.z)

        # Convert to ackermann commands
        v_out, delta = self.convert2acker(v, w)

        # Publish the converted command
        msg = Twist()
        msg.linear.x = v_out
        msg.angular.z = delta
        self.pub.publish(msg)

    def convert2acker(self, v, w):
        """Convert differential drive commands (v, w) to ackermann commands (v, delta)"""
        # Clamp angular velocity to max limits
        w = max(min(w, self.max_angular_velocity), -self.max_angular_velocity)

        # Handle straight motion case (prevent division by zero)
        if abs(w) < 1e-6:
            return v, 0.0

        # Calculate turning radius
        R = v / w

        # Handle small turning radius case
        if abs(R) < self.min_turning_radius:
            R = self.min_turning_radius if R > 0 else -self.min_turning_radius
            v = R * w   # adjust linear velocity according to desired angular velocity

        # Calculate steering angle delta
        delta = atan(self.wheelbase / R)
        delta = max(min(delta, self.max_steering_angle), -self.max_steering_angle)

        return v, delta


def main(args=None):
    """Main function to initialize the node and spin."""
    rclpy.init(args=args)
    node = DiffDriveConverter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()