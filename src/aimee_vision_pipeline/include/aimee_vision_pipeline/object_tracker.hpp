#pragma once

#include <rclcpp/rclcpp.hpp>
#include "aimee_msgs/msg/object_detection.hpp"
#include <deque>
#include <map>
#include <vector>
#include <string>
#include <mutex>

namespace aimee_vision_pipeline
{

struct Position {
    double x;
    double y;
    double width;
    double height;
    double confidence;
    rclcpp::Time timestamp;
};

class TrackedObject {
public:
    TrackedObject(const aimee_msgs::msg::ObjectDetection& detection, int track_id);
    void update(const aimee_msgs::msg::ObjectDetection& detection);
    void predict();
    void get_smoothed_position(double &x, double &y, double &w, double &h) const;
    aimee_msgs::msg::ObjectDetection to_detection_msg() const;

    int track_id_;
    std::string object_class_;
    std::string color_;
    std::deque<Position> position_history_;
    int missed_frames_;
    int total_frames_;
    double confidence_;
};

class ObjectTrackerNode : public rclcpp::Node
{
public:
    explicit ObjectTrackerNode(const rclcpp::NodeOptions & options = rclcpp::NodeOptions());
    virtual ~ObjectTrackerNode() = default;

private:
    void on_detection(const aimee_msgs::msg::ObjectDetection::SharedPtr msg);
    void update_tracks();
    double calculate_match_score(const TrackedObject& track, const aimee_msgs::msg::ObjectDetection& detection) const;
    void cleanup_tracks();
    void publish_tracks();

    rclcpp::Subscription<aimee_msgs::msg::ObjectDetection>::SharedPtr detection_sub_;
    rclcpp::Publisher<aimee_msgs::msg::ObjectDetection>::SharedPtr tracked_pub_;
    rclcpp::TimerBase::SharedPtr track_timer_;

    double max_distance_;
    int max_missed_;
    int min_confirmed_;
    
    std::map<int, TrackedObject> tracks_;
    int next_track_id_ = 1;
    std::vector<aimee_msgs::msg::ObjectDetection> pending_detections_;
    std::mutex detections_mutex_;
};

}  // namespace aimee_vision_pipeline
