// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aimee_msgs:msg/FaceDetection.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__FACE_DETECTION__BUILDER_HPP_
#define AIMEE_MSGS__MSG__DETAIL__FACE_DETECTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aimee_msgs/msg/detail/face_detection__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aimee_msgs
{

namespace msg
{

namespace builder
{

class Init_FaceDetection_camera_source
{
public:
  explicit Init_FaceDetection_camera_source(::aimee_msgs::msg::FaceDetection & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::msg::FaceDetection camera_source(::aimee_msgs::msg::FaceDetection::_camera_source_type arg)
  {
    msg_.camera_source = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::msg::FaceDetection msg_;
};

class Init_FaceDetection_timestamp
{
public:
  explicit Init_FaceDetection_timestamp(::aimee_msgs::msg::FaceDetection & msg)
  : msg_(msg)
  {}
  Init_FaceDetection_camera_source timestamp(::aimee_msgs::msg::FaceDetection::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return Init_FaceDetection_camera_source(msg_);
  }

private:
  ::aimee_msgs::msg::FaceDetection msg_;
};

class Init_FaceDetection_position_3d
{
public:
  explicit Init_FaceDetection_position_3d(::aimee_msgs::msg::FaceDetection & msg)
  : msg_(msg)
  {}
  Init_FaceDetection_timestamp position_3d(::aimee_msgs::msg::FaceDetection::_position_3d_type arg)
  {
    msg_.position_3d = std::move(arg);
    return Init_FaceDetection_timestamp(msg_);
  }

private:
  ::aimee_msgs::msg::FaceDetection msg_;
};

class Init_FaceDetection_face_landmarks
{
public:
  explicit Init_FaceDetection_face_landmarks(::aimee_msgs::msg::FaceDetection & msg)
  : msg_(msg)
  {}
  Init_FaceDetection_position_3d face_landmarks(::aimee_msgs::msg::FaceDetection::_face_landmarks_type arg)
  {
    msg_.face_landmarks = std::move(arg);
    return Init_FaceDetection_position_3d(msg_);
  }

private:
  ::aimee_msgs::msg::FaceDetection msg_;
};

class Init_FaceDetection_num_faces_detected
{
public:
  explicit Init_FaceDetection_num_faces_detected(::aimee_msgs::msg::FaceDetection & msg)
  : msg_(msg)
  {}
  Init_FaceDetection_face_landmarks num_faces_detected(::aimee_msgs::msg::FaceDetection::_num_faces_detected_type arg)
  {
    msg_.num_faces_detected = std::move(arg);
    return Init_FaceDetection_face_landmarks(msg_);
  }

private:
  ::aimee_msgs::msg::FaceDetection msg_;
};

class Init_FaceDetection_height
{
public:
  explicit Init_FaceDetection_height(::aimee_msgs::msg::FaceDetection & msg)
  : msg_(msg)
  {}
  Init_FaceDetection_num_faces_detected height(::aimee_msgs::msg::FaceDetection::_height_type arg)
  {
    msg_.height = std::move(arg);
    return Init_FaceDetection_num_faces_detected(msg_);
  }

private:
  ::aimee_msgs::msg::FaceDetection msg_;
};

class Init_FaceDetection_width
{
public:
  explicit Init_FaceDetection_width(::aimee_msgs::msg::FaceDetection & msg)
  : msg_(msg)
  {}
  Init_FaceDetection_height width(::aimee_msgs::msg::FaceDetection::_width_type arg)
  {
    msg_.width = std::move(arg);
    return Init_FaceDetection_height(msg_);
  }

private:
  ::aimee_msgs::msg::FaceDetection msg_;
};

class Init_FaceDetection_center_y
{
public:
  explicit Init_FaceDetection_center_y(::aimee_msgs::msg::FaceDetection & msg)
  : msg_(msg)
  {}
  Init_FaceDetection_width center_y(::aimee_msgs::msg::FaceDetection::_center_y_type arg)
  {
    msg_.center_y = std::move(arg);
    return Init_FaceDetection_width(msg_);
  }

private:
  ::aimee_msgs::msg::FaceDetection msg_;
};

class Init_FaceDetection_center_x
{
public:
  explicit Init_FaceDetection_center_x(::aimee_msgs::msg::FaceDetection & msg)
  : msg_(msg)
  {}
  Init_FaceDetection_center_y center_x(::aimee_msgs::msg::FaceDetection::_center_x_type arg)
  {
    msg_.center_x = std::move(arg);
    return Init_FaceDetection_center_y(msg_);
  }

private:
  ::aimee_msgs::msg::FaceDetection msg_;
};

class Init_FaceDetection_recognition_confidence
{
public:
  explicit Init_FaceDetection_recognition_confidence(::aimee_msgs::msg::FaceDetection & msg)
  : msg_(msg)
  {}
  Init_FaceDetection_center_x recognition_confidence(::aimee_msgs::msg::FaceDetection::_recognition_confidence_type arg)
  {
    msg_.recognition_confidence = std::move(arg);
    return Init_FaceDetection_center_x(msg_);
  }

private:
  ::aimee_msgs::msg::FaceDetection msg_;
};

class Init_FaceDetection_person_name
{
public:
  explicit Init_FaceDetection_person_name(::aimee_msgs::msg::FaceDetection & msg)
  : msg_(msg)
  {}
  Init_FaceDetection_recognition_confidence person_name(::aimee_msgs::msg::FaceDetection::_person_name_type arg)
  {
    msg_.person_name = std::move(arg);
    return Init_FaceDetection_recognition_confidence(msg_);
  }

private:
  ::aimee_msgs::msg::FaceDetection msg_;
};

class Init_FaceDetection_face_id
{
public:
  Init_FaceDetection_face_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FaceDetection_person_name face_id(::aimee_msgs::msg::FaceDetection::_face_id_type arg)
  {
    msg_.face_id = std::move(arg);
    return Init_FaceDetection_person_name(msg_);
  }

private:
  ::aimee_msgs::msg::FaceDetection msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::msg::FaceDetection>()
{
  return aimee_msgs::msg::builder::Init_FaceDetection_face_id();
}

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__FACE_DETECTION__BUILDER_HPP_
