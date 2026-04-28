#include <rclcpp/rclcpp.hpp>
#include "aimee_vision_pipeline/color_detector.hpp"

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<aimee_vision_pipeline::ColorDetectorNode>());
  rclcpp::shutdown();
  return 0;
}
