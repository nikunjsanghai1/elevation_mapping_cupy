from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Get package directories
    elevation_mapping_cupy_dir = get_package_share_directory('elevation_mapping_cupy')
    gazebo_ros_dir = get_package_share_directory('gazebo_ros')
    turtlebot3_gazebo_dir = get_package_share_directory('turtlebot3_gazebo')
    turtlebot3_description_dir = get_package_share_directory('turtlebot3_description')

    # Declare launch arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )
    use_sim_time = LaunchConfiguration('use_sim_time')

    namespace_arg = DeclareLaunchArgument(
        'namespace',
        default_value='turtlebot3',
        description='Namespace for the robot'
    )
    namespace = LaunchConfiguration('namespace')

    # Include the turtlesim_init launch file for basic simulation setup
    turtlesim_init = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                elevation_mapping_cupy_dir,
                'launch',
                'turtlesim_init.launch.py'
            ])
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'namespace': namespace
        }.items()
    )

    # Elevation Mapping Node with minimal configuration
    elevation_mapping_node = Node(
        package='elevation_mapping_cupy',
        executable='elevation_mapping_node',
        name='elevation_mapping',
        namespace=namespace,
        arguments=['--ros-args', '--log-level', 'debug'],
        output='screen',
        parameters=[
            PathJoinSubstitution([
                elevation_mapping_cupy_dir,
                'config',
                'core',
                'core_param.yaml'
            ]),
            {
                'use_sim_time': use_sim_time,
                'enable_edge_sharpen': False,
                'enable_visibility_cleanup': False,
                'enable_drift_compensation': False,
                'enable_overlap_clearance': False,
                'enable_pointcloud_publishing': False,
                'enable_drift_corrected_TF_publishing': False,
                'enable_normal_color': False,
                'use_chainer': True,  # Use Chainer for lower GPU memory usage
                'publishers': {
                    'elevation_map_raw': {
                        'layers': ['elevation', 'variance'],
                        'basic_layers': ['elevation'],
                        'fps': 5.0
                    }
                },
                'subscribers': {
                    'front_cam': {
                        'topic_name': [namespace, '/camera/depth/points'],
                        'data_type': 'pointcloud'
                    }
                }
            }
        ]
    )

    return LaunchDescription([
        use_sim_time_arg,
        namespace_arg,
        turtlesim_init,
        elevation_mapping_node
    ]) 