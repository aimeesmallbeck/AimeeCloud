// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aimee_msgs:msg/Transcription.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__TRANSCRIPTION__TRAITS_HPP_
#define AIMEE_MSGS__MSG__DETAIL__TRANSCRIPTION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aimee_msgs/msg/detail/transcription__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace aimee_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const Transcription & msg,
  std::ostream & out)
{
  out << "{";
  // member: text
  {
    out << "text: ";
    rosidl_generator_traits::value_to_yaml(msg.text, out);
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

  // member: is_command
  {
    out << "is_command: ";
    rosidl_generator_traits::value_to_yaml(msg.is_command, out);
    out << ", ";
  }

  // member: is_partial
  {
    out << "is_partial: ";
    rosidl_generator_traits::value_to_yaml(msg.is_partial, out);
    out << ", ";
  }

  // member: wake_word_detected
  {
    out << "wake_word_detected: ";
    rosidl_generator_traits::value_to_yaml(msg.wake_word_detected, out);
    out << ", ";
  }

  // member: wake_word
  {
    out << "wake_word: ";
    rosidl_generator_traits::value_to_yaml(msg.wake_word, out);
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
    out << ", ";
  }

  // member: correlation_id
  {
    out << "correlation_id: ";
    rosidl_generator_traits::value_to_yaml(msg.correlation_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Transcription & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: text
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "text: ";
    rosidl_generator_traits::value_to_yaml(msg.text, out);
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

  // member: is_command
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_command: ";
    rosidl_generator_traits::value_to_yaml(msg.is_command, out);
    out << "\n";
  }

  // member: is_partial
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_partial: ";
    rosidl_generator_traits::value_to_yaml(msg.is_partial, out);
    out << "\n";
  }

  // member: wake_word_detected
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "wake_word_detected: ";
    rosidl_generator_traits::value_to_yaml(msg.wake_word_detected, out);
    out << "\n";
  }

  // member: wake_word
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "wake_word: ";
    rosidl_generator_traits::value_to_yaml(msg.wake_word, out);
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

  // member: correlation_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "correlation_id: ";
    rosidl_generator_traits::value_to_yaml(msg.correlation_id, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Transcription & msg, bool use_flow_style = false)
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
  const aimee_msgs::msg::Transcription & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::msg::Transcription & msg)
{
  return aimee_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::msg::Transcription>()
{
  return "aimee_msgs::msg::Transcription";
}

template<>
inline const char * name<aimee_msgs::msg::Transcription>()
{
  return "aimee_msgs/msg/Transcription";
}

template<>
struct has_fixed_size<aimee_msgs::msg::Transcription>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aimee_msgs::msg::Transcription>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aimee_msgs::msg::Transcription>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AIMEE_MSGS__MSG__DETAIL__TRANSCRIPTION__TRAITS_HPP_
