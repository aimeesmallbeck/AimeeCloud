// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from aimee_msgs:action/ExecuteSkill.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "aimee_msgs/action/detail/execute_skill__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace aimee_msgs
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

void ExecuteSkill_Goal_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) aimee_msgs::action::ExecuteSkill_Goal(_init);
}

void ExecuteSkill_Goal_fini_function(void * message_memory)
{
  auto typed_message = static_cast<aimee_msgs::action::ExecuteSkill_Goal *>(message_memory);
  typed_message->~ExecuteSkill_Goal();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ExecuteSkill_Goal_message_member_array[5] = {
  {
    "skill_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_Goal, skill_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "user_input",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_Goal, user_input),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "robot_state",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<aimee_msgs::msg::RobotState>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_Goal, robot_state),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "user_context",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_Goal, user_context),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "session_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_Goal, session_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ExecuteSkill_Goal_message_members = {
  "aimee_msgs::action",  // message namespace
  "ExecuteSkill_Goal",  // message name
  5,  // number of fields
  sizeof(aimee_msgs::action::ExecuteSkill_Goal),
  ExecuteSkill_Goal_message_member_array,  // message members
  ExecuteSkill_Goal_init_function,  // function to initialize message memory (memory has to be allocated)
  ExecuteSkill_Goal_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ExecuteSkill_Goal_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ExecuteSkill_Goal_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace aimee_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<aimee_msgs::action::ExecuteSkill_Goal>()
{
  return &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_Goal_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, aimee_msgs, action, ExecuteSkill_Goal)() {
  return &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_Goal_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "array"
// already included above
// #include "cstddef"
// already included above
// #include "string"
// already included above
// #include "vector"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/field_types.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace aimee_msgs
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

void ExecuteSkill_Result_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) aimee_msgs::action::ExecuteSkill_Result(_init);
}

void ExecuteSkill_Result_fini_function(void * message_memory)
{
  auto typed_message = static_cast<aimee_msgs::action::ExecuteSkill_Result *>(message_memory);
  typed_message->~ExecuteSkill_Result();
}

size_t size_function__ExecuteSkill_Result__motor_actions(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<aimee_msgs::msg::MotorAction> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ExecuteSkill_Result__motor_actions(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<aimee_msgs::msg::MotorAction> *>(untyped_member);
  return &member[index];
}

void * get_function__ExecuteSkill_Result__motor_actions(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<aimee_msgs::msg::MotorAction> *>(untyped_member);
  return &member[index];
}

void fetch_function__ExecuteSkill_Result__motor_actions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const aimee_msgs::msg::MotorAction *>(
    get_const_function__ExecuteSkill_Result__motor_actions(untyped_member, index));
  auto & value = *reinterpret_cast<aimee_msgs::msg::MotorAction *>(untyped_value);
  value = item;
}

void assign_function__ExecuteSkill_Result__motor_actions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<aimee_msgs::msg::MotorAction *>(
    get_function__ExecuteSkill_Result__motor_actions(untyped_member, index));
  const auto & value = *reinterpret_cast<const aimee_msgs::msg::MotorAction *>(untyped_value);
  item = value;
}

void resize_function__ExecuteSkill_Result__motor_actions(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<aimee_msgs::msg::MotorAction> *>(untyped_member);
  member->resize(size);
}

size_t size_function__ExecuteSkill_Result__camera_actions(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<aimee_msgs::msg::CameraAction> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ExecuteSkill_Result__camera_actions(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<aimee_msgs::msg::CameraAction> *>(untyped_member);
  return &member[index];
}

void * get_function__ExecuteSkill_Result__camera_actions(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<aimee_msgs::msg::CameraAction> *>(untyped_member);
  return &member[index];
}

void fetch_function__ExecuteSkill_Result__camera_actions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const aimee_msgs::msg::CameraAction *>(
    get_const_function__ExecuteSkill_Result__camera_actions(untyped_member, index));
  auto & value = *reinterpret_cast<aimee_msgs::msg::CameraAction *>(untyped_value);
  value = item;
}

void assign_function__ExecuteSkill_Result__camera_actions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<aimee_msgs::msg::CameraAction *>(
    get_function__ExecuteSkill_Result__camera_actions(untyped_member, index));
  const auto & value = *reinterpret_cast<const aimee_msgs::msg::CameraAction *>(untyped_value);
  item = value;
}

void resize_function__ExecuteSkill_Result__camera_actions(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<aimee_msgs::msg::CameraAction> *>(untyped_member);
  member->resize(size);
}

size_t size_function__ExecuteSkill_Result__led_actions(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<aimee_msgs::msg::LEDAction> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ExecuteSkill_Result__led_actions(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<aimee_msgs::msg::LEDAction> *>(untyped_member);
  return &member[index];
}

void * get_function__ExecuteSkill_Result__led_actions(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<aimee_msgs::msg::LEDAction> *>(untyped_member);
  return &member[index];
}

void fetch_function__ExecuteSkill_Result__led_actions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const aimee_msgs::msg::LEDAction *>(
    get_const_function__ExecuteSkill_Result__led_actions(untyped_member, index));
  auto & value = *reinterpret_cast<aimee_msgs::msg::LEDAction *>(untyped_value);
  value = item;
}

void assign_function__ExecuteSkill_Result__led_actions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<aimee_msgs::msg::LEDAction *>(
    get_function__ExecuteSkill_Result__led_actions(untyped_member, index));
  const auto & value = *reinterpret_cast<const aimee_msgs::msg::LEDAction *>(untyped_value);
  item = value;
}

