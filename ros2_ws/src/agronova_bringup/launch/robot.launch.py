import os

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    share = get_package_share_directory("agronova_description")
    urdf = xacro.process_file(os.path.join(share, "urdf", "agronova.urdf.xacro")).toxml()
    return LaunchDescription([
        Node(package="robot_state_publisher", executable="robot_state_publisher",
             parameters=[{"robot_description": urdf}]),
        Node(package="agronova_kinematics", executable="diff_drive_node",
             parameters=[{"wheel_radius": 0.15, "track_width": 0.50}]),
    ])
