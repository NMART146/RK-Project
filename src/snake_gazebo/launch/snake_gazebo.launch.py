import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

# used some claude to get this working, derived from the rviz launch file

def generate_launch_description():

    # --- Launch arguments ---
    gz_args = LaunchConfiguration("gz_args")
    use_rviz = LaunchConfiguration("rviz")

    declare_gz_args = DeclareLaunchArgument(
        "gz_args",
        default_value="-r empty.sdf",
        description="Arguments for gz sim (add -s for headless server only)",
    )
    declare_rviz = DeclareLaunchArgument(
        "rviz",
        default_value="true",
        description="Start RViz",
    )

    # --- Paths ---
    urdf_path = PathJoinSubstitution(
        [FindPackageShare("snake_description"), "urdf", "snake_robot.urdf.xacro"]
    )
    snake_gait_params = PathJoinSubstitution(
        [FindPackageShare("snake_gait"), "config", "snake_gait_config.yaml"]
    )
    rviz_config = PathJoinSubstitution(
        [FindPackageShare("snake_bringup"), "rviz", "snake.rviz"]
    )

    # Let Gazebo resolve package://snake_description/meshes/... by adding the
    # directory that contains snake_description's share folder to its resource path.
    gz_resource_path = AppendEnvironmentVariable(
        "GZ_SIM_RESOURCE_PATH",
        os.path.dirname(get_package_share_directory("snake_description")),
    )

    # --- Robot description (Gazebo hardware) ---
    robot_description_content = ParameterValue(
        Command([FindExecutable(name="xacro"), " ", urdf_path, " gazebo:=true"]),
        value_type=str,
    )
    robot_description = {"robot_description": robot_description_content}

    # --- Gazebo ---
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"]
            )
        ),
        launch_arguments={"gz_args": gz_args, "on_exit_shutdown": "true"}.items(),
    )

    # Bridge the simulation clock into ROS so use_sim_time works
    clock_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"],
        output="screen",
    )

    robot_state_pub_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[robot_description, {"use_sim_time": True}],
    )

    # Spawn the robot from the /robot_description topic, slightly above the ground
    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=["-topic", "robot_description", "-name", "snakebot", "-z", "0.03"],
        output="screen",
    )

    # --- Controllers (the controller manager lives inside Gazebo) ---
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["snake_gait_controller"],
    )

    # --- Gait + visualization ---
    snake_gait_node = Node(
        package="snake_gait",
        executable="snake_gait_node",
        parameters=[snake_gait_params, {"use_sim_time": True}],
        output="screen",
    )

    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_config],
        parameters=[{"use_sim_time": True}],
        output="screen",
        condition=IfCondition(use_rviz),
    )

    # --- Startup ordering ---
    # robot spawned -> joint_state_broadcaster -> snake_gait_controller -> gait node
    start_jsb_after_spawn = RegisterEventHandler(
        OnProcessExit(target_action=spawn_robot, on_exit=[joint_state_broadcaster_spawner])
    )
    start_controller_after_jsb = RegisterEventHandler(
        OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[robot_controller_spawner],
        )
    )
    start_gait_after_controller = RegisterEventHandler(
        OnProcessExit(target_action=robot_controller_spawner, on_exit=[snake_gait_node])
    )

    return LaunchDescription(
        [
            declare_gz_args,
            declare_rviz,
            gz_resource_path,
            gazebo,
            clock_bridge,
            robot_state_pub_node,
            spawn_robot,
            start_jsb_after_spawn,
            start_controller_after_jsb,
            start_gait_after_controller,
            rviz2,
        ]
    )
