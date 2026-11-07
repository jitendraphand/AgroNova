"""ROS 2 node: /cmd_vel -> wheel speed targets; wheel speeds -> /odom."""
import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

from agronova_kinematics.diff_drive import DiffDriveParams, forward, integrate_odometry, inverse


class DiffDriveNode(Node):
    def __init__(self):
        super().__init__("diff_drive")
        self.declare_parameter("wheel_radius", 0.10)
        self.declare_parameter("track_width", 0.50)
        self.p = DiffDriveParams(
            self.get_parameter("wheel_radius").value, self.get_parameter("track_width").value
        )
        self.pose = [0.0, 0.0, 0.0]
        self.cmd_pub = self.create_publisher(Float64MultiArray, "wheel_cmd", 10)
        self.odom_pub = self.create_publisher(Odometry, "odom", 10)
        self.create_subscription(Twist, "cmd_vel", self.on_cmd, 10)
        self.create_subscription(Float64MultiArray, "wheel_state", self.on_state, 10)
        self.last = None

    def on_cmd(self, msg: Twist):
        wl, wr = inverse(msg.linear.x, msg.angular.z, self.p)
        self.cmd_pub.publish(Float64MultiArray(data=[wl, wr]))

    def on_state(self, msg: Float64MultiArray):
        now = self.get_clock().now()
        if self.last is not None and len(msg.data) >= 2:
            dt = (now - self.last).nanoseconds * 1e-9
            v, w = forward(msg.data[0], msg.data[1], self.p)
            self.pose = list(integrate_odometry(*self.pose, v, w, dt))
            o = Odometry()
            o.header.stamp = now.to_msg()
            o.header.frame_id, o.child_frame_id = "odom", "base_link"
            o.pose.pose.position.x, o.pose.pose.position.y = self.pose[0], self.pose[1]
            import math
            o.pose.pose.orientation.z = math.sin(self.pose[2] / 2)
            o.pose.pose.orientation.w = math.cos(self.pose[2] / 2)
            o.twist.twist.linear.x, o.twist.twist.angular.z = v, w
            self.odom_pub.publish(o)
        self.last = now


def main():
    rclpy.init()
    rclpy.spin(DiffDriveNode())
    rclpy.shutdown()
