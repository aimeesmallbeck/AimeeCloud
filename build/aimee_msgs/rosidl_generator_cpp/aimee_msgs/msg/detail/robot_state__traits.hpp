// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aimee_msgs:msg/RobotState.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__ROBOT_STATE__TRAITS_HPP_
#define AIMEE_MSGS__MSG__DETAIL__ROBOT_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aimee_msgs/msg/detail/robot_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'current_velocity'
#include "geometry_msgs/msg/detail/twist__traits.hpp"
// Member 'odometry'
#include "nav_msgs/msg/detail/odometry__traits.hpp"
// Member 'arm_state'
#include "sensor_msgs/msg/detail/joint_state__traits.hpp"
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace aimee_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const RobotState & msg,
  std::ostream & out)
{
  out << "{";
  // member: robot_name
  {
    out << "robot_name: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_name, out);
    out << ", ";
  }

  // member: robot_type
  {
    out << "robot_type: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_type, out);
    out << ", ";
  }

  // member: battery_level
  {
    out << "battery_level: ";
    rosidl_generator_traits::value_to_yaml(msg.battery_level, out);
    out << ", ";
  }

  // member: is_charging
  {
    out << "is_charging: ";
    rosidl_generator_traits::value_to_yaml(msg.is_charging, out);
    out << ", ";
  }

  // member: power_status
  {
    out << "power_status: ";
    rosidl_generator_traits::value_to_yaml(msg.power_status, out);
    out << ", ";
  }

  // member: current_action
  {
    out << "current_action: ";
    rosidl_generator_traits::value_to_yaml(msg.current_action, out);
    out << ", ";
  }

  // member: current_velocity
  {
    out << "current_velocity: ";
    to_flow_style_yaml(msg.current_velocity, out);
    out << ", ";
  }

  // member: odometry
  {
    out << "odometry: ";
    to_flow_style_yaml(msg.odometry, out);
    out << ", ";
  }

  // member: arm_state
  {
    out << "arm_state: ";
    to_flow_style_yaml(msg.arm_state, out);
    out << ", ";
  }

  // member: arm_is_moving
  {
    out << "arm_is_moving: ";
    rosidl_generator_traits::value_to_yaml(msg.arm_is_moving, out);
    out << ", ";
  }

  // member: arm_pose_name
  {
    out << "arm_pose_name: ";
    rosidl_generator_traits::value_to_yaml(msg.arm_pose_name, out);
    out << ", ";
  }

  // member: gripper_position
  {
    out << "gripper_position: ";
    rosidl_generator_traits::value_to_yaml(msg.gripper_position, out);
    out << ", ";
  }

  // member: camera_mode
  {
    out << "camera_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.camera_mode, out);
    out << ", ";
  }

  // member: tracking_target
  {
    out << "tracking_target: ";
    rosidl_generator_traits::value_to_yaml(msg.tracking_target, out);
    out << ", ";
  }

  // member: active_skills
  {
    if (msg.active_skills.size() == 0) {
      out << "active_skills: []";
    } else {
      out << "active_skills: [";
      size_t pending_items = msg.active_skills.size();
      for (auto item : msg.active_skills) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: current_skill_id
  {
    out << "current_skill_id: ";
    rosidl_generator_traits::value_to_yaml(msg.current_skill_id, out);
    out << ", ";
  }

  // member: errors
  {
    if (msg.errors.size() == 0) {
      out << "errors: []";
    } else {
      out << "errors: [";
      size_t pending_items = msg.errors.size();
      for (auto item : msg.errors) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: warnings
  {
    if (msg.warnings.size() == 0) {
      out << "warnings: []";
    } else {
      out << "warnings: [";
      size_t pending_items = msg.warnings.size();
      for (auto item : msg.warnings) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: timestamp
  {
    out << "timestamp: ";
    to_flow_style_yaml(msg.timestamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RobotState & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: robot_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "robot_name: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_name, out);
    out << "\n";
  }

  // member: robot_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "robot_type: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_type, out);
    out << "\n";
  }

  // member: battery_level
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "battery_level: ";
    rosidl_generator_traits::value_to_yaml(msg.battery_level, out);
    out << "\n";
  }

  // member: is_charging
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_charging: ";
    rosidl_generator_traits::value_to_yaml(msg.is_charging, out);
    out << "\n";
  }

  // member: power_status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "power_status: ";
    rosidl_generator_traits::value_to_yaml(msg.power_status, out);
    out << "\n";
  }

  // member: current_action
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "current_action: ";
    rosidl_generator_traits::value_to_yaml(msg.current_action, out);
    out << "\n";
  }

  // member: current_velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "current_velocity:\n";
    to_block_style_yaml(msg.current_velocity, out, indentation + 2);
  }

  // member: odometry
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "odometry:\n";
    to_block_style_yaml(msg.odometry, out, indentation + 2);
  }

  // member: arm_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "arm_state:\n";
    to_block_style_yaml(msg.arm_state, out, indentation + 2);
  }

  // member: arm_is_moving
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "arm_is_moving: ";
    rosidl_generator_traits::value_to_yaml(msg.arm_is_moving, out);
    out << "\n";
  }

  // member: arm_pose_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "arm_pose_name: ";
    rosidl_generator_traits::value_to_yaml(msg.arm_pose_name, out);
    out << "\n";
  }

  // member: gripper_position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gripper_position: ";
    rosidl_generator_traits::value_to_yaml(msg.gripper_position, out);
    out << "\n";
  }

  // member: camera_mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "camera_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.camera_mode, out);
    out << "\n";
  }

  // member: tracking_target
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tracking_target: ";
    rosidl_generator_traits::value_to_yaml(msg.tracking_target, out);
    out << "\n";
  }

  // member: active_skills
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.active_skills.size() == 0) {
      out << "active_skills: []\n";
    } else {
      out << "active_skills:\n";
      for (auto item : msg.active_skills) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: current_skill_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "current_skill_id: ";
    rosidl_generator_traits::value_to_yaml(msg.current_skill_id, out);
    out << "\n";
  }

  // member: errors
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.errors.size() == 0) {
      out << "errors: []\n";
    } else {
      out << "errors:\n";
      for (auto item : msg.errors) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: warnings
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.warnings.size() == 0) {
      out << "warnings: []\n";
    } else {
      out << "warnings:\n";
      for (auto item : msg.warnings) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: timestamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "timestamp:\n";
    to_block_style_yaml(msg.timestamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RobotState & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace aimee_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aimee_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aimee_msgs::msg::RobotState & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::msg::RobotState & msg)
{
  return aimee_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::msg::RobotState>()
{
  return "aimee_msgs::msg::RobotState";
}

template<>
inline const char * name<aimee_msgs::msg::RobotState>()
{
  return "aimee_msgs/msg/RobotState";
}

template<>
struct has_fixed_size<aimee_msgs::msg::RobotState>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aimee_msgs::msg::RobotState>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aimee_msgs::msg::RobotState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AIMEE_MSGS__MSG__DETAIL__ROBOT_STATE__TRAITS_HPP_
