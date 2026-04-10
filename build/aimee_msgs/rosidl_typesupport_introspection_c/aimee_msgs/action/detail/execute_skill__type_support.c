// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from aimee_msgs:action/ExecuteSkill.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "aimee_msgs/action/detail/execute_skill__rosidl_typesupport_introspection_c.h"
#include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "aimee_msgs/action/detail/execute_skill__functions.h"
#include "aimee_msgs/action/detail/execute_skill__struct.h"


// Include directives for member types
// Member `skill_id`
// Member `user_input`
// Member `user_context`
// Member `session_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `robot_state`
#include "aimee_msgs/msg/robot_state.h"
// Member `robot_state`
#include "aimee_msgs/msg/detail/robot_state__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__action__ExecuteSkill_Goal__rosidl_typesupport_introspection_c__ExecuteSkill_Goal_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__action__ExecuteSkill_Goal__init(message_memory);
}

void aimee_msgs__action__ExecuteSkill_Goal__rosidl_typesupport_introspection_c__ExecuteSkill_Goal_fini_function(void * message_memory)
{
  aimee_msgs__action__ExecuteSkill_Goal__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__action__ExecuteSkill_Goal__rosidl_typesupport_introspection_c__ExecuteSkill_Goal_message_member_array[5] = {
  {
    "skill_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_Goal, skill_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "user_input",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_Goal, user_input),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "robot_state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_Goal, robot_state),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "user_context",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_Goal, user_context),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "session_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_Goal, session_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__action__ExecuteSkill_Goal__rosidl_typesupport_introspection_c__ExecuteSkill_Goal_message_members = {
  "aimee_msgs__action",  // message namespace
  "ExecuteSkill_Goal",  // message name
  5,  // number of fields
  sizeof(aimee_msgs__action__ExecuteSkill_Goal),
  aimee_msgs__action__ExecuteSkill_Goal__rosidl_typesupport_introspection_c__ExecuteSkill_Goal_message_member_array,  // message members
  aimee_msgs__action__ExecuteSkill_Goal__rosidl_typesupport_introspection_c__ExecuteSkill_Goal_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__action__ExecuteSkill_Goal__rosidl_typesupport_introspection_c__ExecuteSkill_Goal_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__action__ExecuteSkill_Goal__rosidl_typesupport_introspection_c__ExecuteSkill_Goal_message_type_support_handle = {
  0,
  &aimee_msgs__action__ExecuteSkill_Goal__rosidl_typesupport_introspection_c__ExecuteSkill_Goal_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_Goal)() {
  aimee_msgs__action__ExecuteSkill_Goal__rosidl_typesupport_introspection_c__ExecuteSkill_Goal_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, msg, RobotState)();
  if (!aimee_msgs__action__ExecuteSkill_Goal__rosidl_typesupport_introspection_c__ExecuteSkill_Goal_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__ExecuteSkill_Goal__rosidl_typesupport_introspection_c__ExecuteSkill_Goal_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__action__ExecuteSkill_Goal__rosidl_typesupport_introspection_c__ExecuteSkill_Goal_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "aimee_msgs/action/detail/execute_skill__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__functions.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.h"


// Include directives for member types
// Member `response_text`
// Member `tts_audio_path`
// Member `error_message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"
// Member `motor_actions`
#include "aimee_msgs/msg/motor_action.h"
// Member `motor_actions`
#include "aimee_msgs/msg/detail/motor_action__rosidl_typesupport_introspection_c.h"
// Member `camera_actions`
#include "aimee_msgs/msg/camera_action.h"
// Member `camera_actions`
#include "aimee_msgs/msg/detail/camera_action__rosidl_typesupport_introspection_c.h"
// Member `led_actions`
#include "aimee_msgs/msg/led_action.h"
// Member `led_actions`
#include "aimee_msgs/msg/detail/led_action__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__ExecuteSkill_Result_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__action__ExecuteSkill_Result__init(message_memory);
}

void aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__ExecuteSkill_Result_fini_function(void * message_memory)
{
  aimee_msgs__action__ExecuteSkill_Result__fini(message_memory);
}

size_t aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__size_function__ExecuteSkill_Result__motor_actions(
  const void * untyped_member)
{
  const aimee_msgs__msg__MotorAction__Sequence * member =
    (const aimee_msgs__msg__MotorAction__Sequence *)(untyped_member);
  return member->size;
}

const void * aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_const_function__ExecuteSkill_Result__motor_actions(
  const void * untyped_member, size_t index)
{
  const aimee_msgs__msg__MotorAction__Sequence * member =
    (const aimee_msgs__msg__MotorAction__Sequence *)(untyped_member);
  return &member->data[index];
}

void * aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_function__ExecuteSkill_Result__motor_actions(
  void * untyped_member, size_t index)
{
  aimee_msgs__msg__MotorAction__Sequence * member =
    (aimee_msgs__msg__MotorAction__Sequence *)(untyped_member);
  return &member->data[index];
}

void aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__fetch_function__ExecuteSkill_Result__motor_actions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const aimee_msgs__msg__MotorAction * item =
    ((const aimee_msgs__msg__MotorAction *)
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_const_function__ExecuteSkill_Result__motor_actions(untyped_member, index));
  aimee_msgs__msg__MotorAction * value =
    (aimee_msgs__msg__MotorAction *)(untyped_value);
  *value = *item;
}

void aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__assign_function__ExecuteSkill_Result__motor_actions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  aimee_msgs__msg__MotorAction * item =
    ((aimee_msgs__msg__MotorAction *)
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_function__ExecuteSkill_Result__motor_actions(untyped_member, index));
  const aimee_msgs__msg__MotorAction * value =
    (const aimee_msgs__msg__MotorAction *)(untyped_value);
  *item = *value;
}

bool aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__resize_function__ExecuteSkill_Result__motor_actions(
  void * untyped_member, size_t size)
{
  aimee_msgs__msg__MotorAction__Sequence * member =
    (aimee_msgs__msg__MotorAction__Sequence *)(untyped_member);
  aimee_msgs__msg__MotorAction__Sequence__fini(member);
  return aimee_msgs__msg__MotorAction__Sequence__init(member, size);
}

size_t aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__size_function__ExecuteSkill_Result__camera_actions(
  const void * untyped_member)
{
  const aimee_msgs__msg__CameraAction__Sequence * member =
    (const aimee_msgs__msg__CameraAction__Sequence *)(untyped_member);
  return member->size;
}

const void * aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_const_function__ExecuteSkill_Result__camera_actions(
  const void * untyped_member, size_t index)
{
  const aimee_msgs__msg__CameraAction__Sequence * member =
    (const aimee_msgs__msg__CameraAction__Sequence *)(untyped_member);
  return &member->data[index];
}

void * aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_function__ExecuteSkill_Result__camera_actions(
  void * untyped_member, size_t index)
{
  aimee_msgs__msg__CameraAction__Sequence * member =
    (aimee_msgs__msg__CameraAction__Sequence *)(untyped_member);
  return &member->data[index];
}

void aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__fetch_function__ExecuteSkill_Result__camera_actions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const aimee_msgs__msg__CameraAction * item =
    ((const aimee_msgs__msg__CameraAction *)
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_const_function__ExecuteSkill_Result__camera_actions(untyped_member, index));
  aimee_msgs__msg__CameraAction * value =
    (aimee_msgs__msg__CameraAction *)(untyped_value);
  *value = *item;
}

void aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__assign_function__ExecuteSkill_Result__camera_actions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  aimee_msgs__msg__CameraAction * item =
    ((aimee_msgs__msg__CameraAction *)
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_function__ExecuteSkill_Result__camera_actions(untyped_member, index));
  const aimee_msgs__msg__CameraAction * value =
    (const aimee_msgs__msg__CameraAction *)(untyped_value);
  *item = *value;
}

