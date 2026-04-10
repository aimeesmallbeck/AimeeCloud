// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aimee_msgs:msg/WakeWordDetection.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__WAKE_WORD_DETECTION__TRAITS_HPP_
#define AIMEE_MSGS__MSG__DETAIL__WAKE_WORD_DETECTION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aimee_msgs/msg/detail/wake_word_detection__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace aimee_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const WakeWordDetection & msg,
  std::ostream & out)
{
  out << "{";
  // member: wake_word
  {
    out << "wake_word: ";
    rosidl_generator_traits::value_to_yaml(msg.wake_word, out);
    out << ", ";
  }

  // member: confidence
  {
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << ", ";
  }

  // member: source
  {
    out << "source: ";
    rosidl_generator_traits::value_to_yaml(msg.source, out);
    out << ", ";
  }

  // member: sample_index
  {
    out << "sample_index: ";
    rosidl_generator_traits::value_to_yaml(msg.sample_index, out);
    out << ", ";
  }

  // member: signal_energy
  {
    out << "signal_energy: ";
    rosidl_generator_traits::value_to_yaml(msg.signal_energy, out);
    out << ", ";
  }

  // member: active
  {
    out << "active: ";
    rosidl_generator_traits::value_to_yaml(msg.active, out);
    out << ", ";
  }

  // member: timestamp
  {
    out << "timestamp: ";
    to_flow_style_yaml(msg.timestamp, out);
    out << ", ";
  }

  // member: session_id
  {
    out << "session_id: ";
    rosidl_generator_traits::value_to_yaml(msg.session_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const WakeWordDetection & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: wake_word
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "wake_word: ";
    rosidl_generator_traits::value_to_yaml(msg.wake_word, out);
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

  // member: source
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "source: ";
    rosidl_generator_traits::value_to_yaml(msg.source, out);
    out << "\n";
  }

  // member: sample_index
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sample_index: ";
    rosidl_generator_traits::value_to_yaml(msg.sample_index, out);
    out << "\n";
  }

  // member: signal_energy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "signal_energy: ";
    rosidl_generator_traits::value_to_yaml(msg.signal_energy, out);
    out << "\n";
  }

  // member: active
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "active: ";
    rosidl_generator_traits::value_to_yaml(msg.active, out);
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

  // member: session_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "session_id: ";
    rosidl_generator_traits::value_to_yaml(msg.session_id, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const WakeWordDetection & msg, bool use_flow_style = false)
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
  const aimee_msgs::msg::WakeWordDetection & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::msg::WakeWordDetection & msg)
{
  return aimee_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::msg::WakeWordDetection>()
{
  return "aimee_msgs::msg::WakeWordDetection";
}

template<>
inline const char * name<aimee_msgs::msg::WakeWordDetection>()
{
  return "aimee_msgs/msg/WakeWordDetection";
}

template<>
struct has_fixed_size<aimee_msgs::msg::WakeWordDetection>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aimee_msgs::msg::WakeWordDetection>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aimee_msgs::msg::WakeWordDetection>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AIMEE_MSGS__MSG__DETAIL__WAKE_WORD_DETECTION__TRAITS_HPP_
