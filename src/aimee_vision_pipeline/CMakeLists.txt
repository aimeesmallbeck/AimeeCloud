cmake_minimum_required(VERSION 3.8)
project(aimee_vision_pipeline)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(aimee_msgs REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(image_transport REQUIRED)
find_package(OpenCV REQUIRED)

include_directories(include)

add_library(${PROJECT_NAME}_components SHARED
  src/color_detector.cpp
  src/object_tracker.cpp
)

target_include_directories(${PROJECT_NAME}_components PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${OpenCV_INCLUDE_DIRS}
)

ament_target_dependencies(${PROJECT_NAME}_components
  rclcpp
  rclcpp_components
  std_msgs
  sensor_msgs
  geometry_msgs
  aimee_msgs
  cv_bridge
  image_transport
)

target_link_libraries(${PROJECT_NAME}_components
  ${OpenCV_LIBRARIES}
)

rclcpp_components_register_nodes(${PROJECT_NAME}_components "aimee_vision_pipeline::ColorDetectorNode")
rclcpp_components_register_nodes(${PROJECT_NAME}_components "aimee_vision_pipeline::ObjectTrackerNode")

# Create standalone executables
add_executable(color_detector_node src/color_detector_main.cpp)
target_link_libraries(color_detector_node ${PROJECT_NAME}_components)
ament_target_dependencies(color_detector_node rclcpp)

add_executable(object_tracker_node src/object_tracker_main.cpp)
target_link_libraries(object_tracker_node ${PROJECT_NAME}_components)
ament_target_dependencies(object_tracker_node rclcpp)

install(TARGETS
  ${PROJECT_NAME}_components
  color_detector_node
  object_tracker_node
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY include/
  DESTINATION include
)

install(DIRECTORY config
  DESTINATION share/${PROJECT_NAME}
  PATTERN ".svn" EXCLUDE
)

ament_export_include_directories(include)
ament_export_libraries(${PROJECT_NAME}_components)
ament_package()
