// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aimee_msgs:msg/CameraAction.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__CAMERA_ACTION__BUILDER_HPP_
#define AIMEE_MSGS__MSG__DETAIL__CAMERA_ACTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aimee_msgs/msg/detail/camera_action__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aimee_msgs
{

namespace msg
{

namespace builder
{

class Init_CameraAction_execution_time
{
public:
  explicit Init_CameraAction_execution_time(::aimee_msgs::msg::CameraAction & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::msg::CameraAction execution_time(::aimee_msgs::msg::CameraAction::_execution_time_type arg)
  {
    msg_.execution_time = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::msg::CameraAction msg_;
};

class Init_CameraAction_confidence
{
public:
  explicit Init_CameraAction_confidence(::aimee_msgs::msg::CameraAction & msg)
  : msg_(msg)
  {}
  Init_CameraAction_execution_time confidence(::aimee_msgs::msg::CameraAction::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_CameraAction_execution_time(msg_);
  }

private:
  ::aimee_msgs::msg::CameraAction msg_;
};

class Init_CameraAction_target
{
public:
  explicit Init_CameraAction_target(::aimee_msgs::msg::CameraAction & msg)
  : msg_(msg)
  {}
  Init_CameraAction_confidence target(::aimee_msgs::msg::CameraAction::_target_type arg)
  {
    msg_.target = std::move(arg);
    return Init_CameraAction_confidence(msg_);
  }

private:
  ::aimee_msgs::msg::CameraAction msg_;
};

class Init_CameraAction_action_type
{
public:
  Init_CameraAction_action_type()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CameraAction_target action_type(::aimee_msgs::msg::CameraAction::_action_type_type arg)
  {
    msg_.action_type = std::move(arg);
    return Init_CameraAction_target(msg_);
  }

private:
  ::aimee_msgs::msg::CameraAction msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::msg::CameraAction>()
{
  return aimee_msgs::msg::builder::Init_CameraAction_action_type();
}

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__CAMERA_ACTION__BUILDER_HPP_
