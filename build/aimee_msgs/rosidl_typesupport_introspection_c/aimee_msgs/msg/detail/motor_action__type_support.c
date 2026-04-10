// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from aimee_msgs:msg/MotorAction.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "aimee_msgs/msg/detail/motor_action__rosidl_typesupport_introspection_c.h"
#include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "aimee_msgs/msg/detail/motor_action__functions.h"
#include "aimee_msgs/msg/detail/motor_action__struct.h"


// Include directives for member types
// Member `motor_id`
// Member `action_type`
#include "rosidl_runtime_c/string_functions.h"
// Member `values`
#include "rosidl_runtime_c/primitives_sequence_functions.h"
// Member `execution_time`
#include "builtin_interfaces/msg/duration.h"
// Member `execution_time`
#include "builtin_interfaces/msg/detail/duration__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__MotorAction_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__msg__MotorAction__init(message_memory);
}

void aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__MotorAction_fini_function(void * message_memory)
{
  aimee_msgs__msg__MotorAction__fini(message_memory);
}

size_t aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__size_function__MotorAction__values(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__get_const_function__MotorAction__values(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__get_function__MotorAction__values(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__fetch_function__MotorAction__values(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__get_const_function__MotorAction__values(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__assign_function__MotorAction__values(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__get_function__MotorAction__values(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__resize_function__MotorAction__values(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__MotorAction_message_member_array[4] = {
  {
    "motor_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__MotorAction, motor_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "action_type",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__MotorAction, action_type),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "values",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__MotorAction, values),  // bytes offset in struct
    NULL,  // default value
    aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__size_function__MotorAction__values,  // size() function pointer
    aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__get_const_function__MotorAction__values,  // get_const(index) function pointer
    aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__get_function__MotorAction__values,  // get(index) function pointer
    aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__fetch_function__MotorAction__values,  // fetch(index, &value) function pointer
    aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__assign_function__MotorAction__values,  // assign(index, value) function pointer
    aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__resize_function__MotorAction__values  // resize(index) function pointer
  },
  {
    "execution_time",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__MotorAction, execution_time),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__MotorAction_message_members = {
  "aimee_msgs__msg",  // message namespace
  "MotorAction",  // message name
  4,  // number of fields
  sizeof(aimee_msgs__msg__MotorAction),
  aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__MotorAction_message_member_array,  // message members
  aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__MotorAction_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__MotorAction_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__MotorAction_message_type_support_handle = {
  0,
  &aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__MotorAction_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, msg, MotorAction)() {
  aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__MotorAction_message_member_array[3].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Duration)();
  if (!aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__MotorAction_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__MotorAction_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__msg__MotorAction__rosidl_typesupport_introspection_c__MotorAction_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
