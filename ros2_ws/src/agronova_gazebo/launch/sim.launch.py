import os

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def _setup(context):
    desc = get_package_share_directory("agronova_description")
    gz = get_package_share_directory("agronova_gazebo")
    urdf = xacro.process_file(os.path.join(desc, "urdf", "agronova.urdf.xacro"), mappings={"sim": "true"}).toxml()
    world = os.path.join(gz, "worlds", LaunchConfiguration("world").perform(context))
    headless = LaunchConfiguration("headless").perform(context) == "true"
    gz_args = f"-r {world}" + (" -s --headless-rendering" if headless else "")
    gz_launch = os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
    return [
        IncludeLaunchDescription(PythonLaunchDescriptionSource(gz_launch),
                                 launch_arguments={"gz_args": gz_args, "on_exit_shutdown": "true"}.items()),
        Node(package="robot_state_publisher", executable="robot_state_publisher",
             parameters=[{"robot_description": urdf, "use_sim_time": True}]),
        Node(package="ros_gz_sim", executable="create", arguments=["-name", "agronova", "-topic", "robot_description",
                                                                  "-x", "0", "-y", "0", "-z", "0.3"]),
        Node(package="ros_gz_bridge", executable="parameter_bridge",
             parameters=[{"config_file": os.path.join(gz, "config", "bridge.yaml"), "use_sim_time": True}]),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("world", default_value="cotton_field.sdf"),
        DeclareLaunchArgument("headless", default_value="false"),
        OpaqueFunction(function=_setup),
    ])
