// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aimee_msgs:msg/Intent.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__INTENT__TRAITS_HPP_
#define AIMEE_MSGS__MSG__DETAIL__INTENT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aimee_msgs/msg/detail/intent__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace aimee_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const Intent & msg,
  std::ostream & out)
{
  out << "{";
  // member: intent_type
  {
    out << "intent_type: ";
    rosidl_generator_traits::value_to_yaml(msg.intent_type, out);
    out << ", ";
  }

  // member: action
  {
    out << "action: ";
    rosidl_generator_traits::value_to_yaml(msg.action, out);
    out << ", ";
  }

  // member: confidence
  {
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << ", ";
  }

  // member: raw_text
  {
    out << "raw_text: ";
    rosidl_generator_traits::value_to_yaml(msg.raw_text, out);
    out << ", ";
  }

  // member: requires_skill
  {
    out << "requires_skill: ";
    rosidl_generator_traits::value_to_yaml(msg.requires_skill, out);
    out << ", ";
  }

  // member: skill_name
  {
    out << "skill_name: ";
    rosidl_generator_traits::value_to_yaml(msg.skill_name, out);
    out << ", ";
  }

  // member: parameters_json
  {
    out << "parameters_json: ";
    rosidl_generator_traits::value_to_yaml(msg.parameters_json, out);
    out << ", ";
  }

  // member: session_id
  {
    out << "session_id: ";
    rosidl_generator_traits::value_to_yaml(msg.session_id, out);
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
  const Intent & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: intent_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "intent_type: ";
    rosidl_generator_traits::value_to_yaml(msg.intent_type, out);
    out << "\n";
  }

  // member: action
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "action: ";
    rosidl_generator_traits::value_to_yaml(msg.action, out);
    out << "\n";
  }

  // member: confidence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << "\n";
  }

  // member: raw_text
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "raw_text: ";
    rosidl_generator_traits::value_to_yaml(msg.raw_text, out);
    out << "\n";
  }

  // member: requires_skill
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "requires_skill: ";
    rosidl_generator_traits::value_to_yaml(msg.requires_skill, out);
    out << "\n";
  }

  // member: skill_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "skill_name: ";
    rosidl_generator_traits::value_to_yaml(msg.skill_name, out);
    out << "\n";
  }

  // member: parameters_json
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "parameters_json: ";
    rosidl_generator_traits::value_to_yaml(msg.parameters_json, out);
    out << "\n";
  }

  // member: session_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "session_id: ";
    rosidl_generator_traits::value_to_yaml(msg.session_id, out);
    out << "\n";
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

inline std::string to_yaml(const Intent & msg, bool use_flow_style = false)
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
  const aimee_msgs::msg::Intent & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::msg::Intent & msg)
{
  return aimee_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::msg::Intent>()
{
  return "aimee_msgs::msg::Intent";
}

template<>
inline const char * name<aimee_msgs::msg::Intent>()
{
  return "aimee_msgs/msg/Intent";
}

template<>
struct has_fixed_size<aimee_msgs::msg::Intent>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aimee_msgs::msg::Intent>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aimee_msgs::msg::Intent>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AIMEE_MSGS__MSG__DETAIL__INTENT__TRAITS_HPP_
