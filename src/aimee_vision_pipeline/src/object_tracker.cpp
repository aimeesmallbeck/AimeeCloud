#include "aimee_vision_pipeline/object_tracker.hpp"
#include <rclcpp_components/register_node_macro.hpp>
#include <cmath>
#include <algorithm>

namespace aimee_vision_pipeline
{

TrackedObject::TrackedObject(const aimee_msgs::msg::ObjectDetection& detection, int track_id)
: track_id_(track_id), object_class_(detection.object_class), color_(detection.color), missed_frames_(0), total_frames_(1), confidence_(detection.confidence)
{
    update(detection);
}

void TrackedObject::update(const aimee_msgs::msg::ObjectDetection& detection)
{
    Position p;
    p.x = detection.bbox_x;
    p.y = detection.bbox_y;
    p.width = detection.bbox_width;
    p.height = detection.bbox_height;
    p.confidence = detection.confidence;
    p.timestamp = rclcpp::Time(detection.timestamp);
    
    if (position_history_.size() >= 10) {
        position_history_.pop_front();
    }
    position_history_.push_back(p);
    
    confidence_ = detection.confidence;
    missed_frames_ = 0;
    total_frames_++;
}

void TrackedObject::predict()
{
    missed_frames_++;
}

void TrackedObject::get_smoothed_position(double &x, double &y, double &w, double &h) const
{
    if (position_history_.empty()) {
        x = y = w = h = 0.0;
        return;
    }
    if (position_history_.size() < 2) {
        const auto& p = position_history_.front();
        x = p.x; y = p.y; w = p.width; h = p.height;
        return;
    }
    
    x = 0; y = 0; w = 0; h = 0;
    for (const auto& p : position_history_) {
        x += p.x; y += p.y; w += p.width; h += p.height;
    }
    double count = position_history_.size();
    x /= count; y /= count; w /= count; h /= count;
}

aimee_msgs::msg::ObjectDetection TrackedObject::to_detection_msg() const
{
    double x, y, w, h;
    get_smoothed_position(x, y, w, h);
    
    aimee_msgs::msg::ObjectDetection msg;
    msg.object_class = object_class_;
    char id_buf[64];
    snprintf(id_buf, sizeof(id_buf), "%s_%s_%03d", color_.c_str(), object_class_.c_str(), track_id_);
    msg.object_id = id_buf;
    msg.color = color_;
    msg.confidence = confidence_;
    msg.bbox_x = x;
    msg.bbox_y = y;
    msg.bbox_width = w;
    msg.bbox_height = h;
    msg.detection_method = "tracked";
    msg.camera_source = "tracked";
    
    return msg;
}

ObjectTrackerNode::ObjectTrackerNode(const rclcpp::NodeOptions & options)
: Node("object_tracker_node", options)
{
    max_distance_ = this->declare_parameter("max_distance", 0.15);
    max_missed_ = this->declare_parameter("max_missed_frames", 5);
    min_confirmed_ = this->declare_parameter("min_frames_confirmed", 3);
    
    rclcpp::QoS reliable_qos(rclcpp::KeepLast(10));
    reliable_qos.reliable();
    
    tracked_pub_ = this->create_publisher<aimee_msgs::msg::ObjectDetection>("/vision/tracked_objects", reliable_qos);
    
    detection_sub_ = this->create_subscription<aimee_msgs::msg::ObjectDetection>(
        "/vision/detections", 10,
        std::bind(&ObjectTrackerNode::on_detection, this, std::placeholders::_1));
        
    track_timer_ = this->create_wall_timer(
        std::chrono::milliseconds(33),
        std::bind(&ObjectTrackerNode::update_tracks, this));
        
    RCLCPP_INFO(this->get_logger(), "ObjectTrackerNode initialized");
}

void ObjectTrackerNode::on_detection(const aimee_msgs::msg::ObjectDetection::SharedPtr msg)
{
    std::lock_guard<std::mutex> lock(detections_mutex_);
    pending_detections_.push_back(*msg);
}

void ObjectTrackerNode::update_tracks()
{
    std::vector<aimee_msgs::msg::ObjectDetection> detections;
    {
        std::lock_guard<std::mutex> lock(detections_mutex_);
        if (pending_detections_.empty()) {
            for (auto& pair : tracks_) {
                pair.second.predict();
            }
            cleanup_tracks();
            return;
        }
        detections = std::move(pending_detections_);
        pending_detections_.clear();
    }
    
    for (auto& pair : tracks_) {
        pair.second.predict();
    }
    
    std::vector<int> matched_tracks;
    
    for (const auto& det : detections) {
        int best_track_id = -1;
        double best_score = -1.0;
        
        for (const auto& pair : tracks_) {
            if (std::find(matched_tracks.begin(), matched_tracks.end(), pair.first) != matched_tracks.end()) {
                continue;
            }
            
            double score = calculate_match_score(pair.second, det);
            if (score > best_score && score > 0.5) {
                best_score = score;
                best_track_id = pair.first;
            }
        }
        
        if (best_track_id != -1) {
            tracks_.at(best_track_id).update(det);
            matched_tracks.push_back(best_track_id);
        } else {
            tracks_.emplace(std::piecewise_construct,
                            std::forward_as_tuple(next_track_id_),
                            std::forward_as_tuple(det, next_track_id_));
            next_track_id_++;
        }
    }
    
    publish_tracks();
    cleanup_tracks();
}

double ObjectTrackerNode::calculate_match_score(const TrackedObject& track, const aimee_msgs::msg::ObjectDetection& detection) const
{
    if (track.color_ != detection.color) return 0.0;
    
    if (track.object_class_ != detection.object_class) {
        if (track.object_class_ != "object" && detection.object_class != "object") {
            return 0.0;
        }
    }
    
    double tx, ty, tw, th;
    track.get_smoothed_position(tx, ty, tw, th);
    
    double distance = std::sqrt(std::pow(tx - detection.bbox_x, 2) + std::pow(ty - detection.bbox_y, 2));
    
    if (distance > max_distance_) return 0.0;
    
    double distance_score = 1.0 - (distance / max_distance_);
    return distance_score * 0.7 + detection.confidence * 0.3;
}

void ObjectTrackerNode::cleanup_tracks()
{
    for (auto it = tracks_.begin(); it != tracks_.end(); ) {
        if (it->second.missed_frames_ > max_missed_) {
            it = tracks_.erase(it);
        } else {
            ++it;
        }
    }
}

void ObjectTrackerNode::publish_tracks()
{
    for (const auto& pair : tracks_) {
        if (pair.second.total_frames_ >= min_confirmed_) {
            auto msg = pair.second.to_detection_msg();
            msg.timestamp = this->now();
            tracked_pub_->publish(msg);
        }
    }
}

}  // namespace aimee_vision_pipeline

RCLCPP_COMPONENTS_REGISTER_NODE(aimee_vision_pipeline::ObjectTrackerNode)
