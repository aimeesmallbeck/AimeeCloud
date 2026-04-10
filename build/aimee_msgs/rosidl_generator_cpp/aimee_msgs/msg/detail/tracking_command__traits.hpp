// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aimee_msgs:msg/TrackingCommand.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__TRACKING_COMMAND__TRAITS_HPP_
#define AIMEE_MSGS__MSG__DETAIL__TRACKING_COMMAND__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aimee_msgs/msg/detail/tracking_command__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'target_position'
#include "geometry_msgs/msg/detail/point__traits.hpp"
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace aimee_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const TrackingCommand & msg,
  std::ostream & out)
{
  out << "{";
  // member: command
  {
    out << "command: ";
    rosidl_generator_traits::value_to_yaml(msg.command, out);
    out << ", ";
  }

  // member: mode
  {
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
    out << ", ";
  }

  // member: preset_id
  {
    out << "preset_id: ";
    rosidl_generator_traits::value_to_yaml(msg.preset_id, out);
    out << ", ";
  }

  // member: zoom_level
  {
    out << "zoom_level: ";
    rosidl_generator_traits::value_to_yaml(msg.zoom_level, out);
    out << ", ";
  }

  // member: target_type
  {
    out << "target_type: ";
    rosidl_generator_traits::value_to_yaml(msg.target_type, out);
    out << ", ";
  }

  // member: target_id
  {
    out << "target_id: ";
    rosidl_generator_traits::value_to_yaml(msg.target_id, out);
    out << ", ";
  }

  // member: target_position
  {
    out << "target_position: ";
    to_flow_style_yaml(msg.target_position, out);
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
  const TrackingCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: command
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "command: ";
    rosidl_generator_traits::value_to_yaml(msg.command, out);
    out << "\n";
  }

  // member: mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
    out << "\n";
  }

  // member: preset_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "preset_id: ";
    rosidl_generator_traits::value_to_yaml(msg.preset_id, out);
    out << "\n";
  }

  // member: zoom_level
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "zoom_level: ";
    rosidl_generator_traits::value_to_yaml(msg.zoom_level, out);
    out << "\n";
  }

  // member: target_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_type: ";
    rosidl_generator_traits::value_to_yaml(msg.target_type, out);
    out << "\n";
  }

  // member: target_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_id: ";
    rosidl_generator_traits::value_to_yaml(msg.target_id, out);
    out << "\n";
  }

  // member: target_position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_position:\n";
    to_block_style_yaml(msg.target_position, out, indentation + 2);
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

inline std::string to_yaml(const TrackingCommand & msg, bool use_flow_style = false)
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
  const aimee_msgs::msg::TrackingCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::msg::TrackingCommand & msg)
{
  return aimee_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::msg::TrackingCommand>()
{
  return "aimee_msgs::msg::TrackingCommand";
}

template<>
inline const char * name<aimee_msgs::msg::TrackingCommand>()
{
  return "aimee_msgs/msg/TrackingCommand";
}

template<>
struct has_fixed_size<aimee_msgs::msg::TrackingCommand>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aimee_msgs::msg::TrackingCommand>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aimee_msgs::msg::TrackingCommand>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AIMEE_MSGS__MSG__DETAIL__TRACKING_COMMAND__TRAITS_HPP_
