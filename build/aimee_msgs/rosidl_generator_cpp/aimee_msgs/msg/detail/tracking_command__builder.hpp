// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aimee_msgs:msg/TrackingCommand.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__TRACKING_COMMAND__BUILDER_HPP_
#define AIMEE_MSGS__MSG__DETAIL__TRACKING_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aimee_msgs/msg/detail/tracking_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aimee_msgs
{

namespace msg
{

namespace builder
{

class Init_TrackingCommand_timestamp
{
public:
  explicit Init_TrackingCommand_timestamp(::aimee_msgs::msg::TrackingCommand & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::msg::TrackingCommand timestamp(::aimee_msgs::msg::TrackingCommand::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::msg::TrackingCommand msg_;
};

class Init_TrackingCommand_target_position
{
public:
  explicit Init_TrackingCommand_target_position(::aimee_msgs::msg::TrackingCommand & msg)
  : msg_(msg)
  {}
  Init_TrackingCommand_timestamp target_position(::aimee_msgs::msg::TrackingCommand::_target_position_type arg)
  {
    msg_.target_position = std::move(arg);
    return Init_TrackingCommand_timestamp(msg_);
  }

private:
  ::aimee_msgs::msg::TrackingCommand msg_;
};

class Init_TrackingCommand_target_id
{
public:
  explicit Init_TrackingCommand_target_id(::aimee_msgs::msg::TrackingCommand & msg)
  : msg_(msg)
  {}
  Init_TrackingCommand_target_position target_id(::aimee_msgs::msg::TrackingCommand::_target_id_type arg)
  {
    msg_.target_id = std::move(arg);
    return Init_TrackingCommand_target_position(msg_);
  }

private:
  ::aimee_msgs::msg::TrackingCommand msg_;
};

class Init_TrackingCommand_target_type
{
public:
  explicit Init_TrackingCommand_target_type(::aimee_msgs::msg::TrackingCommand & msg)
  : msg_(msg)
  {}
  Init_TrackingCommand_target_id target_type(::aimee_msgs::msg::TrackingCommand::_target_type_type arg)
  {
    msg_.target_type = std::move(arg);
    return Init_TrackingCommand_target_id(msg_);
  }

private:
  ::aimee_msgs::msg::TrackingCommand msg_;
};

class Init_TrackingCommand_zoom_level
{
public:
  explicit Init_TrackingCommand_zoom_level(::aimee_msgs::msg::TrackingCommand & msg)
  : msg_(msg)
  {}
  Init_TrackingCommand_target_type zoom_level(::aimee_msgs::msg::TrackingCommand::_zoom_level_type arg)
  {
    msg_.zoom_level = std::move(arg);
    return Init_TrackingCommand_target_type(msg_);
  }

private:
  ::aimee_msgs::msg::TrackingCommand msg_;
};

class Init_TrackingCommand_preset_id
{
public:
  explicit Init_TrackingCommand_preset_id(::aimee_msgs::msg::TrackingCommand & msg)
  : msg_(msg)
  {}
  Init_TrackingCommand_zoom_level preset_id(::aimee_msgs::msg::TrackingCommand::_preset_id_type arg)
  {
    msg_.preset_id = std::move(arg);
    return Init_TrackingCommand_zoom_level(msg_);
  }

private:
  ::aimee_msgs::msg::TrackingCommand msg_;
};

class Init_TrackingCommand_mode
{
public:
  explicit Init_TrackingCommand_mode(::aimee_msgs::msg::TrackingCommand & msg)
  : msg_(msg)
  {}
  Init_TrackingCommand_preset_id mode(::aimee_msgs::msg::TrackingCommand::_mode_type arg)
  {
    msg_.mode = std::move(arg);
    return Init_TrackingCommand_preset_id(msg_);
  }

private:
  ::aimee_msgs::msg::TrackingCommand msg_;
};

class Init_TrackingCommand_command
{
public:
  Init_TrackingCommand_command()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TrackingCommand_mode command(::aimee_msgs::msg::TrackingCommand::_command_type arg)
  {
    msg_.command = std::move(arg);
    return Init_TrackingCommand_mode(msg_);
  }

private:
  ::aimee_msgs::msg::TrackingCommand msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::msg::TrackingCommand>()
{
  return aimee_msgs::msg::builder::Init_TrackingCommand_command();
}

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__TRACKING_COMMAND__BUILDER_HPP_