bool aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__resize_function__ExecuteSkill_Result__camera_actions(
  void * untyped_member, size_t size)
{
  aimee_msgs__msg__CameraAction__Sequence * member =
    (aimee_msgs__msg__CameraAction__Sequence *)(untyped_member);
  aimee_msgs__msg__CameraAction__Sequence__fini(member);
  return aimee_msgs__msg__CameraAction__Sequence__init(member, size);
}

size_t aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__size_function__ExecuteSkill_Result__led_actions(
  const void * untyped_member)
{
  const aimee_msgs__msg__LEDAction__Sequence * member =
    (const aimee_msgs__msg__LEDAction__Sequence *)(untyped_member);
  return member->size;
}

const void * aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_const_function__ExecuteSkill_Result__led_actions(
  const void * untyped_member, size_t index)
{
  const aimee_msgs__msg__LEDAction__Sequence * member =
    (const aimee_msgs__msg__LEDAction__Sequence *)(untyped_member);
  return &member->data[index];
}

void * aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_function__ExecuteSkill_Result__led_actions(
  void * untyped_member, size_t index)
{
  aimee_msgs__msg__LEDAction__Sequence * member =
    (aimee_msgs__msg__LEDAction__Sequence *)(untyped_member);
  return &member->data[index];
}

void aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__fetch_function__ExecuteSkill_Result__led_actions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const aimee_msgs__msg__LEDAction * item =
    ((const aimee_msgs__msg__LEDAction *)
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_const_function__ExecuteSkill_Result__led_actions(untyped_member, index));
  aimee_msgs__msg__LEDAction * value =
    (aimee_msgs__msg__LEDAction *)(untyped_value);
  *value = *item;
}

void aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__assign_function__ExecuteSkill_Result__led_actions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  aimee_msgs__msg__LEDAction * item =
    ((aimee_msgs__msg__LEDAction *)
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_function__ExecuteSkill_Result__led_actions(untyped_member, index));
  const aimee_msgs__msg__LEDAction * value =
    (const aimee_msgs__msg__LEDAction *)(untyped_value);
  *item = *value;
}

