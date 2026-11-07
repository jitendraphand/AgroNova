import os

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    desc = get_package_share_directory("agronova_description")
    gz = get_package_share_directory("agronova_gazebo")
    urdf = xacro.process_file(os.path.join(desc, "urdf", "agronova.urdf.xacro"), mappings={"sim": "true"}).toxml()
    world = os.path.join(gz, "worlds", "cotton_field.sdf")
    gz_launch = os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
    return LaunchDescription([
        IncludeLaunchDescription(PythonLaunchDescriptionSource(gz_launch),
                                 launch_arguments={"gz_args": f"-r {world}"}.items()),
        Node(package="robot_state_publisher", executable="robot_state_publisher",
             parameters=[{"robot_description": urdf, "use_sim_time": True}]),
        Node(package="ros_gz_sim", executable="create", arguments=["-name", "agronova", "-topic", "robot_description",
                                                                  "-x", "0", "-y", "0.45", "-z", "0.3"]),
        Node(package="ros_gz_bridge", executable="parameter_bridge",
             parameters=[{"config_file": os.path.join(gz, "config", "bridge.yaml"), "use_sim_time": True}]),
    ])
