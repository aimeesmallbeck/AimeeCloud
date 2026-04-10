// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aimee_msgs:action/ExecuteSkill.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__ACTION__DETAIL__EXECUTE_SKILL__TRAITS_HPP_
#define AIMEE_MSGS__ACTION__DETAIL__EXECUTE_SKILL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aimee_msgs/action/detail/execute_skill__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'robot_state'
#include "aimee_msgs/msg/detail/robot_state__traits.hpp"

namespace aimee_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const ExecuteSkill_Goal & msg,
  std::ostream & out)
{
  out << "{";
  // member: skill_id
  {
    out << "skill_id: ";
    rosidl_generator_traits::value_to_yaml(msg.skill_id, out);
    out << ", ";
  }

  // member: user_input
  {
    out << "user_input: ";
    rosidl_generator_traits::value_to_yaml(msg.user_input, out);
    out << ", ";
  }

  // member: robot_state
  {
    out << "robot_state: ";
    to_flow_style_yaml(msg.robot_state, out);
    out << ", ";
  }

  // member: user_context
  {
    out << "user_context: ";
    rosidl_generator_traits::value_to_yaml(msg.user_context, out);
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
  const ExecuteSkill_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: skill_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "skill_id: ";
    rosidl_generator_traits::value_to_yaml(msg.skill_id, out);
    out << "\n";
  }

  // member: user_input
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "user_input: ";
    rosidl_generator_traits::value_to_yaml(msg.user_input, out);
    out << "\n";
  }

  // member: robot_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "robot_state:\n";
    to_block_style_yaml(msg.robot_state, out, indentation + 2);
  }

  // member: user_context
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "user_context: ";
    rosidl_generator_traits::value_to_yaml(msg.user_context, out);
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

