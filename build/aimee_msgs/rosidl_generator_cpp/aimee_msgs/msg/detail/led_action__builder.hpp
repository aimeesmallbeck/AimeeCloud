// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aimee_msgs:msg/LEDAction.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__LED_ACTION__BUILDER_HPP_
#define AIMEE_MSGS__MSG__DETAIL__LED_ACTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aimee_msgs/msg/detail/led_action__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aimee_msgs
{

namespace msg
{

namespace builder
{

class Init_LEDAction_duration_sec
{
public:
  explicit Init_LEDAction_duration_sec(::aimee_msgs::msg::LEDAction & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::msg::LEDAction duration_sec(::aimee_msgs::msg::LEDAction::_duration_sec_type arg)
  {
    msg_.duration_sec = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::msg::LEDAction msg_;
};

class Init_LEDAction_pattern
{
public:
  explicit Init_LEDAction_pattern(::aimee_msgs::msg::LEDAction & msg)
  : msg_(msg)
  {}
  Init_LEDAction_duration_sec pattern(::aimee_msgs::msg::LEDAction::_pattern_type arg)
  {
    msg_.pattern = std::move(arg);
    return Init_LEDAction_duration_sec(msg_);
  }

private:
  ::aimee_msgs::msg::LEDAction msg_;
};

class Init_LEDAction_color
{
public:
  explicit Init_LEDAction_color(::aimee_msgs::msg::LEDAction & msg)
  : msg_(msg)
  {}
  Init_LEDAction_pattern color(::aimee_msgs::msg::LEDAction::_color_type arg)
  {
    msg_.color = std::move(arg);
    return Init_LEDAction_pattern(msg_);
  }

private:
  ::aimee_msgs::msg::LEDAction msg_;
};

class Init_LEDAction_led_id
{
public:
  Init_LEDAction_led_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LEDAction_color led_id(::aimee_msgs::msg::LEDAction::_led_id_type arg)
  {
    msg_.led_id = std::move(arg);
    return Init_LEDAction_color(msg_);
  }

private:
  ::aimee_msgs::msg::LEDAction msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::msg::LEDAction>()
{
  return aimee_msgs::msg::builder::Init_LEDAction_led_id();
}

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__LED_ACTION__BUILDER_HPP_
