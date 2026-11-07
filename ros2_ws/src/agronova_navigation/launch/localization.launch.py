import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    cfg = os.path.join(get_package_share_directory("agronova_navigation"), "config", "ekf.yaml")
    sim = {"use_sim_time": LaunchConfiguration("use_sim_time")}
    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value="true"),
        Node(package="robot_localization", executable="ekf_node", name="ekf_local", parameters=[cfg, sim],
             remappings=[("odometry/filtered", "odometry/local")]),
        Node(package="robot_localization", executable="ekf_node", name="ekf_global", parameters=[cfg, sim],
             remappings=[("odometry/filtered", "odometry/global")]),
        Node(package="robot_localization", executable="navsat_transform_node", name="navsat_transform",
             parameters=[cfg, sim], remappings=[("imu/data", "imu"), ("gps/fix", "gps/fix"),
                                                ("odometry/filtered", "odometry/global")]),
    ])
