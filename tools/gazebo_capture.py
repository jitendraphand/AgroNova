#!/usr/bin/env python3
"""ROS 2 node: drive AgroNova in the running Gazebo sim and save real Gazebo camera frames + logs.

Run (after `ros2 launch agronova_gazebo sim.launch.py world:=cotton_field_capture.sdf headless:=true`):
    python3 tools/gazebo_capture.py --out docs/media/gazebo --seconds 16
Saves: overview_XX.png / top_XX.png (Gazebo ogre2 renders), run_log.npz (odom trace + last scan).
"""
import argparse
import math
import time
from pathlib import Path

import numpy as np
import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from PIL import Image as PILImage
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image, LaserScan


class Capture(Node):
    def __init__(self, out, seconds):
        super().__init__("agronova_capture")
        self.out, self.seconds = Path(out), seconds
        self.out.mkdir(parents=True, exist_ok=True)
        self.latest = {}
        self.odom, self.scan = [], None
        for t in ("overview_camera", "top_camera"):
            self.create_subscription(Image, t, lambda m, t=t: self.latest.__setitem__(t, m), qos_profile_sensor_data)
        self.create_subscription(Odometry, "wheel/odom", self.on_odom, 10)
        self.create_subscription(LaserScan, "scan", lambda m: setattr(self, "scan", m), qos_profile_sensor_data)
        self.pub = self.create_publisher(Twist, "cmd_vel", 10)

    def on_odom(self, m):
        q = m.pose.pose.orientation
        yaw = math.atan2(2 * (q.w * q.z + q.x * q.y), 1 - 2 * (q.y * q.y + q.z * q.z))
        self.odom.append((m.header.stamp.sec + m.header.stamp.nanosec * 1e-9, m.pose.pose.position.x,
                          m.pose.pose.position.y, yaw))

    def save(self, topic, name):
        m = self.latest.get(topic)
        if m is None:
            return False
        arr = np.frombuffer(bytes(m.data), np.uint8).reshape(m.height, m.width, -1)[:, :, :3]
        PILImage.fromarray(arr).save(self.out / name)
        return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="docs/media/gazebo")
    ap.add_argument("--seconds", type=float, default=16.0)
    ap.add_argument("--speed", type=float, default=0.5)
    a = ap.parse_args()
    rclpy.init()
    n = Capture(a.out, a.seconds)
    t0 = time.time()
    while "overview_camera" not in n.latest and time.time() - t0 < 120:
        rclpy.spin_once(n, timeout_sec=0.1)
    n.save("overview_camera", "overview_00_start.png")
    n.save("top_camera", "top_00_start.png")
    t0, k = time.time(), 1
    while time.time() - t0 < a.seconds:
        tw = Twist()
        tw.linear.x = a.speed
        n.pub.publish(tw)
        rclpy.spin_once(n, timeout_sec=0.05)
        if time.time() - t0 > k * a.seconds / 16:
            n.save("overview_camera", f"overview_{k:02d}.png")
            n.save("top_camera", f"top_{k:02d}.png")
            k += 1
    for _ in range(20):
        n.pub.publish(Twist())
        rclpy.spin_once(n, timeout_sec=0.05)
    n.save("overview_camera", "overview_99_end.png")
    n.save("top_camera", "top_99_end.png")
    s = n.scan
    np.savez(n.out / "run_log.npz", odom=np.array(n.odom),
             scan_ranges=np.array(s.ranges if s else []), scan_angle_min=s.angle_min if s else 0.0,
             scan_angle_inc=s.angle_increment if s else 0.0)
    print(f"saved to {n.out}; odom samples={len(n.odom)}; scan={'yes' if s else 'no'}")
    rclpy.shutdown()


if __name__ == "__main__":
    main()
