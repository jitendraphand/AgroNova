import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    nav = get_package_share_directory("agronova_navigation")
    nav2 = os.path.join(get_package_share_directory("nav2_bringup"), "launch", "navigation_launch.py")
    return LaunchDescription([
        IncludeLaunchDescription(PythonLaunchDescriptionSource(os.path.join(nav, "launch", "localization.launch.py"))),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(nav2), launch_arguments={
            "params_file": os.path.join(nav, "config", "nav2_params.yaml"), "use_sim_time": "true"}.items()),
    ])
