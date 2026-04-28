#pragma once

#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/image.hpp>
#include <sensor_msgs/msg/camera_info.hpp>
#include <cv_bridge/cv_bridge.h>
#include <image_transport/image_transport.hpp>
#include "aimee_msgs/msg/object_detection.hpp"

#include <opencv2/opencv.hpp>
#include <map>
#include <vector>
#include <string>
#include <optional>

namespace aimee_vision_pipeline
{

class ColorDetectorNode : public rclcpp::Node
{
public:
  explicit ColorDetectorNode(const rclcpp::NodeOptions & options = rclcpp::NodeOptions());
  virtual ~ColorDetectorNode() = default;

private:
  void on_image(const sensor_msgs::msg::Image::ConstSharedPtr& msg);
  void on_camera_info(const sensor_msgs::msg::CameraInfo::ConstSharedPtr& msg);
  
  std::vector<aimee_msgs::msg::ObjectDetection> detect_objects(const cv::Mat & image);
  std::vector<aimee_msgs::msg::ObjectDetection> detect_color(const cv::Mat & hsv, const cv::Mat & bgr, const std::string & color);
  std::optional<aimee_msgs::msg::ObjectDetection> process_contour(const std::vector<cv::Point> & contour, const std::string & color);
  std::string classify_object(const std::vector<cv::Point> & contour, int w, int h, double circularity);
  cv::Mat draw_detections(cv::Mat image, const std::vector<aimee_msgs::msg::ObjectDetection> & detections);

  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr image_sub_;
  rclcpp::Subscription<sensor_msgs::msg::CameraInfo>::SharedPtr camera_info_sub_;
  rclcpp::Publisher<aimee_msgs::msg::ObjectDetection>::SharedPtr detections_pub_;
  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr debug_image_pub_;

  std::vector<std::string> enabled_colors_;
  std::vector<std::string> detectable_objects_;
  double confidence_threshold_;
  int min_area_;
  int max_area_;
  bool publish_debug_;
  std::string frame_id_;

  sensor_msgs::msg::CameraInfo::ConstSharedPtr camera_info_;
  int image_width_ = 640;
  int image_height_ = 480;

  struct ColorRange {
      cv::Scalar lower;
      cv::Scalar upper;
  };
  std::map<std::string, std::vector<ColorRange>> color_ranges_;

  struct ObjectConfig {
      double aspect_ratio_min;
      double aspect_ratio_max;
      int min_area;
      int max_area;
      double circularity_threshold;
  };
  std::map<std::string, ObjectConfig> object_configs_;
};

}  // namespace aimee_vision_pipeline
