// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aimee_msgs:msg/MotorAction.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__MOTOR_ACTION__BUILDER_HPP_
#define AIMEE_MSGS__MSG__DETAIL__MOTOR_ACTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aimee_msgs/msg/detail/motor_action__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aimee_msgs
{

namespace msg
{

namespace builder
{

class Init_MotorAction_execution_time
{
public:
  explicit Init_MotorAction_execution_time(::aimee_msgs::msg::MotorAction & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::msg::MotorAction execution_time(::aimee_msgs::msg::MotorAction::_execution_time_type arg)
  {
    msg_.execution_time = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::msg::MotorAction msg_;
};

class Init_MotorAction_values
{
public:
  explicit Init_MotorAction_values(::aimee_msgs::msg::MotorAction & msg)
  : msg_(msg)
  {}
  Init_MotorAction_execution_time values(::aimee_msgs::msg::MotorAction::_values_type arg)
  {
    msg_.values = std::move(arg);
    return Init_MotorAction_execution_time(msg_);
  }

private:
  ::aimee_msgs::msg::MotorAction msg_;
};

class Init_MotorAction_action_type
{
public:
  explicit Init_MotorAction_action_type(::aimee_msgs::msg::MotorAction & msg)
  : msg_(msg)
  {}
  Init_MotorAction_values action_type(::aimee_msgs::msg::MotorAction::_action_type_type arg)
  {
    msg_.action_type = std::move(arg);
    return Init_MotorAction_values(msg_);
  }

private:
  ::aimee_msgs::msg::MotorAction msg_;
};

class Init_MotorAction_motor_id
{
public:
  Init_MotorAction_motor_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotorAction_action_type motor_id(::aimee_msgs::msg::MotorAction::_motor_id_type arg)
  {
    msg_.motor_id = std::move(arg);
    return Init_MotorAction_action_type(msg_);
  }

private:
  ::aimee_msgs::msg::MotorAction msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::msg::MotorAction>()
{
  return aimee_msgs::msg::builder::Init_MotorAction_motor_id();
}

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__MOTOR_ACTION__BUILDER_HPP_
