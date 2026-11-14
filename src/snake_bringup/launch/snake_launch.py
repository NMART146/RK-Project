from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution, FindExecutable
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    # --- Paths ---
    description_pkg = get_package_share_directory("snake_description")
    urdf_path = PathJoinSubstitution([description_pkg, "urdf", "snake_robot.urdf.xacro"])

    use_gazebo = 'false'

    robot_description_content = ParameterValue(Command([
        FindExecutable(name='xacro'),
        ' ',
        urdf_path,
        ' gazebo:=',
        use_gazebo
    ]), value_type=str)

    robot_description = {'robot_description': robot_description_content}

    robot_controllers = PathJoinSubstitution(
        [
            FindPackageShare("snake_bringup"),
            "config",
            "snake_controllers.yaml",
        ]
    )

    snake_gait_params = PathJoinSubstitution(
        [
            FindPackageShare("snake_gait"),
            "config",
            "snake_gait_config.yaml",
        ]
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_controllers],
        output="both",
    )

    robot_state_pub_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "snake_gait_controller",
            "--param-file",
            robot_controllers,
        ],
    )

    snake_gait_node = Node(
        package="snake_gait",
        executable="snake_gait_node",
        parameters=[snake_gait_params],
    )

    rviz_config = PathJoinSubstitution(
        [
            FindPackageShare("snake_bringup"),
            "rviz",
            "snake.rviz",
        ]
    )

    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_config],
        output="screen",
    )


    nodes = [
        control_node,
        robot_state_pub_node,
        joint_state_broadcaster_spawner,
        robot_controller_spawner,
        snake_gait_node,
        rviz2,
        
    ]

    return LaunchDescription(nodes)
