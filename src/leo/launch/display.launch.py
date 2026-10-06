from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.substitutions import FindPackageShare
import os


def generate_launch_description():

    # Get package path
    pkg = FindPackageShare('leo').find('leo')

    # URDF Xacro file
    xacro_file = os.path.join(pkg, 'urdf', 'leo.urdf.xacro')

    # RViz config file
    rviz_config = os.path.join(pkg, 'rviz', 'leo.rviz')

    return LaunchDescription([

        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': Command(['xacro ', xacro_file])
            }]
        ),

        # Joint State Publisher GUI
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui'
        ),

	Node(
	    package='leo',
	    executable='fake_odom.py',
	    output='screen'
	),

        # RViz with saved config
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config]
        )
    ])