void resize_function__ExecuteSkill_Result__led_actions(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<aimee_msgs::msg::LEDAction> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ExecuteSkill_Result_message_member_array[7] = {
  {
    "success",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_Result, success),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "response_text",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_Result, response_text),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "tts_audio_path",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_Result, tts_audio_path),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "error_message",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_Result, error_message),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "motor_actions",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<aimee_msgs::msg::MotorAction>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_Result, motor_actions),  // bytes offset in struct
    nullptr,  // default value
    size_function__ExecuteSkill_Result__motor_actions,  // size() function pointer
    get_const_function__ExecuteSkill_Result__motor_actions,  // get_const(index) function pointer
    get_function__ExecuteSkill_Result__motor_actions,  // get(index) function pointer
    fetch_function__ExecuteSkill_Result__motor_actions,  // fetch(index, &value) function pointer
    assign_function__ExecuteSkill_Result__motor_actions,  // assign(index, value) function pointer
    resize_function__ExecuteSkill_Result__motor_actions  // resize(index) function pointer
  },
  {
    "camera_actions",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<aimee_msgs::msg::CameraAction>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_Result, camera_actions),  // bytes offset in struct
    nullptr,  // default value
    size_function__ExecuteSkill_Result__camera_actions,  // size() function pointer
    get_const_function__ExecuteSkill_Result__camera_actions,  // get_const(index) function pointer
    get_function__ExecuteSkill_Result__camera_actions,  // get(index) function pointer
    fetch_function__ExecuteSkill_Result__camera_actions,  // fetch(index, &value) function pointer
    assign_function__ExecuteSkill_Result__camera_actions,  // assign(index, value) function pointer
    resize_function__ExecuteSkill_Result__camera_actions  // resize(index) function pointer
  },
  {
    "led_actions",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<aimee_msgs::msg::LEDAction>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_Result, led_actions),  // bytes offset in struct
    nullptr,  // default value
    size_function__ExecuteSkill_Result__led_actions,  // size() function pointer
    get_const_function__ExecuteSkill_Result__led_actions,  // get_const(index) function pointer
    get_function__ExecuteSkill_Result__led_actions,  // get(index) function pointer
    fetch_function__ExecuteSkill_Result__led_actions,  // fetch(index, &value) function pointer
    assign_function__ExecuteSkill_Result__led_actions,  // assign(index, value) function pointer
    resize_function__ExecuteSkill_Result__led_actions  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ExecuteSkill_Result_message_members = {
  "aimee_msgs::action",  // message namespace
  "ExecuteSkill_Result",  // message name
  7,  // number of fields
  sizeof(aimee_msgs::action::ExecuteSkill_Result),
  ExecuteSkill_Result_message_member_array,  // message members
  ExecuteSkill_Result_init_function,  // function to initialize message memory (memory has to be allocated)
  ExecuteSkill_Result_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ExecuteSkill_Result_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ExecuteSkill_Result_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace aimee_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<aimee_msgs::action::ExecuteSkill_Result>()
{
  return &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_Result_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, aimee_msgs, action, ExecuteSkill_Result)() {
  return &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_Result_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "array"
// already included above
// #include "cstddef"
// already included above
// #include "string"
// already included above
// #include "vector"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/field_types.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace aimee_msgs
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

void ExecuteSkill_Feedback_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) aimee_msgs::action::ExecuteSkill_Feedback(_init);
}

