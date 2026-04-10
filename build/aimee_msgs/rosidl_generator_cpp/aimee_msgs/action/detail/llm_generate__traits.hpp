// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aimee_msgs:action/LLMGenerate.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__ACTION__DETAIL__LLM_GENERATE__TRAITS_HPP_
#define AIMEE_MSGS__ACTION__DETAIL__LLM_GENERATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aimee_msgs/action/detail/llm_generate__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace aimee_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const LLMGenerate_Goal & msg,
  std::ostream & out)
{
  out << "{";
  // member: prompt
  {
    out << "prompt: ";
    rosidl_generator_traits::value_to_yaml(msg.prompt, out);
    out << ", ";
  }

  // member: system_context
  {
    out << "system_context: ";
    rosidl_generator_traits::value_to_yaml(msg.system_context, out);
    out << ", ";
  }

  // member: max_tokens
  {
    out << "max_tokens: ";
    rosidl_generator_traits::value_to_yaml(msg.max_tokens, out);
    out << ", ";
  }

  // member: temperature
  {
    out << "temperature: ";
    rosidl_generator_traits::value_to_yaml(msg.temperature, out);
    out << ", ";
  }

  // member: stream
  {
    out << "stream: ";
    rosidl_generator_traits::value_to_yaml(msg.stream, out);
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
  const LLMGenerate_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: prompt
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "prompt: ";
    rosidl_generator_traits::value_to_yaml(msg.prompt, out);
    out << "\n";
  }

  // member: system_context
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "system_context: ";
    rosidl_generator_traits::value_to_yaml(msg.system_context, out);
    out << "\n";
  }

  // member: max_tokens
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "max_tokens: ";
    rosidl_generator_traits::value_to_yaml(msg.max_tokens, out);
    out << "\n";
  }

  // member: temperature
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "temperature: ";
    rosidl_generator_traits::value_to_yaml(msg.temperature, out);
    out << "\n";
  }

  // member: stream
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stream: ";
    rosidl_generator_traits::value_to_yaml(msg.stream, out);
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
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LLMGenerate_Goal & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace aimee_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aimee_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aimee_msgs::action::LLMGenerate_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::action::LLMGenerate_Goal & msg)
{
  return aimee_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::action::LLMGenerate_Goal>()
{
  return "aimee_msgs::action::LLMGenerate_Goal";
}

template<>
inline const char * name<aimee_msgs::action::LLMGenerate_Goal>()
{
  return "aimee_msgs/action/LLMGenerate_Goal";
}

template<>
struct has_fixed_size<aimee_msgs::action::LLMGenerate_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aimee_msgs::action::LLMGenerate_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aimee_msgs::action::LLMGenerate_Goal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace aimee_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const LLMGenerate_Result & msg,
  std::ostream & out)
{
  out << "{";
  // member: response
  {
    out << "response: ";
    rosidl_generator_traits::value_to_yaml(msg.response, out);
    out << ", ";
  }

  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: error_message
  {
    out << "error_message: ";
    rosidl_generator_traits::value_to_yaml(msg.error_message, out);
    out << ", ";
  }

  // member: generation_time
  {
    out << "generation_time: ";
    rosidl_generator_traits::value_to_yaml(msg.generation_time, out);
    out << ", ";
  }

  // member: tokens_generated
  {
    out << "tokens_generated: ";
    rosidl_generator_traits::value_to_yaml(msg.tokens_generated, out);
    out << ", ";
  }

  // member: tokens_input
  {
    out << "tokens_input: ";
    rosidl_generator_traits::value_to_yaml(msg.tokens_input, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LLMGenerate_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "response: ";
    rosidl_generator_traits::value_to_yaml(msg.response, out);
    out << "\n";
  }

  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: error_message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "error_message: ";
    rosidl_generator_traits::value_to_yaml(msg.error_message, out);
    out << "\n";
  }

  // member: generation_time
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "generation_time: ";
    rosidl_generator_traits::value_to_yaml(msg.generation_time, out);
    out << "\n";
  }

  // member: tokens_generated
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tokens_generated: ";
    rosidl_generator_traits::value_to_yaml(msg.tokens_generated, out);
    out << "\n";
  }

  // member: tokens_input
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tokens_input: ";
    rosidl_generator_traits::value_to_yaml(msg.tokens_input, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LLMGenerate_Result & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace aimee_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aimee_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aimee_msgs::action::LLMGenerate_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::action::LLMGenerate_Result & msg)
{
  return aimee_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::action::LLMGenerate_Result>()
{
  return "aimee_msgs::action::LLMGenerate_Result";
}

template<>
inline const char * name<aimee_msgs::action::LLMGenerate_Result>()
{
  return "aimee_msgs/action/LLMGenerate_Result";
}

template<>
struct has_fixed_size<aimee_msgs::action::LLMGenerate_Result>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aimee_msgs::action::LLMGenerate_Result>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aimee_msgs::action::LLMGenerate_Result>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace aimee_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const LLMGenerate_Feedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: partial_response
  {
    out << "partial_response: ";
    rosidl_generator_traits::value_to_yaml(msg.partial_response, out);
    out << ", ";
  }

  // member: tokens_generated
  {
    out << "tokens_generated: ";
    rosidl_generator_traits::value_to_yaml(msg.tokens_generated, out);
    out << ", ";
  }

  // member: tokens_total
  {
    out << "tokens_total: ";
    rosidl_generator_traits::value_to_yaml(msg.tokens_total, out);
    out << ", ";
  }

  // member: is_complete
  {
    out << "is_complete: ";
    rosidl_generator_traits::value_to_yaml(msg.is_complete, out);
    out << ", ";
  }

  // member: current_word
  {
    out << "current_word: ";
    rosidl_generator_traits::value_to_yaml(msg.current_word, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LLMGenerate_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: partial_response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "partial_response: ";
    rosidl_generator_traits::value_to_yaml(msg.partial_response, out);
    out << "\n";
  }

  // member: tokens_generated
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tokens_generated: ";
    rosidl_generator_traits::value_to_yaml(msg.tokens_generated, out);
    out << "\n";
  }

  // member: tokens_total
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tokens_total: ";
    rosidl_generator_traits::value_to_yaml(msg.tokens_total, out);
    out << "\n";
  }

  // member: is_complete
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_complete: ";
    rosidl_generator_traits::value_to_yaml(msg.is_complete, out);
    out << "\n";
  }

  // member: current_word
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "current_word: ";
    rosidl_generator_traits::value_to_yaml(msg.current_word, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LLMGenerate_Feedback & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace aimee_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aimee_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aimee_msgs::action::LLMGenerate_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::action::LLMGenerate_Feedback & msg)
{
  return aimee_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::action::LLMGenerate_Feedback>()
{
  return "aimee_msgs::action::LLMGenerate_Feedback";
}

template<>
inline const char * name<aimee_msgs::action::LLMGenerate_Feedback>()
{
  return "aimee_msgs/action/LLMGenerate_Feedback";
}

template<>
struct has_fixed_size<aimee_msgs::action::LLMGenerate_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aimee_msgs::action::LLMGenerate_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aimee_msgs::action::LLMGenerate_Feedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'goal'
#include "aimee_msgs/action/detail/llm_generate__traits.hpp"

namespace aimee_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const LLMGenerate_SendGoal_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: goal
  {
    out << "goal: ";
    to_flow_style_yaml(msg.goal, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LLMGenerate_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: goal
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal:\n";
    to_block_style_yaml(msg.goal, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LLMGenerate_SendGoal_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace aimee_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aimee_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aimee_msgs::action::LLMGenerate_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::action::LLMGenerate_SendGoal_Request & msg)
{
  return aimee_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::action::LLMGenerate_SendGoal_Request>()
{
  return "aimee_msgs::action::LLMGenerate_SendGoal_Request";
}

template<>
inline const char * name<aimee_msgs::action::LLMGenerate_SendGoal_Request>()
{
  return "aimee_msgs/action/LLMGenerate_SendGoal_Request";
}

template<>
struct has_fixed_size<aimee_msgs::action::LLMGenerate_SendGoal_Request>
  : std::integral_constant<bool, has_fixed_size<aimee_msgs::action::LLMGenerate_Goal>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<aimee_msgs::action::LLMGenerate_SendGoal_Request>
  : std::integral_constant<bool, has_bounded_size<aimee_msgs::action::LLMGenerate_Goal>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<aimee_msgs::action::LLMGenerate_SendGoal_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace aimee_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const LLMGenerate_SendGoal_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LLMGenerate_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LLMGenerate_SendGoal_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace aimee_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aimee_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aimee_msgs::action::LLMGenerate_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::action::LLMGenerate_SendGoal_Response & msg)
{
  return aimee_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::action::LLMGenerate_SendGoal_Response>()
{
  return "aimee_msgs::action::LLMGenerate_SendGoal_Response";
}

template<>
inline const char * name<aimee_msgs::action::LLMGenerate_SendGoal_Response>()
{
  return "aimee_msgs/action/LLMGenerate_SendGoal_Response";
}

template<>
struct has_fixed_size<aimee_msgs::action::LLMGenerate_SendGoal_Response>
  : std::integral_constant<bool, has_fixed_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct has_bounded_size<aimee_msgs::action::LLMGenerate_SendGoal_Response>
  : std::integral_constant<bool, has_bounded_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct is_message<aimee_msgs::action::LLMGenerate_SendGoal_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<aimee_msgs::action::LLMGenerate_SendGoal>()
{
  return "aimee_msgs::action::LLMGenerate_SendGoal";
}

template<>
inline const char * name<aimee_msgs::action::LLMGenerate_SendGoal>()
{
  return "aimee_msgs/action/LLMGenerate_SendGoal";
}

template<>
struct has_fixed_size<aimee_msgs::action::LLMGenerate_SendGoal>
  : std::integral_constant<
    bool,
    has_fixed_size<aimee_msgs::action::LLMGenerate_SendGoal_Request>::value &&
    has_fixed_size<aimee_msgs::action::LLMGenerate_SendGoal_Response>::value
  >
{
};

template<>
struct has_bounded_size<aimee_msgs::action::LLMGenerate_SendGoal>
  : std::integral_constant<
    bool,
    has_bounded_size<aimee_msgs::action::LLMGenerate_SendGoal_Request>::value &&
    has_bounded_size<aimee_msgs::action::LLMGenerate_SendGoal_Response>::value
  >
{
};

template<>
struct is_service<aimee_msgs::action::LLMGenerate_SendGoal>
  : std::true_type
{
};

template<>
struct is_service_request<aimee_msgs::action::LLMGenerate_SendGoal_Request>
  : std::true_type
{
};

template<>
struct is_service_response<aimee_msgs::action::LLMGenerate_SendGoal_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"

namespace aimee_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const LLMGenerate_GetResult_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LLMGenerate_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LLMGenerate_GetResult_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace aimee_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aimee_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aimee_msgs::action::LLMGenerate_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::action::LLMGenerate_GetResult_Request & msg)
{
  return aimee_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::action::LLMGenerate_GetResult_Request>()
{
  return "aimee_msgs::action::LLMGenerate_GetResult_Request";
}

template<>
inline const char * name<aimee_msgs::action::LLMGenerate_GetResult_Request>()
{
  return "aimee_msgs/action/LLMGenerate_GetResult_Request";
}

template<>
struct has_fixed_size<aimee_msgs::action::LLMGenerate_GetResult_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<aimee_msgs::action::LLMGenerate_GetResult_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<aimee_msgs::action::LLMGenerate_GetResult_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
// already included above
// #include "aimee_msgs/action/detail/llm_generate__traits.hpp"

namespace aimee_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const LLMGenerate_GetResult_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: result
  {
    out << "result: ";
    to_flow_style_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LLMGenerate_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result:\n";
    to_block_style_yaml(msg.result, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LLMGenerate_GetResult_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace aimee_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aimee_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aimee_msgs::action::LLMGenerate_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::action::LLMGenerate_GetResult_Response & msg)
{
  return aimee_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::action::LLMGenerate_GetResult_Response>()
{
  return "aimee_msgs::action::LLMGenerate_GetResult_Response";
}

template<>
inline const char * name<aimee_msgs::action::LLMGenerate_GetResult_Response>()
{
  return "aimee_msgs/action/LLMGenerate_GetResult_Response";
}

template<>
struct has_fixed_size<aimee_msgs::action::LLMGenerate_GetResult_Response>
  : std::integral_constant<bool, has_fixed_size<aimee_msgs::action::LLMGenerate_Result>::value> {};

template<>
struct has_bounded_size<aimee_msgs::action::LLMGenerate_GetResult_Response>
  : std::integral_constant<bool, has_bounded_size<aimee_msgs::action::LLMGenerate_Result>::value> {};

template<>
struct is_message<aimee_msgs::action::LLMGenerate_GetResult_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<aimee_msgs::action::LLMGenerate_GetResult>()
{
  return "aimee_msgs::action::LLMGenerate_GetResult";
}

template<>
inline const char * name<aimee_msgs::action::LLMGenerate_GetResult>()
{
  return "aimee_msgs/action/LLMGenerate_GetResult";
}

template<>
struct has_fixed_size<aimee_msgs::action::LLMGenerate_GetResult>
  : std::integral_constant<
    bool,
    has_fixed_size<aimee_msgs::action::LLMGenerate_GetResult_Request>::value &&
    has_fixed_size<aimee_msgs::action::LLMGenerate_GetResult_Response>::value
  >
{
};

template<>
struct has_bounded_size<aimee_msgs::action::LLMGenerate_GetResult>
  : std::integral_constant<
    bool,
    has_bounded_size<aimee_msgs::action::LLMGenerate_GetResult_Request>::value &&
    has_bounded_size<aimee_msgs::action::LLMGenerate_GetResult_Response>::value
  >
{
};

template<>
struct is_service<aimee_msgs::action::LLMGenerate_GetResult>
  : std::true_type
{
};

template<>
struct is_service_request<aimee_msgs::action::LLMGenerate_GetResult_Request>
  : std::true_type
{
};

template<>
struct is_service_response<aimee_msgs::action::LLMGenerate_GetResult_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'feedback'
// already included above
// #include "aimee_msgs/action/detail/llm_generate__traits.hpp"

namespace aimee_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const LLMGenerate_FeedbackMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: feedback
  {
    out << "feedback: ";
    to_flow_style_yaml(msg.feedback, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LLMGenerate_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback:\n";
    to_block_style_yaml(msg.feedback, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LLMGenerate_FeedbackMessage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace aimee_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aimee_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aimee_msgs::action::LLMGenerate_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::action::LLMGenerate_FeedbackMessage & msg)
{
  return aimee_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::action::LLMGenerate_FeedbackMessage>()
{
  return "aimee_msgs::action::LLMGenerate_FeedbackMessage";
}

template<>
inline const char * name<aimee_msgs::action::LLMGenerate_FeedbackMessage>()
{
  return "aimee_msgs/action/LLMGenerate_FeedbackMessage";
}

template<>
struct has_fixed_size<aimee_msgs::action::LLMGenerate_FeedbackMessage>
  : std::integral_constant<bool, has_fixed_size<aimee_msgs::action::LLMGenerate_Feedback>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<aimee_msgs::action::LLMGenerate_FeedbackMessage>
  : std::integral_constant<bool, has_bounded_size<aimee_msgs::action::LLMGenerate_Feedback>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<aimee_msgs::action::LLMGenerate_FeedbackMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits


namespace rosidl_generator_traits
{

template<>
struct is_action<aimee_msgs::action::LLMGenerate>
  : std::true_type
{
};

template<>
struct is_action_goal<aimee_msgs::action::LLMGenerate_Goal>
  : std::true_type
{
};

template<>
struct is_action_result<aimee_msgs::action::LLMGenerate_Result>
  : std::true_type
{
};

template<>
struct is_action_feedback<aimee_msgs::action::LLMGenerate_Feedback>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits


#endif  // AIMEE_MSGS__ACTION__DETAIL__LLM_GENERATE__TRAITS_HPP_