bool aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__resize_function__ExecuteSkill_Result__led_actions(
  void * untyped_member, size_t size)
{
  aimee_msgs__msg__LEDAction__Sequence * member =
    (aimee_msgs__msg__LEDAction__Sequence *)(untyped_member);
  aimee_msgs__msg__LEDAction__Sequence__fini(member);
  return aimee_msgs__msg__LEDAction__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__ExecuteSkill_Result_message_member_array[7] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_Result, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "response_text",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_Result, response_text),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "tts_audio_path",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_Result, tts_audio_path),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "error_message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_Result, error_message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "motor_actions",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_Result, motor_actions),  // bytes offset in struct
    NULL,  // default value
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__size_function__ExecuteSkill_Result__motor_actions,  // size() function pointer
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_const_function__ExecuteSkill_Result__motor_actions,  // get_const(index) function pointer
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_function__ExecuteSkill_Result__motor_actions,  // get(index) function pointer
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__fetch_function__ExecuteSkill_Result__motor_actions,  // fetch(index, &value) function pointer
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__assign_function__ExecuteSkill_Result__motor_actions,  // assign(index, value) function pointer
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__resize_function__ExecuteSkill_Result__motor_actions  // resize(index) function pointer
  },
  {
    "camera_actions",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_Result, camera_actions),  // bytes offset in struct
    NULL,  // default value
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__size_function__ExecuteSkill_Result__camera_actions,  // size() function pointer
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_const_function__ExecuteSkill_Result__camera_actions,  // get_const(index) function pointer
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_function__ExecuteSkill_Result__camera_actions,  // get(index) function pointer
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__fetch_function__ExecuteSkill_Result__camera_actions,  // fetch(index, &value) function pointer
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__assign_function__ExecuteSkill_Result__camera_actions,  // assign(index, value) function pointer
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__resize_function__ExecuteSkill_Result__camera_actions  // resize(index) function pointer
  },
  {
    "led_actions",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_Result, led_actions),  // bytes offset in struct
    NULL,  // default value
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__size_function__ExecuteSkill_Result__led_actions,  // size() function pointer
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_const_function__ExecuteSkill_Result__led_actions,  // get_const(index) function pointer
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__get_function__ExecuteSkill_Result__led_actions,  // get(index) function pointer
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__fetch_function__ExecuteSkill_Result__led_actions,  // fetch(index, &value) function pointer
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__assign_function__ExecuteSkill_Result__led_actions,  // assign(index, value) function pointer
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__resize_function__ExecuteSkill_Result__led_actions  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__ExecuteSkill_Result_message_members = {
  "aimee_msgs__action",  // message namespace
  "ExecuteSkill_Result",  // message name
  7,  // number of fields
  sizeof(aimee_msgs__action__ExecuteSkill_Result),
  aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__ExecuteSkill_Result_message_member_array,  // message members
  aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__ExecuteSkill_Result_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__ExecuteSkill_Result_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__ExecuteSkill_Result_message_type_support_handle = {
  0,
  &aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__ExecuteSkill_Result_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_Result)() {
  aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__ExecuteSkill_Result_message_member_array[4].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, msg, MotorAction)();
  aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__ExecuteSkill_Result_message_member_array[5].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, msg, CameraAction)();
  aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__ExecuteSkill_Result_message_member_array[6].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, msg, LEDAction)();
  if (!aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__ExecuteSkill_Result_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__ExecuteSkill_Result_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__action__ExecuteSkill_Result__rosidl_typesupport_introspection_c__ExecuteSkill_Result_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "aimee_msgs/action/detail/execute_skill__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__functions.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.h"


// Include directives for member types
// Member `status`
// Member `current_action`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__action__ExecuteSkill_Feedback__rosidl_typesupport_introspection_c__ExecuteSkill_Feedback_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__action__ExecuteSkill_Feedback__init(message_memory);
}

