// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aimee_msgs:msg/Intent.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__INTENT__BUILDER_HPP_
#define AIMEE_MSGS__MSG__DETAIL__INTENT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aimee_msgs/msg/detail/intent__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aimee_msgs
{

namespace msg
{

namespace builder
{

class Init_Intent_timestamp
{
public:
  explicit Init_Intent_timestamp(::aimee_msgs::msg::Intent & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::msg::Intent timestamp(::aimee_msgs::msg::Intent::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::msg::Intent msg_;
};

class Init_Intent_session_id
{
public:
  explicit Init_Intent_session_id(::aimee_msgs::msg::Intent & msg)
  : msg_(msg)
  {}
  Init_Intent_timestamp session_id(::aimee_msgs::msg::Intent::_session_id_type arg)
  {
    msg_.session_id = std::move(arg);
    return Init_Intent_timestamp(msg_);
  }

private:
  ::aimee_msgs::msg::Intent msg_;
};

class Init_Intent_parameters_json
{
public:
  explicit Init_Intent_parameters_json(::aimee_msgs::msg::Intent & msg)
  : msg_(msg)
  {}
  Init_Intent_session_id parameters_json(::aimee_msgs::msg::Intent::_parameters_json_type arg)
  {
    msg_.parameters_json = std::move(arg);
    return Init_Intent_session_id(msg_);
  }

private:
  ::aimee_msgs::msg::Intent msg_;
};

class Init_Intent_skill_name
{
public:
  explicit Init_Intent_skill_name(::aimee_msgs::msg::Intent & msg)
  : msg_(msg)
  {}
  Init_Intent_parameters_json skill_name(::aimee_msgs::msg::Intent::_skill_name_type arg)
  {
    msg_.skill_name = std::move(arg);
    return Init_Intent_parameters_json(msg_);
  }

private:
  ::aimee_msgs::msg::Intent msg_;
};

class Init_Intent_requires_skill
{
public:
  explicit Init_Intent_requires_skill(::aimee_msgs::msg::Intent & msg)
  : msg_(msg)
  {}
  Init_Intent_skill_name requires_skill(::aimee_msgs::msg::Intent::_requires_skill_type arg)
  {
    msg_.requires_skill = std::move(arg);
    return Init_Intent_skill_name(msg_);
  }

private:
  ::aimee_msgs::msg::Intent msg_;
};

class Init_Intent_raw_text
{
public:
  explicit Init_Intent_raw_text(::aimee_msgs::msg::Intent & msg)
  : msg_(msg)
  {}
  Init_Intent_requires_skill raw_text(::aimee_msgs::msg::Intent::_raw_text_type arg)
  {
    msg_.raw_text = std::move(arg);
    return Init_Intent_requires_skill(msg_);
  }

private:
  ::aimee_msgs::msg::Intent msg_;
};

class Init_Intent_confidence
{
public:
  explicit Init_Intent_confidence(::aimee_msgs::msg::Intent & msg)
  : msg_(msg)
  {}
  Init_Intent_raw_text confidence(::aimee_msgs::msg::Intent::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_Intent_raw_text(msg_);
  }

private:
  ::aimee_msgs::msg::Intent msg_;
};

class Init_Intent_action
{
public:
  explicit Init_Intent_action(::aimee_msgs::msg::Intent & msg)
  : msg_(msg)
  {}
  Init_Intent_confidence action(::aimee_msgs::msg::Intent::_action_type arg)
  {
    msg_.action = std::move(arg);
    return Init_Intent_confidence(msg_);
  }

private:
  ::aimee_msgs::msg::Intent msg_;
};

class Init_Intent_intent_type
{
public:
  Init_Intent_intent_type()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Intent_action intent_type(::aimee_msgs::msg::Intent::_intent_type_type arg)
  {
    msg_.intent_type = std::move(arg);
    return Init_Intent_action(msg_);
  }

private:
  ::aimee_msgs::msg::Intent msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::msg::Intent>()
{
  return aimee_msgs::msg::builder::Init_Intent_intent_type();
}

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__INTENT__BUILDER_HPP_
