#include <rclcpp/rclcpp.hpp>
#include "aimee_vision_pipeline/object_tracker.hpp"

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<aimee_vision_pipeline::ObjectTrackerNode>());
  rclcpp::shutdown();
  return 0;
}