void ExecuteSkill_Feedback_fini_function(void * message_memory)
{
  auto typed_message = static_cast<aimee_msgs::action::ExecuteSkill_Feedback *>(message_memory);
  typed_message->~ExecuteSkill_Feedback();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ExecuteSkill_Feedback_message_member_array[4] = {
  {
    "status",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_Feedback, status),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "current_action",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_Feedback, current_action),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "progress",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_Feedback, progress),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "can_cancel",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_Feedback, can_cancel),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ExecuteSkill_Feedback_message_members = {
  "aimee_msgs::action",  // message namespace
  "ExecuteSkill_Feedback",  // message name
  4,  // number of fields
  sizeof(aimee_msgs::action::ExecuteSkill_Feedback),
  ExecuteSkill_Feedback_message_member_array,  // message members
  ExecuteSkill_Feedback_init_function,  // function to initialize message memory (memory has to be allocated)
  ExecuteSkill_Feedback_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ExecuteSkill_Feedback_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ExecuteSkill_Feedback_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace aimee_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<aimee_msgs::action::ExecuteSkill_Feedback>()
{
  return &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_Feedback_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, aimee_msgs, action, ExecuteSkill_Feedback)() {
  return &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_Feedback_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "array"
// already included above
// #include "cstddef"
// already included above
// #include "string"
// already included above
// #include "vector"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/field_types.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace aimee_msgs
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

void ExecuteSkill_SendGoal_Request_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) aimee_msgs::action::ExecuteSkill_SendGoal_Request(_init);
}

