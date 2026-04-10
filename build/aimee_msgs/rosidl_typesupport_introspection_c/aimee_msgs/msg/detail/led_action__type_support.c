// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from aimee_msgs:msg/LEDAction.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "aimee_msgs/msg/detail/led_action__rosidl_typesupport_introspection_c.h"
#include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "aimee_msgs/msg/detail/led_action__functions.h"
#include "aimee_msgs/msg/detail/led_action__struct.h"


// Include directives for member types
// Member `led_id`
// Member `pattern`
#include "rosidl_runtime_c/string_functions.h"
// Member `color`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__LEDAction_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__msg__LEDAction__init(message_memory);
}

void aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__LEDAction_fini_function(void * message_memory)
{
  aimee_msgs__msg__LEDAction__fini(message_memory);
}

size_t aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__size_function__LEDAction__color(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return member->size;
}

const void * aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__get_const_function__LEDAction__color(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void * aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__get_function__LEDAction__color(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__fetch_function__LEDAction__color(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__get_const_function__LEDAction__color(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__assign_function__LEDAction__color(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__get_function__LEDAction__color(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

bool aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__resize_function__LEDAction__color(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  rosidl_runtime_c__uint8__Sequence__fini(member);
  return rosidl_runtime_c__uint8__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__LEDAction_message_member_array[4] = {
  {
    "led_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__LEDAction, led_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "color",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__LEDAction, color),  // bytes offset in struct
    NULL,  // default value
    aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__size_function__LEDAction__color,  // size() function pointer
    aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__get_const_function__LEDAction__color,  // get_const(index) function pointer
    aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__get_function__LEDAction__color,  // get(index) function pointer
    aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__fetch_function__LEDAction__color,  // fetch(index, &value) function pointer
    aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__assign_function__LEDAction__color,  // assign(index, value) function pointer
    aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__resize_function__LEDAction__color  // resize(index) function pointer
  },
  {
    "pattern",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__LEDAction, pattern),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "duration_sec",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__LEDAction, duration_sec),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__LEDAction_message_members = {
  "aimee_msgs__msg",  // message namespace
  "LEDAction",  // message name
  4,  // number of fields
  sizeof(aimee_msgs__msg__LEDAction),
  aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__LEDAction_message_member_array,  // message members
  aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__LEDAction_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__LEDAction_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__LEDAction_message_type_support_handle = {
  0,
  &aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__LEDAction_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, msg, LEDAction)() {
  if (!aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__LEDAction_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__LEDAction_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__msg__LEDAction__rosidl_typesupport_introspection_c__LEDAction_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
