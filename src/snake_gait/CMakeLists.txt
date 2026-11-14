cmake_minimum_required(VERSION 3.8)
project(snake_gait)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# Serpenoid gait publisher node
add_executable(snake_gait_node src/snake_gait.cpp)
target_compile_features(snake_gait_node PUBLIC cxx_std_17)
target_link_libraries(snake_gait_node
  rclcpp::rclcpp
  ${std_msgs_TARGETS}
)

# Installs to lib/snake_gait so `ros2 run snake_gait snake_gait_node` can find it
install(TARGETS snake_gait_node
  DESTINATION lib/${PROJECT_NAME}
)

# Install gait parameter files so launch files can find them
install(DIRECTORY config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
