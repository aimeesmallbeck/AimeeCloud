// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aimee_msgs:msg/LEDAction.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__LED_ACTION__TRAITS_HPP_
#define AIMEE_MSGS__MSG__DETAIL__LED_ACTION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aimee_msgs/msg/detail/led_action__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace aimee_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const LEDAction & msg,
  std::ostream & out)
{
  out << "{";
  // member: led_id
  {
    out << "led_id: ";
    rosidl_generator_traits::value_to_yaml(msg.led_id, out);
    out << ", ";
  }

  // member: color
  {
    if (msg.color.size() == 0) {
      out << "color: []";
    } else {
      out << "color: [";
      size_t pending_items = msg.color.size();
      for (auto item : msg.color) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: pattern
  {
    out << "pattern: ";
    rosidl_generator_traits::value_to_yaml(msg.pattern, out);
    out << ", ";
  }

  // member: duration_sec
  {
    out << "duration_sec: ";
    rosidl_generator_traits::value_to_yaml(msg.duration_sec, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LEDAction & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: led_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "led_id: ";
    rosidl_generator_traits::value_to_yaml(msg.led_id, out);
    out << "\n";
  }

  // member: color
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.color.size() == 0) {
      out << "color: []\n";
    } else {
      out << "color:\n";
      for (auto item : msg.color) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: pattern
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pattern: ";
    rosidl_generator_traits::value_to_yaml(msg.pattern, out);
    out << "\n";
  }

  // member: duration_sec
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "duration_sec: ";
    rosidl_generator_traits::value_to_yaml(msg.duration_sec, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LEDAction & msg, bool use_flow_style = false)
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
  const aimee_msgs::msg::LEDAction & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::msg::LEDAction & msg)
{
  return aimee_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::msg::LEDAction>()
{
  return "aimee_msgs::msg::LEDAction";
}

template<>
inline const char * name<aimee_msgs::msg::LEDAction>()
{
  return "aimee_msgs/msg/LEDAction";
}

template<>
struct has_fixed_size<aimee_msgs::msg::LEDAction>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aimee_msgs::msg::LEDAction>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aimee_msgs::msg::LEDAction>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AIMEE_MSGS__MSG__DETAIL__LED_ACTION__TRAITS_HPP_