inline std::string to_yaml(const ExecuteSkill_Goal & msg, bool use_flow_style = false)
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
  const aimee_msgs::action::ExecuteSkill_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::action::ExecuteSkill_Goal & msg)
{
  return aimee_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::action::ExecuteSkill_Goal>()
{
  return "aimee_msgs::action::ExecuteSkill_Goal";
}

template<>
inline const char * name<aimee_msgs::action::ExecuteSkill_Goal>()
{
  return "aimee_msgs/action/ExecuteSkill_Goal";
}

template<>
struct has_fixed_size<aimee_msgs::action::ExecuteSkill_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aimee_msgs::action::ExecuteSkill_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aimee_msgs::action::ExecuteSkill_Goal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'motor_actions'
#include "aimee_msgs/msg/detail/motor_action__traits.hpp"
// Member 'camera_actions'
#include "aimee_msgs/msg/detail/camera_action__traits.hpp"
// Member 'led_actions'
#include "aimee_msgs/msg/detail/led_action__traits.hpp"

namespace aimee_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const ExecuteSkill_Result & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: response_text
  {
    out << "response_text: ";
    rosidl_generator_traits::value_to_yaml(msg.response_text, out);
    out << ", ";
  }

  // member: tts_audio_path
  {
    out << "tts_audio_path: ";
    rosidl_generator_traits::value_to_yaml(msg.tts_audio_path, out);
    out << ", ";
  }

  // member: error_message
  {
    out << "error_message: ";
    rosidl_generator_traits::value_to_yaml(msg.error_message, out);
    out << ", ";
  }

  // member: motor_actions
  {
    if (msg.motor_actions.size() == 0) {
      out << "motor_actions: []";
    } else {
      out << "motor_actions: [";
      size_t pending_items = msg.motor_actions.size();
      for (auto item : msg.motor_actions) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: camera_actions
  {
    if (msg.camera_actions.size() == 0) {
      out << "camera_actions: []";
    } else {
      out << "camera_actions: [";
      size_t pending_items = msg.camera_actions.size();
      for (auto item : msg.camera_actions) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: led_actions
  {
    if (msg.led_actions.size() == 0) {
      out << "led_actions: []";
    } else {
      out << "led_actions: [";
      size_t pending_items = msg.led_actions.size();
      for (auto item : msg.led_actions) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ExecuteSkill_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: response_text
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "response_text: ";
    rosidl_generator_traits::value_to_yaml(msg.response_text, out);
    out << "\n";
  }

  // member: tts_audio_path
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tts_audio_path: ";
    rosidl_generator_traits::value_to_yaml(msg.tts_audio_path, out);
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

  // member: motor_actions
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.motor_actions.size() == 0) {
      out << "motor_actions: []\n";
    } else {
      out << "motor_actions:\n";
      for (auto item : msg.motor_actions) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: camera_actions
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.camera_actions.size() == 0) {
      out << "camera_actions: []\n";
    } else {
      out << "camera_actions:\n";
      for (auto item : msg.camera_actions) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: led_actions
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.led_actions.size() == 0) {
      out << "led_actions: []\n";
    } else {
      out << "led_actions:\n";
      for (auto item : msg.led_actions) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ExecuteSkill_Result & msg, bool use_flow_style = false)
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
  const aimee_msgs::action::ExecuteSkill_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::action::ExecuteSkill_Result & msg)
{
  return aimee_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::action::ExecuteSkill_Result>()
{
  return "aimee_msgs::action::ExecuteSkill_Result";
}

template<>
inline const char * name<aimee_msgs::action::ExecuteSkill_Result>()
{
  return "aimee_msgs/action/ExecuteSkill_Result";
}

template<>
struct has_fixed_size<aimee_msgs::action::ExecuteSkill_Result>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aimee_msgs::action::ExecuteSkill_Result>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aimee_msgs::action::ExecuteSkill_Result>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace aimee_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const ExecuteSkill_Feedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: current_action
  {
    out << "current_action: ";
    rosidl_generator_traits::value_to_yaml(msg.current_action, out);
    out << ", ";
  }

  // member: progress
  {
    out << "progress: ";
    rosidl_generator_traits::value_to_yaml(msg.progress, out);
    out << ", ";
  }

  // member: can_cancel
  {
    out << "can_cancel: ";
    rosidl_generator_traits::value_to_yaml(msg.can_cancel, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ExecuteSkill_Feedback & msg,
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

  // member: current_action
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "current_action: ";
    rosidl_generator_traits::value_to_yaml(msg.current_action, out);
    out << "\n";
  }

  // member: progress
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "progress: ";
    rosidl_generator_traits::value_to_yaml(msg.progress, out);
    out << "\n";
  }

  // member: can_cancel
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "can_cancel: ";
    rosidl_generator_traits::value_to_yaml(msg.can_cancel, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ExecuteSkill_Feedback & msg, bool use_flow_style = false)
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
  const aimee_msgs::action::ExecuteSkill_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::action::ExecuteSkill_Feedback & msg)
{
  return aimee_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::action::ExecuteSkill_Feedback>()
{
  return "aimee_msgs::action::ExecuteSkill_Feedback";
}

template<>
inline const char * name<aimee_msgs::action::ExecuteSkill_Feedback>()
{
  return "aimee_msgs/action/ExecuteSkill_Feedback";
}

template<>
struct has_fixed_size<aimee_msgs::action::ExecuteSkill_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aimee_msgs::action::ExecuteSkill_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aimee_msgs::action::ExecuteSkill_Feedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'goal'
#include "aimee_msgs/action/detail/execute_skill__traits.hpp"

namespace aimee_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const ExecuteSkill_SendGoal_Request & msg,
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
  const ExecuteSkill_SendGoal_Request & msg,
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

inline std::string to_yaml(const ExecuteSkill_SendGoal_Request & msg, bool use_flow_style = false)
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
  const aimee_msgs::action::ExecuteSkill_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::action::ExecuteSkill_SendGoal_Request & msg)
{
  return aimee_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::action::ExecuteSkill_SendGoal_Request>()
{
  return "aimee_msgs::action::ExecuteSkill_SendGoal_Request";
}

template<>
inline const char * name<aimee_msgs::action::ExecuteSkill_SendGoal_Request>()
{
  return "aimee_msgs/action/ExecuteSkill_SendGoal_Request";
}

template<>
struct has_fixed_size<aimee_msgs::action::ExecuteSkill_SendGoal_Request>
  : std::integral_constant<bool, has_fixed_size<aimee_msgs::action::ExecuteSkill_Goal>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<aimee_msgs::action::ExecuteSkill_SendGoal_Request>
  : std::integral_constant<bool, has_bounded_size<aimee_msgs::action::ExecuteSkill_Goal>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<aimee_msgs::action::ExecuteSkill_SendGoal_Request>
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
  const ExecuteSkill_SendGoal_Response & msg,
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
  const ExecuteSkill_SendGoal_Response & msg,
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

inline std::string to_yaml(const ExecuteSkill_SendGoal_Response & msg, bool use_flow_style = false)
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
  const aimee_msgs::action::ExecuteSkill_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::action::ExecuteSkill_SendGoal_Response & msg)
{
  return aimee_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::action::ExecuteSkill_SendGoal_Response>()
{
  return "aimee_msgs::action::ExecuteSkill_SendGoal_Response";
}

template<>
inline const char * name<aimee_msgs::action::ExecuteSkill_SendGoal_Response>()
{
  return "aimee_msgs/action/ExecuteSkill_SendGoal_Response";
}

template<>
struct has_fixed_size<aimee_msgs::action::ExecuteSkill_SendGoal_Response>
  : std::integral_constant<bool, has_fixed_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct has_bounded_size<aimee_msgs::action::ExecuteSkill_SendGoal_Response>
  : std::integral_constant<bool, has_bounded_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct is_message<aimee_msgs::action::ExecuteSkill_SendGoal_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<aimee_msgs::action::ExecuteSkill_SendGoal>()
{
  return "aimee_msgs::action::ExecuteSkill_SendGoal";
}

template<>
inline const char * name<aimee_msgs::action::ExecuteSkill_SendGoal>()
{
  return "aimee_msgs/action/ExecuteSkill_SendGoal";
}

template<>
struct has_fixed_size<aimee_msgs::action::ExecuteSkill_SendGoal>
  : std::integral_constant<
    bool,
    has_fixed_size<aimee_msgs::action::ExecuteSkill_SendGoal_Request>::value &&
    has_fixed_size<aimee_msgs::action::ExecuteSkill_SendGoal_Response>::value
  >
{
};

template<>
struct has_bounded_size<aimee_msgs::action::ExecuteSkill_SendGoal>
  : std::integral_constant<
    bool,
    has_bounded_size<aimee_msgs::action::ExecuteSkill_SendGoal_Request>::value &&
    has_bounded_size<aimee_msgs::action::ExecuteSkill_SendGoal_Response>::value
  >
{
};

template<>
struct is_service<aimee_msgs::action::ExecuteSkill_SendGoal>
  : std::true_type
{
};

template<>
struct is_service_request<aimee_msgs::action::ExecuteSkill_SendGoal_Request>
  : std::true_type
{
};

template<>
struct is_service_response<aimee_msgs::action::ExecuteSkill_SendGoal_Response>
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
  const ExecuteSkill_GetResult_Request & msg,
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
  const ExecuteSkill_GetResult_Request & msg,
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

inline std::string to_yaml(const ExecuteSkill_GetResult_Request & msg, bool use_flow_style = false)
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
  const aimee_msgs::action::ExecuteSkill_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::action::ExecuteSkill_GetResult_Request & msg)
{
  return aimee_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::action::ExecuteSkill_GetResult_Request>()
{
  return "aimee_msgs::action::ExecuteSkill_GetResult_Request";
}

template<>
inline const char * name<aimee_msgs::action::ExecuteSkill_GetResult_Request>()
{
  return "aimee_msgs/action/ExecuteSkill_GetResult_Request";
}

template<>
struct has_fixed_size<aimee_msgs::action::ExecuteSkill_GetResult_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<aimee_msgs::action::ExecuteSkill_GetResult_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<aimee_msgs::action::ExecuteSkill_GetResult_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
// already included above
// #include "aimee_msgs/action/detail/execute_skill__traits.hpp"

namespace aimee_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const ExecuteSkill_GetResult_Response & msg,
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
  const ExecuteSkill_GetResult_Response & msg,
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

inline std::string to_yaml(const ExecuteSkill_GetResult_Response & msg, bool use_flow_style = false)
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
  const aimee_msgs::action::ExecuteSkill_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::action::ExecuteSkill_GetResult_Response & msg)
{
  return aimee_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::action::ExecuteSkill_GetResult_Response>()
{
  return "aimee_msgs::action::ExecuteSkill_GetResult_Response";
}

template<>
inline const char * name<aimee_msgs::action::ExecuteSkill_GetResult_Response>()
{
  return "aimee_msgs/action/ExecuteSkill_GetResult_Response";
}

template<>
struct has_fixed_size<aimee_msgs::action::ExecuteSkill_GetResult_Response>
  : std::integral_constant<bool, has_fixed_size<aimee_msgs::action::ExecuteSkill_Result>::value> {};

template<>
struct has_bounded_size<aimee_msgs::action::ExecuteSkill_GetResult_Response>
  : std::integral_constant<bool, has_bounded_size<aimee_msgs::action::ExecuteSkill_Result>::value> {};

template<>
struct is_message<aimee_msgs::action::ExecuteSkill_GetResult_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<aimee_msgs::action::ExecuteSkill_GetResult>()
{
  return "aimee_msgs::action::ExecuteSkill_GetResult";
}

template<>
inline const char * name<aimee_msgs::action::ExecuteSkill_GetResult>()
{
  return "aimee_msgs/action/ExecuteSkill_GetResult";
}

template<>
struct has_fixed_size<aimee_msgs::action::ExecuteSkill_GetResult>
  : std::integral_constant<
    bool,
    has_fixed_size<aimee_msgs::action::ExecuteSkill_GetResult_Request>::value &&
    has_fixed_size<aimee_msgs::action::ExecuteSkill_GetResult_Response>::value
  >
{
};

template<>
struct has_bounded_size<aimee_msgs::action::ExecuteSkill_GetResult>
  : std::integral_constant<
    bool,
    has_bounded_size<aimee_msgs::action::ExecuteSkill_GetResult_Request>::value &&
    has_bounded_size<aimee_msgs::action::ExecuteSkill_GetResult_Response>::value
  >
{
};

template<>
struct is_service<aimee_msgs::action::ExecuteSkill_GetResult>
  : std::true_type
{
};

template<>
struct is_service_request<aimee_msgs::action::ExecuteSkill_GetResult_Request>
  : std::true_type
{
};

template<>
struct is_service_response<aimee_msgs::action::ExecuteSkill_GetResult_Response>
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
// #include "aimee_msgs/action/detail/execute_skill__traits.hpp"

namespace aimee_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const ExecuteSkill_FeedbackMessage & msg,
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
  const ExecuteSkill_FeedbackMessage & msg,
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

inline std::string to_yaml(const ExecuteSkill_FeedbackMessage & msg, bool use_flow_style = false)
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
  const aimee_msgs::action::ExecuteSkill_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::action::ExecuteSkill_FeedbackMessage & msg)
{
  return aimee_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::action::ExecuteSkill_FeedbackMessage>()
{
  return "aimee_msgs::action::ExecuteSkill_FeedbackMessage";
}

template<>
inline const char * name<aimee_msgs::action::ExecuteSkill_FeedbackMessage>()
{
  return "aimee_msgs/action/ExecuteSkill_FeedbackMessage";
}

template<>
struct has_fixed_size<aimee_msgs::action::ExecuteSkill_FeedbackMessage>
  : std::integral_constant<bool, has_fixed_size<aimee_msgs::action::ExecuteSkill_Feedback>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<aimee_msgs::action::ExecuteSkill_FeedbackMessage>
  : std::integral_constant<bool, has_bounded_size<aimee_msgs::action::ExecuteSkill_Feedback>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<aimee_msgs::action::ExecuteSkill_FeedbackMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits


namespace rosidl_generator_traits
{

template<>
struct is_action<aimee_msgs::action::ExecuteSkill>
  : std::true_type
{
};

template<>
struct is_action_goal<aimee_msgs::action::ExecuteSkill_Goal>
  : std::true_type
{
};

template<>
struct is_action_result<aimee_msgs::action::ExecuteSkill_Result>
  : std::true_type
{
};

template<>
struct is_action_feedback<aimee_msgs::action::ExecuteSkill_Feedback>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits


#endif  // AIMEE_MSGS__ACTION__DETAIL__EXECUTE_SKILL__TRAITS_HPP_