void aimee_msgs__action__ExecuteSkill_Feedback__rosidl_typesupport_introspection_c__ExecuteSkill_Feedback_fini_function(void * message_memory)
{
  aimee_msgs__action__ExecuteSkill_Feedback__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__action__ExecuteSkill_Feedback__rosidl_typesupport_introspection_c__ExecuteSkill_Feedback_message_member_array[4] = {
  {
    "status",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_Feedback, status),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "current_action",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_Feedback, current_action),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "progress",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_Feedback, progress),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "can_cancel",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_Feedback, can_cancel),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__action__ExecuteSkill_Feedback__rosidl_typesupport_introspection_c__ExecuteSkill_Feedback_message_members = {
  "aimee_msgs__action",  // message namespace
  "ExecuteSkill_Feedback",  // message name
  4,  // number of fields
  sizeof(aimee_msgs__action__ExecuteSkill_Feedback),
  aimee_msgs__action__ExecuteSkill_Feedback__rosidl_typesupport_introspection_c__ExecuteSkill_Feedback_message_member_array,  // message members
  aimee_msgs__action__ExecuteSkill_Feedback__rosidl_typesupport_introspection_c__ExecuteSkill_Feedback_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__action__ExecuteSkill_Feedback__rosidl_typesupport_introspection_c__ExecuteSkill_Feedback_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__action__ExecuteSkill_Feedback__rosidl_typesupport_introspection_c__ExecuteSkill_Feedback_message_type_support_handle = {
  0,
  &aimee_msgs__action__ExecuteSkill_Feedback__rosidl_typesupport_introspection_c__ExecuteSkill_Feedback_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_Feedback)() {
  if (!aimee_msgs__action__ExecuteSkill_Feedback__rosidl_typesupport_introspection_c__ExecuteSkill_Feedback_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__ExecuteSkill_Feedback__rosidl_typesupport_introspection_c__ExecuteSkill_Feedback_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__action__ExecuteSkill_Feedback__rosidl_typesupport_introspection_c__ExecuteSkill_Feedback_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "aimee_msgs/action/detail/execute_skill__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__functions.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.h"


// Include directives for member types
// Member `goal_id`
#include "unique_identifier_msgs/msg/uuid.h"
// Member `goal_id`
#include "unique_identifier_msgs/msg/detail/uuid__rosidl_typesupport_introspection_c.h"
// Member `goal`
#include "aimee_msgs/action/execute_skill.h"
// Member `goal`
// already included above
// #include "aimee_msgs/action/detail/execute_skill__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__action__ExecuteSkill_SendGoal_Request__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__action__ExecuteSkill_SendGoal_Request__init(message_memory);
}

void aimee_msgs__action__ExecuteSkill_SendGoal_Request__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Request_fini_function(void * message_memory)
{
  aimee_msgs__action__ExecuteSkill_SendGoal_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__action__ExecuteSkill_SendGoal_Request__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Request_message_member_array[2] = {
  {
    "goal_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_SendGoal_Request, goal_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "goal",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_SendGoal_Request, goal),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__action__ExecuteSkill_SendGoal_Request__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Request_message_members = {
  "aimee_msgs__action",  // message namespace
  "ExecuteSkill_SendGoal_Request",  // message name
  2,  // number of fields
  sizeof(aimee_msgs__action__ExecuteSkill_SendGoal_Request),
  aimee_msgs__action__ExecuteSkill_SendGoal_Request__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Request_message_member_array,  // message members
  aimee_msgs__action__ExecuteSkill_SendGoal_Request__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__action__ExecuteSkill_SendGoal_Request__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__action__ExecuteSkill_SendGoal_Request__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Request_message_type_support_handle = {
  0,
  &aimee_msgs__action__ExecuteSkill_SendGoal_Request__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_SendGoal_Request)() {
  aimee_msgs__action__ExecuteSkill_SendGoal_Request__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unique_identifier_msgs, msg, UUID)();
  aimee_msgs__action__ExecuteSkill_SendGoal_Request__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Request_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_Goal)();
  if (!aimee_msgs__action__ExecuteSkill_SendGoal_Request__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Request_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__ExecuteSkill_SendGoal_Request__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__action__ExecuteSkill_SendGoal_Request__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "aimee_msgs/action/detail/execute_skill__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__functions.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.h"


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/time.h"
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__action__ExecuteSkill_SendGoal_Response__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__action__ExecuteSkill_SendGoal_Response__init(message_memory);
}

void aimee_msgs__action__ExecuteSkill_SendGoal_Response__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Response_fini_function(void * message_memory)
{
  aimee_msgs__action__ExecuteSkill_SendGoal_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__action__ExecuteSkill_SendGoal_Response__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Response_message_member_array[2] = {
  {
    "accepted",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_SendGoal_Response, accepted),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "stamp",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_SendGoal_Response, stamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__action__ExecuteSkill_SendGoal_Response__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Response_message_members = {
  "aimee_msgs__action",  // message namespace
  "ExecuteSkill_SendGoal_Response",  // message name
  2,  // number of fields
  sizeof(aimee_msgs__action__ExecuteSkill_SendGoal_Response),
  aimee_msgs__action__ExecuteSkill_SendGoal_Response__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Response_message_member_array,  // message members
  aimee_msgs__action__ExecuteSkill_SendGoal_Response__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__action__ExecuteSkill_SendGoal_Response__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__action__ExecuteSkill_SendGoal_Response__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Response_message_type_support_handle = {
  0,
  &aimee_msgs__action__ExecuteSkill_SendGoal_Response__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_SendGoal_Response)() {
  aimee_msgs__action__ExecuteSkill_SendGoal_Response__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Response_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Time)();
  if (!aimee_msgs__action__ExecuteSkill_SendGoal_Response__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Response_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__ExecuteSkill_SendGoal_Response__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__action__ExecuteSkill_SendGoal_Response__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_service_members = {
  "aimee_msgs__action",  // service namespace
  "ExecuteSkill_SendGoal",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Request_message_type_support_handle,
  NULL  // response message
  // aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_Response_message_type_support_handle
};

static rosidl_service_type_support_t aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_service_type_support_handle = {
  0,
  &aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_SendGoal_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_SendGoal_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_SendGoal)() {
  if (!aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_service_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_SendGoal_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_SendGoal_Response)()->data;
  }

  return &aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_SendGoal_service_type_support_handle;
}

// already included above
// #include <stddef.h>
// already included above
// #include "aimee_msgs/action/detail/execute_skill__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__functions.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.h"


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/uuid.h"
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__action__ExecuteSkill_GetResult_Request__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__action__ExecuteSkill_GetResult_Request__init(message_memory);
}

void aimee_msgs__action__ExecuteSkill_GetResult_Request__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Request_fini_function(void * message_memory)
{
  aimee_msgs__action__ExecuteSkill_GetResult_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__action__ExecuteSkill_GetResult_Request__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Request_message_member_array[1] = {
  {
    "goal_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_GetResult_Request, goal_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__action__ExecuteSkill_GetResult_Request__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Request_message_members = {
  "aimee_msgs__action",  // message namespace
  "ExecuteSkill_GetResult_Request",  // message name
  1,  // number of fields
  sizeof(aimee_msgs__action__ExecuteSkill_GetResult_Request),
  aimee_msgs__action__ExecuteSkill_GetResult_Request__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Request_message_member_array,  // message members
  aimee_msgs__action__ExecuteSkill_GetResult_Request__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__action__ExecuteSkill_GetResult_Request__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__action__ExecuteSkill_GetResult_Request__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Request_message_type_support_handle = {
  0,
  &aimee_msgs__action__ExecuteSkill_GetResult_Request__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_GetResult_Request)() {
  aimee_msgs__action__ExecuteSkill_GetResult_Request__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unique_identifier_msgs, msg, UUID)();
  if (!aimee_msgs__action__ExecuteSkill_GetResult_Request__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Request_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__ExecuteSkill_GetResult_Request__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__action__ExecuteSkill_GetResult_Request__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "aimee_msgs/action/detail/execute_skill__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__functions.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.h"


// Include directives for member types
// Member `result`
// already included above
// #include "aimee_msgs/action/execute_skill.h"
// Member `result`
// already included above
// #include "aimee_msgs/action/detail/execute_skill__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__action__ExecuteSkill_GetResult_Response__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__action__ExecuteSkill_GetResult_Response__init(message_memory);
}

void aimee_msgs__action__ExecuteSkill_GetResult_Response__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Response_fini_function(void * message_memory)
{
  aimee_msgs__action__ExecuteSkill_GetResult_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__action__ExecuteSkill_GetResult_Response__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Response_message_member_array[2] = {
  {
    "status",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_GetResult_Response, status),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "result",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_GetResult_Response, result),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__action__ExecuteSkill_GetResult_Response__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Response_message_members = {
  "aimee_msgs__action",  // message namespace
  "ExecuteSkill_GetResult_Response",  // message name
  2,  // number of fields
  sizeof(aimee_msgs__action__ExecuteSkill_GetResult_Response),
  aimee_msgs__action__ExecuteSkill_GetResult_Response__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Response_message_member_array,  // message members
  aimee_msgs__action__ExecuteSkill_GetResult_Response__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__action__ExecuteSkill_GetResult_Response__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__action__ExecuteSkill_GetResult_Response__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Response_message_type_support_handle = {
  0,
  &aimee_msgs__action__ExecuteSkill_GetResult_Response__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_GetResult_Response)() {
  aimee_msgs__action__ExecuteSkill_GetResult_Response__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Response_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_Result)();
  if (!aimee_msgs__action__ExecuteSkill_GetResult_Response__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Response_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__ExecuteSkill_GetResult_Response__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__action__ExecuteSkill_GetResult_Response__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_service_members = {
  "aimee_msgs__action",  // service namespace
  "ExecuteSkill_GetResult",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Request_message_type_support_handle,
  NULL  // response message
  // aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_Response_message_type_support_handle
};

static rosidl_service_type_support_t aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_service_type_support_handle = {
  0,
  &aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_GetResult_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_GetResult_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_GetResult)() {
  if (!aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_service_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_GetResult_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_GetResult_Response)()->data;
  }

  return &aimee_msgs__action__detail__execute_skill__rosidl_typesupport_introspection_c__ExecuteSkill_GetResult_service_type_support_handle;
}

// already included above
// #include <stddef.h>
// already included above
// #include "aimee_msgs/action/detail/execute_skill__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__functions.h"
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.h"


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/uuid.h"
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__rosidl_typesupport_introspection_c.h"
// Member `feedback`
// already included above
// #include "aimee_msgs/action/execute_skill.h"
// Member `feedback`
// already included above
// #include "aimee_msgs/action/detail/execute_skill__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__action__ExecuteSkill_FeedbackMessage__rosidl_typesupport_introspection_c__ExecuteSkill_FeedbackMessage_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__action__ExecuteSkill_FeedbackMessage__init(message_memory);
}

void aimee_msgs__action__ExecuteSkill_FeedbackMessage__rosidl_typesupport_introspection_c__ExecuteSkill_FeedbackMessage_fini_function(void * message_memory)
{
  aimee_msgs__action__ExecuteSkill_FeedbackMessage__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__action__ExecuteSkill_FeedbackMessage__rosidl_typesupport_introspection_c__ExecuteSkill_FeedbackMessage_message_member_array[2] = {
  {
    "goal_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_FeedbackMessage, goal_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "feedback",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__ExecuteSkill_FeedbackMessage, feedback),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__action__ExecuteSkill_FeedbackMessage__rosidl_typesupport_introspection_c__ExecuteSkill_FeedbackMessage_message_members = {
  "aimee_msgs__action",  // message namespace
  "ExecuteSkill_FeedbackMessage",  // message name
  2,  // number of fields
  sizeof(aimee_msgs__action__ExecuteSkill_FeedbackMessage),
  aimee_msgs__action__ExecuteSkill_FeedbackMessage__rosidl_typesupport_introspection_c__ExecuteSkill_FeedbackMessage_message_member_array,  // message members
  aimee_msgs__action__ExecuteSkill_FeedbackMessage__rosidl_typesupport_introspection_c__ExecuteSkill_FeedbackMessage_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__action__ExecuteSkill_FeedbackMessage__rosidl_typesupport_introspection_c__ExecuteSkill_FeedbackMessage_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__action__ExecuteSkill_FeedbackMessage__rosidl_typesupport_introspection_c__ExecuteSkill_FeedbackMessage_message_type_support_handle = {
  0,
  &aimee_msgs__action__ExecuteSkill_FeedbackMessage__rosidl_typesupport_introspection_c__ExecuteSkill_FeedbackMessage_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_FeedbackMessage)() {
  aimee_msgs__action__ExecuteSkill_FeedbackMessage__rosidl_typesupport_introspection_c__ExecuteSkill_FeedbackMessage_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unique_identifier_msgs, msg, UUID)();
  aimee_msgs__action__ExecuteSkill_FeedbackMessage__rosidl_typesupport_introspection_c__ExecuteSkill_FeedbackMessage_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, ExecuteSkill_Feedback)();
  if (!aimee_msgs__action__ExecuteSkill_FeedbackMessage__rosidl_typesupport_introspection_c__ExecuteSkill_FeedbackMessage_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__ExecuteSkill_FeedbackMessage__rosidl_typesupport_introspection_c__ExecuteSkill_FeedbackMessage_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__action__ExecuteSkill_FeedbackMessage__rosidl_typesupport_introspection_c__ExecuteSkill_FeedbackMessage_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