void ExecuteSkill_SendGoal_Request_fini_function(void * message_memory)
{
  auto typed_message = static_cast<aimee_msgs::action::ExecuteSkill_SendGoal_Request *>(message_memory);
  typed_message->~ExecuteSkill_SendGoal_Request();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ExecuteSkill_SendGoal_Request_message_member_array[2] = {
  {
    "goal_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<unique_identifier_msgs::msg::UUID>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_SendGoal_Request, goal_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "goal",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<aimee_msgs::action::ExecuteSkill_Goal>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_SendGoal_Request, goal),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ExecuteSkill_SendGoal_Request_message_members = {
  "aimee_msgs::action",  // message namespace
  "ExecuteSkill_SendGoal_Request",  // message name
  2,  // number of fields
  sizeof(aimee_msgs::action::ExecuteSkill_SendGoal_Request),
  ExecuteSkill_SendGoal_Request_message_member_array,  // message members
  ExecuteSkill_SendGoal_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  ExecuteSkill_SendGoal_Request_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ExecuteSkill_SendGoal_Request_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ExecuteSkill_SendGoal_Request_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace aimee_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<aimee_msgs::action::ExecuteSkill_SendGoal_Request>()
{
  return &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_SendGoal_Request_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, aimee_msgs, action, ExecuteSkill_SendGoal_Request)() {
  return &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_SendGoal_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "array"
// already included above
// #include "cstddef"
// already included above
// #include "string"
// already included above
// #include "vector"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/field_types.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace aimee_msgs
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

void ExecuteSkill_SendGoal_Response_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) aimee_msgs::action::ExecuteSkill_SendGoal_Response(_init);
}

void ExecuteSkill_SendGoal_Response_fini_function(void * message_memory)
{
  auto typed_message = static_cast<aimee_msgs::action::ExecuteSkill_SendGoal_Response *>(message_memory);
  typed_message->~ExecuteSkill_SendGoal_Response();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ExecuteSkill_SendGoal_Response_message_member_array[2] = {
  {
    "accepted",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_SendGoal_Response, accepted),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "stamp",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<builtin_interfaces::msg::Time>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_SendGoal_Response, stamp),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ExecuteSkill_SendGoal_Response_message_members = {
  "aimee_msgs::action",  // message namespace
  "ExecuteSkill_SendGoal_Response",  // message name
  2,  // number of fields
  sizeof(aimee_msgs::action::ExecuteSkill_SendGoal_Response),
  ExecuteSkill_SendGoal_Response_message_member_array,  // message members
  ExecuteSkill_SendGoal_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  ExecuteSkill_SendGoal_Response_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ExecuteSkill_SendGoal_Response_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ExecuteSkill_SendGoal_Response_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace aimee_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<aimee_msgs::action::ExecuteSkill_SendGoal_Response>()
{
  return &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_SendGoal_Response_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, aimee_msgs, action, ExecuteSkill_SendGoal_Response)() {
  return &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_SendGoal_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/service_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/service_type_support_decl.hpp"

namespace aimee_msgs
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

// this is intentionally not const to allow initialization later to prevent an initialization race
static ::rosidl_typesupport_introspection_cpp::ServiceMembers ExecuteSkill_SendGoal_service_members = {
  "aimee_msgs::action",  // service namespace
  "ExecuteSkill_SendGoal",  // service name
  // these two fields are initialized below on the first access
  // see get_service_type_support_handle<aimee_msgs::action::ExecuteSkill_SendGoal>()
  nullptr,  // request message
  nullptr  // response message
};

static const rosidl_service_type_support_t ExecuteSkill_SendGoal_service_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ExecuteSkill_SendGoal_service_members,
  get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace aimee_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<aimee_msgs::action::ExecuteSkill_SendGoal>()
{
  // get a handle to the value to be returned
  auto service_type_support =
    &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_SendGoal_service_type_support_handle;
  // get a non-const and properly typed version of the data void *
  auto service_members = const_cast<::rosidl_typesupport_introspection_cpp::ServiceMembers *>(
    static_cast<const ::rosidl_typesupport_introspection_cpp::ServiceMembers *>(
      service_type_support->data));
  // make sure that both the request_members_ and the response_members_ are initialized
  // if they are not, initialize them
  if (
    service_members->request_members_ == nullptr ||
    service_members->response_members_ == nullptr)
  {
    // initialize the request_members_ with the static function from the external library
    service_members->request_members_ = static_cast<
      const ::rosidl_typesupport_introspection_cpp::MessageMembers *
      >(
      ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<
        ::aimee_msgs::action::ExecuteSkill_SendGoal_Request
      >()->data
      );
    // initialize the response_members_ with the static function from the external library
    service_members->response_members_ = static_cast<
      const ::rosidl_typesupport_introspection_cpp::MessageMembers *
      >(
      ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<
        ::aimee_msgs::action::ExecuteSkill_SendGoal_Response
      >()->data
      );
  }
  // finally return the properly initialized service_type_support handle
  return service_type_support;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, aimee_msgs, action, ExecuteSkill_SendGoal)() {
  return ::rosidl_typesupport_introspection_cpp::get_service_type_support_handle<aimee_msgs::action::ExecuteSkill_SendGoal>();
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "array"
// already included above
// #include "cstddef"
// already included above
// #include "string"
// already included above
// #include "vector"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/field_types.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace aimee_msgs
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

void ExecuteSkill_GetResult_Request_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) aimee_msgs::action::ExecuteSkill_GetResult_Request(_init);
}

void ExecuteSkill_GetResult_Request_fini_function(void * message_memory)
{
  auto typed_message = static_cast<aimee_msgs::action::ExecuteSkill_GetResult_Request *>(message_memory);
  typed_message->~ExecuteSkill_GetResult_Request();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ExecuteSkill_GetResult_Request_message_member_array[1] = {
  {
    "goal_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<unique_identifier_msgs::msg::UUID>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_GetResult_Request, goal_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ExecuteSkill_GetResult_Request_message_members = {
  "aimee_msgs::action",  // message namespace
  "ExecuteSkill_GetResult_Request",  // message name
  1,  // number of fields
  sizeof(aimee_msgs::action::ExecuteSkill_GetResult_Request),
  ExecuteSkill_GetResult_Request_message_member_array,  // message members
  ExecuteSkill_GetResult_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  ExecuteSkill_GetResult_Request_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ExecuteSkill_GetResult_Request_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ExecuteSkill_GetResult_Request_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace aimee_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<aimee_msgs::action::ExecuteSkill_GetResult_Request>()
{
  return &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_GetResult_Request_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, aimee_msgs, action, ExecuteSkill_GetResult_Request)() {
  return &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_GetResult_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "array"
// already included above
// #include "cstddef"
// already included above
// #include "string"
// already included above
// #include "vector"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/field_types.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace aimee_msgs
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

void ExecuteSkill_GetResult_Response_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) aimee_msgs::action::ExecuteSkill_GetResult_Response(_init);
}

void ExecuteSkill_GetResult_Response_fini_function(void * message_memory)
{
  auto typed_message = static_cast<aimee_msgs::action::ExecuteSkill_GetResult_Response *>(message_memory);
  typed_message->~ExecuteSkill_GetResult_Response();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ExecuteSkill_GetResult_Response_message_member_array[2] = {
  {
    "status",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_GetResult_Response, status),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "result",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<aimee_msgs::action::ExecuteSkill_Result>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_GetResult_Response, result),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ExecuteSkill_GetResult_Response_message_members = {
  "aimee_msgs::action",  // message namespace
  "ExecuteSkill_GetResult_Response",  // message name
  2,  // number of fields
  sizeof(aimee_msgs::action::ExecuteSkill_GetResult_Response),
  ExecuteSkill_GetResult_Response_message_member_array,  // message members
  ExecuteSkill_GetResult_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  ExecuteSkill_GetResult_Response_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ExecuteSkill_GetResult_Response_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ExecuteSkill_GetResult_Response_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace aimee_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<aimee_msgs::action::ExecuteSkill_GetResult_Response>()
{
  return &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_GetResult_Response_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, aimee_msgs, action, ExecuteSkill_GetResult_Response)() {
  return &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_GetResult_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/service_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/service_type_support_decl.hpp"

namespace aimee_msgs
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

// this is intentionally not const to allow initialization later to prevent an initialization race
static ::rosidl_typesupport_introspection_cpp::ServiceMembers ExecuteSkill_GetResult_service_members = {
  "aimee_msgs::action",  // service namespace
  "ExecuteSkill_GetResult",  // service name
  // these two fields are initialized below on the first access
  // see get_service_type_support_handle<aimee_msgs::action::ExecuteSkill_GetResult>()
  nullptr,  // request message
  nullptr  // response message
};

static const rosidl_service_type_support_t ExecuteSkill_GetResult_service_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ExecuteSkill_GetResult_service_members,
  get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace aimee_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<aimee_msgs::action::ExecuteSkill_GetResult>()
{
  // get a handle to the value to be returned
  auto service_type_support =
    &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_GetResult_service_type_support_handle;
  // get a non-const and properly typed version of the data void *
  auto service_members = const_cast<::rosidl_typesupport_introspection_cpp::ServiceMembers *>(
    static_cast<const ::rosidl_typesupport_introspection_cpp::ServiceMembers *>(
      service_type_support->data));
  // make sure that both the request_members_ and the response_members_ are initialized
  // if they are not, initialize them
  if (
    service_members->request_members_ == nullptr ||
    service_members->response_members_ == nullptr)
  {
    // initialize the request_members_ with the static function from the external library
    service_members->request_members_ = static_cast<
      const ::rosidl_typesupport_introspection_cpp::MessageMembers *
      >(
      ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<
        ::aimee_msgs::action::ExecuteSkill_GetResult_Request
      >()->data
      );
    // initialize the response_members_ with the static function from the external library
    service_members->response_members_ = static_cast<
      const ::rosidl_typesupport_introspection_cpp::MessageMembers *
      >(
      ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<
        ::aimee_msgs::action::ExecuteSkill_GetResult_Response
      >()->data
      );
  }
  // finally return the properly initialized service_type_support handle
  return service_type_support;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, aimee_msgs, action, ExecuteSkill_GetResult)() {
  return ::rosidl_typesupport_introspection_cpp::get_service_type_support_handle<aimee_msgs::action::ExecuteSkill_GetResult>();
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "array"
// already included above
// #include "cstddef"
// already included above
// #include "string"
// already included above
// #include "vector"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/field_types.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace aimee_msgs
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

void ExecuteSkill_FeedbackMessage_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) aimee_msgs::action::ExecuteSkill_FeedbackMessage(_init);
}

void ExecuteSkill_FeedbackMessage_fini_function(void * message_memory)
{
  auto typed_message = static_cast<aimee_msgs::action::ExecuteSkill_FeedbackMessage *>(message_memory);
  typed_message->~ExecuteSkill_FeedbackMessage();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ExecuteSkill_FeedbackMessage_message_member_array[2] = {
  {
    "goal_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<unique_identifier_msgs::msg::UUID>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_FeedbackMessage, goal_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "feedback",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<aimee_msgs::action::ExecuteSkill_Feedback>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs::action::ExecuteSkill_FeedbackMessage, feedback),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ExecuteSkill_FeedbackMessage_message_members = {
  "aimee_msgs::action",  // message namespace
  "ExecuteSkill_FeedbackMessage",  // message name
  2,  // number of fields
  sizeof(aimee_msgs::action::ExecuteSkill_FeedbackMessage),
  ExecuteSkill_FeedbackMessage_message_member_array,  // message members
  ExecuteSkill_FeedbackMessage_init_function,  // function to initialize message memory (memory has to be allocated)
  ExecuteSkill_FeedbackMessage_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ExecuteSkill_FeedbackMessage_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ExecuteSkill_FeedbackMessage_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace aimee_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<aimee_msgs::action::ExecuteSkill_FeedbackMessage>()
{
  return &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_FeedbackMessage_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, aimee_msgs, action, ExecuteSkill_FeedbackMessage)() {
  return &::aimee_msgs::action::rosidl_typesupport_introspection_cpp::ExecuteSkill_FeedbackMessage_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
