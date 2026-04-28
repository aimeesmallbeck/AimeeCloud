#include "aimee_vision_pipeline/color_detector.hpp"
#include <rclcpp_components/register_node_macro.hpp>

namespace aimee_vision_pipeline
{

ColorDetectorNode::ColorDetectorNode(const rclcpp::NodeOptions & options)
: Node("color_detector_node", options)
{
    enabled_colors_ = this->declare_parameter("enabled_colors", std::vector<std::string>{"red", "blue", "green", "yellow"});
    detectable_objects_ = this->declare_parameter("detectable_objects", std::vector<std::string>{"ball", "cup", "block"});
    confidence_threshold_ = this->declare_parameter("confidence_threshold", 0.5);
    min_area_ = this->declare_parameter("min_detection_area", 100);
    max_area_ = this->declare_parameter("max_detection_area", 50000);
    std::string camera_topic = this->declare_parameter("camera_topic", "/camera/image_raw");
    std::string camera_info_topic = this->declare_parameter("camera_info_topic", "/camera/camera_info");
    publish_debug_ = this->declare_parameter("publish_debug_image", true);
    std::string debug_image_topic = this->declare_parameter("debug_image_topic", "/vision/debug_image");
    frame_id_ = this->declare_parameter("frame_id", "obsbot_camera");

    color_ranges_["red"] = {
        {cv::Scalar(0, 100, 100), cv::Scalar(10, 255, 255)},
        {cv::Scalar(160, 100, 100), cv::Scalar(180, 255, 255)}
    };
    color_ranges_["blue"] = { {cv::Scalar(100, 150, 50), cv::Scalar(130, 255, 255)} };
    color_ranges_["green"] = { {cv::Scalar(40, 100, 100), cv::Scalar(80, 255, 255)} };
    color_ranges_["yellow"] = { {cv::Scalar(20, 100, 100), cv::Scalar(35, 255, 255)} };
    color_ranges_["orange"] = { {cv::Scalar(10, 100, 100), cv::Scalar(20, 255, 255)} };
    color_ranges_["purple"] = { {cv::Scalar(130, 100, 100), cv::Scalar(160, 255, 255)} };

    object_configs_["ball"] = {0.8, 1.2, 100, 50000, 0.7};
    object_configs_["cup"] = {0.5, 0.9, 500, 50000, 0.3};
    object_configs_["block"] = {0.7, 1.3, 200, 30000, 0.5};

    rclcpp::QoS reliable_qos(rclcpp::KeepLast(10));
    reliable_qos.reliable();
    rclcpp::QoS best_effort_qos(rclcpp::KeepLast(1));
    best_effort_qos.best_effort();

    detections_pub_ = this->create_publisher<aimee_msgs::msg::ObjectDetection>("/vision/detections", reliable_qos);
    if (publish_debug_) {
        debug_image_pub_ = this->create_publisher<sensor_msgs::msg::Image>(debug_image_topic, best_effort_qos);
    }

    image_sub_ = this->create_subscription<sensor_msgs::msg::Image>(
        camera_topic, best_effort_qos,
        std::bind(&ColorDetectorNode::on_image, this, std::placeholders::_1));

    camera_info_sub_ = this->create_subscription<sensor_msgs::msg::CameraInfo>(
        camera_info_topic, reliable_qos,
        std::bind(&ColorDetectorNode::on_camera_info, this, std::placeholders::_1));

    RCLCPP_INFO(this->get_logger(), "ColorDetectorNode initialized");
}

void ColorDetectorNode::on_camera_info(const sensor_msgs::msg::CameraInfo::ConstSharedPtr& msg)
{
    camera_info_ = msg;
}

void ColorDetectorNode::on_image(const sensor_msgs::msg::Image::ConstSharedPtr& msg)
{
    try {
        cv_bridge::CvImageConstPtr cv_ptr = cv_bridge::toCvShare(msg, "bgr8");
        const cv::Mat& cv_image = cv_ptr->image;
        image_height_ = cv_image.rows;
        image_width_ = cv_image.cols;

        auto detections = detect_objects(cv_image);

        for (const auto& detection : detections) {
            detections_pub_->publish(detection);
        }

        if (publish_debug_ && debug_image_pub_->get_subscription_count() > 0) {
            cv::Mat debug_image = draw_detections(cv_image.clone(), detections);
            sensor_msgs::msg::Image::SharedPtr debug_msg = cv_bridge::CvImage(msg->header, "bgr8", debug_image).toImageMsg();
            debug_image_pub_->publish(*debug_msg);
        }
    } catch (const cv_bridge::Exception& e) {
        RCLCPP_ERROR(this->get_logger(), "cv_bridge exception: %s", e.what());
    } catch (const std::exception& e) {
        RCLCPP_ERROR(this->get_logger(), "Error processing image: %s", e.what());
    }
}

std::vector<aimee_msgs::msg::ObjectDetection> ColorDetectorNode::detect_objects(const cv::Mat & image)
{
    std::vector<aimee_msgs::msg::ObjectDetection> detections;
    cv::Mat hsv;
    cv::cvtColor(image, hsv, cv::COLOR_BGR2HSV);

    for (const auto& color : enabled_colors_) {
        if (color_ranges_.find(color) == color_ranges_.end()) continue;
        auto color_detections = detect_color(hsv, image, color);
        detections.insert(detections.end(), color_detections.begin(), color_detections.end());
    }
    return detections;
}

std::vector<aimee_msgs::msg::ObjectDetection> ColorDetectorNode::detect_color(const cv::Mat & hsv, const cv::Mat & /*bgr*/, const std::string & color)
{
    std::vector<aimee_msgs::msg::ObjectDetection> detections;
    cv::Mat mask = cv::Mat::zeros(hsv.size(), CV_8UC1);

    for (const auto& range : color_ranges_[color]) {
        cv::Mat temp_mask;
        cv::inRange(hsv, range.lower, range.upper, temp_mask);
        cv::bitwise_or(mask, temp_mask, mask);
    }

    cv::Mat kernel = cv::Mat::ones(5, 5, CV_8UC1);
    cv::morphologyEx(mask, mask, cv::MORPH_OPEN, kernel);
    cv::morphologyEx(mask, mask, cv::MORPH_CLOSE, kernel);

    std::vector<std::vector<cv::Point>> contours;
    cv::findContours(mask, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

    for (const auto& contour : contours) {
        auto detection = process_contour(contour, color);
        if (detection) {
            detections.push_back(*detection);
        }
    }
    return detections;
}

std::optional<aimee_msgs::msg::ObjectDetection> ColorDetectorNode::process_contour(const std::vector<cv::Point> & contour, const std::string & color)
{
    double area = cv::contourArea(contour);
    if (area < min_area_ || area > max_area_) return std::nullopt;

    cv::Rect bbox = cv::boundingRect(contour);
    
    double center_x = (bbox.x + bbox.width / 2.0) / image_width_;
    double center_y = (bbox.y + bbox.height / 2.0) / image_height_;
    double norm_width = static_cast<double>(bbox.width) / image_width_;
    double norm_height = static_cast<double>(bbox.height) / image_height_;

    double perimeter = cv::arcLength(contour, true);
    double circularity = 0.0;
    if (perimeter > 0) {
        circularity = 4 * CV_PI * area / (perimeter * perimeter);
    }

    std::string object_class = classify_object(contour, bbox.width, bbox.height, circularity);

    double confidence = std::min(1.0, area / 10000.0) * 0.5;
    if (object_class == "ball") {
        confidence += circularity * 0.5;
    } else {
        confidence += 0.3;
    }

    if (confidence < confidence_threshold_) return std::nullopt;

    aimee_msgs::msg::ObjectDetection detection;
    detection.object_class = object_class;
    detection.object_id = color + "_" + object_class + "_" + std::to_string(reinterpret_cast<uintptr_t>(&contour)).substr(0, 8);
    detection.color = color;
    detection.confidence = confidence;
    detection.bbox_x = center_x;
    detection.bbox_y = center_y;
    detection.bbox_width = norm_width;
    detection.bbox_height = norm_height;
    detection.detection_method = "color";
    detection.camera_source = frame_id_;
    detection.timestamp = this->now();

    return detection;
}

std::string ColorDetectorNode::classify_object(const std::vector<cv::Point> & /*contour*/, int w, int h, double circularity)
{
    double aspect_ratio = (h > 0) ? static_cast<double>(w) / h : 1.0;

    for (const auto& obj_type : detectable_objects_) {
        if (object_configs_.find(obj_type) == object_configs_.end()) continue;
        const auto& config = object_configs_[obj_type];
        
        if (aspect_ratio >= config.aspect_ratio_min && aspect_ratio <= config.aspect_ratio_max &&
            circularity >= config.circularity_threshold) {
            return obj_type;
        }
    }
    return "object";
}

cv::Mat ColorDetectorNode::draw_detections(cv::Mat image, const std::vector<aimee_msgs::msg::ObjectDetection> & detections)
{
    for (const auto& det : detections) {
        int cx = static_cast<int>(det.bbox_x * image_width_);
        int cy = static_cast<int>(det.bbox_y * image_height_);
        int w = static_cast<int>(det.bbox_width * image_width_);
        int h = static_cast<int>(det.bbox_height * image_height_);

        int x1 = cx - w / 2;
        int y1 = cy - h / 2;
        int x2 = x1 + w;
        int y2 = y1 + h;

        cv::Scalar color_scalar(255, 255, 255);
        if (det.color == "red") color_scalar = cv::Scalar(0, 0, 255);
        else if (det.color == "blue") color_scalar = cv::Scalar(255, 0, 0);
        else if (det.color == "green") color_scalar = cv::Scalar(0, 255, 0);
        else if (det.color == "yellow") color_scalar = cv::Scalar(0, 255, 255);
        else if (det.color == "orange") color_scalar = cv::Scalar(0, 128, 255);
        else if (det.color == "purple") color_scalar = cv::Scalar(255, 0, 255);

        cv::rectangle(image, cv::Point(x1, y1), cv::Point(x2, y2), color_scalar, 2);
        
        char label[128];
        snprintf(label, sizeof(label), "%s %s: %.2f", det.color.c_str(), det.object_class.c_str(), det.confidence);
        cv::putText(image, label, cv::Point(x1, y1 - 5), cv::FONT_HERSHEY_SIMPLEX, 0.5, color_scalar, 2);
        cv::circle(image, cv::Point(cx, cy), 3, color_scalar, -1);
    }
    
    char stats[64];
    snprintf(stats, sizeof(stats), "Detections: %zu", detections.size());
    cv::putText(image, stats, cv::Point(10, 30), cv::FONT_HERSHEY_SIMPLEX, 0.7, cv::Scalar(255, 255, 255), 2);
    
    return image;
}

}  // namespace aimee_vision_pipeline

RCLCPP_COMPONENTS_REGISTER_NODE(aimee_vision_pipeline::ColorDetectorNode)
