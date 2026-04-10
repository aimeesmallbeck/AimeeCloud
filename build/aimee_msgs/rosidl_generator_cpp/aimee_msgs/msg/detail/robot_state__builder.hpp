// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aimee_msgs:msg/RobotState.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__ROBOT_STATE__BUILDER_HPP_
#define AIMEE_MSGS__MSG__DETAIL__ROBOT_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aimee_msgs/msg/detail/robot_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aimee_msgs
{

namespace msg
{

namespace builder
{

class Init_RobotState_timestamp
{
public:
  explicit Init_RobotState_timestamp(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::msg::RobotState timestamp(::aimee_msgs::msg::RobotState::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_warnings
{
public:
  explicit Init_RobotState_warnings(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_timestamp warnings(::aimee_msgs::msg::RobotState::_warnings_type arg)
  {
    msg_.warnings = std::move(arg);
    return Init_RobotState_timestamp(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_errors
{
public:
  explicit Init_RobotState_errors(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_warnings errors(::aimee_msgs::msg::RobotState::_errors_type arg)
  {
    msg_.errors = std::move(arg);
    return Init_RobotState_warnings(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_current_skill_id
{
public:
  explicit Init_RobotState_current_skill_id(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_errors current_skill_id(::aimee_msgs::msg::RobotState::_current_skill_id_type arg)
  {
    msg_.current_skill_id = std::move(arg);
    return Init_RobotState_errors(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_active_skills
{
public:
  explicit Init_RobotState_active_skills(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_current_skill_id active_skills(::aimee_msgs::msg::RobotState::_active_skills_type arg)
  {
    msg_.active_skills = std::move(arg);
    return Init_RobotState_current_skill_id(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_tracking_target
{
public:
  explicit Init_RobotState_tracking_target(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_active_skills tracking_target(::aimee_msgs::msg::RobotState::_tracking_target_type arg)
  {
    msg_.tracking_target = std::move(arg);
    return Init_RobotState_active_skills(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_camera_mode
{
public:
  explicit Init_RobotState_camera_mode(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_tracking_target camera_mode(::aimee_msgs::msg::RobotState::_camera_mode_type arg)
  {
    msg_.camera_mode = std::move(arg);
    return Init_RobotState_tracking_target(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_gripper_position
{
public:
  explicit Init_RobotState_gripper_position(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_camera_mode gripper_position(::aimee_msgs::msg::RobotState::_gripper_position_type arg)
  {
    msg_.gripper_position = std::move(arg);
    return Init_RobotState_camera_mode(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_arm_pose_name
{
public:
  explicit Init_RobotState_arm_pose_name(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_gripper_position arm_pose_name(::aimee_msgs::msg::RobotState::_arm_pose_name_type arg)
  {
    msg_.arm_pose_name = std::move(arg);
    return Init_RobotState_gripper_position(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_arm_is_moving
{
public:
  explicit Init_RobotState_arm_is_moving(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_arm_pose_name arm_is_moving(::aimee_msgs::msg::RobotState::_arm_is_moving_type arg)
  {
    msg_.arm_is_moving = std::move(arg);
    return Init_RobotState_arm_pose_name(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_arm_state
{
public:
  explicit Init_RobotState_arm_state(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_arm_is_moving arm_state(::aimee_msgs::msg::RobotState::_arm_state_type arg)
  {
    msg_.arm_state = std::move(arg);
    return Init_RobotState_arm_is_moving(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_odometry
{
public:
  explicit Init_RobotState_odometry(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_arm_state odometry(::aimee_msgs::msg::RobotState::_odometry_type arg)
  {
    msg_.odometry = std::move(arg);
    return Init_RobotState_arm_state(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_current_velocity
{
public:
  explicit Init_RobotState_current_velocity(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_odometry current_velocity(::aimee_msgs::msg::RobotState::_current_velocity_type arg)
  {
    msg_.current_velocity = std::move(arg);
    return Init_RobotState_odometry(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_current_action
{
public:
  explicit Init_RobotState_current_action(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_current_velocity current_action(::aimee_msgs::msg::RobotState::_current_action_type arg)
  {
    msg_.current_action = std::move(arg);
    return Init_RobotState_current_velocity(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_power_status
{
public:
  explicit Init_RobotState_power_status(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_current_action power_status(::aimee_msgs::msg::RobotState::_power_status_type arg)
  {
    msg_.power_status = std::move(arg);
    return Init_RobotState_current_action(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_is_charging
{
public:
  explicit Init_RobotState_is_charging(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_power_status is_charging(::aimee_msgs::msg::RobotState::_is_charging_type arg)
  {
    msg_.is_charging = std::move(arg);
    return Init_RobotState_power_status(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_battery_level
{
public:
  explicit Init_RobotState_battery_level(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_is_charging battery_level(::aimee_msgs::msg::RobotState::_battery_level_type arg)
  {
    msg_.battery_level = std::move(arg);
    return Init_RobotState_is_charging(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_robot_type
{
public:
  explicit Init_RobotState_robot_type(::aimee_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_battery_level robot_type(::aimee_msgs::msg::RobotState::_robot_type_type arg)
  {
    msg_.robot_type = std::move(arg);
    return Init_RobotState_battery_level(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

class Init_RobotState_robot_name
{
public:
  Init_RobotState_robot_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RobotState_robot_type robot_name(::aimee_msgs::msg::RobotState::_robot_name_type arg)
  {
    msg_.robot_name = std::move(arg);
    return Init_RobotState_robot_type(msg_);
  }

private:
  ::aimee_msgs::msg::RobotState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::msg::RobotState>()
{
  return aimee_msgs::msg::builder::Init_RobotState_robot_name();
}

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__ROBOT_STATE__BUILDER_HPP_
