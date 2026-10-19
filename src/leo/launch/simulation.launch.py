import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

import xacro


def generate_launch_description():

    # =========================================================
    # Package paths
    # =========================================================

    pkg_leo = get_package_share_directory('leo')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # =========================================================
    # Gazebo resource path
    # =========================================================

    gazebo_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=os.path.dirname(pkg_leo)
    )

    # =========================================================
    # Robot description
    # =========================================================

    xacro_file = os.path.join(
        pkg_leo,
        'urdf',
        'leo.urdf.xacro'
    )

    robot_description = xacro.process_file(
        xacro_file
    ).toxml()

    # =========================================================
    # World
    # =========================================================

    world_file = os.path.join(
        pkg_leo,
        'worlds',
        'office.world'
    )

    # =========================================================
    # Bridge configuration
    # =========================================================

    bridge_config = os.path.join(
        pkg_leo,
        'config',
        'bridge.yaml'
    )

    # =========================================================
    # Gazebo Harmonic
    # =========================================================

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_ros_gz_sim,
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': world_file + ' -r'
        }.items()
    )

    # =========================================================
    # Robot State Publisher
    # =========================================================

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',

        name='robot_state_publisher',

        parameters=[
            {
                'robot_description': robot_description,
                'use_sim_time': True
            }
        ],

        output='screen'
    )

    # =========================================================
    # Spawn LEO
    # =========================================================

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',

        arguments=[
            '-topic',
            'robot_description',

            '-name',
            'leo',

            '-x',
            '-1.0',

            '-y',
            '-1.0',

            '-z',
            '0.20'
        ],

        output='screen'
    )

    # =========================================================
    # ROS <-> Gazebo bridge
    # =========================================================

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',

        parameters=[
            {
                'config_file': bridge_config
            }
        ],

        output='screen'
    )

    # =========================================================
    # Launch
    # =========================================================

    return LaunchDescription([

        gazebo_resource_path,

        gazebo,

        robot_state_publisher,

        spawn_robot,

        bridge

    ])
