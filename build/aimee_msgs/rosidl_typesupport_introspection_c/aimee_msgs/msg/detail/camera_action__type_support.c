// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from aimee_msgs:msg/CameraAction.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "aimee_msgs/msg/detail/camera_action__rosidl_typesupport_introspection_c.h"
#include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "aimee_msgs/msg/detail/camera_action__functions.h"
#include "aimee_msgs/msg/detail/camera_action__struct.h"


// Include directives for member types
// Member `action_type`
// Member `target`
#include "rosidl_runtime_c/string_functions.h"
// Member `execution_time`
#include "builtin_interfaces/msg/duration.h"
// Member `execution_time`
#include "builtin_interfaces/msg/detail/duration__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__msg__CameraAction__rosidl_typesupport_introspection_c__CameraAction_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__msg__CameraAction__init(message_memory);
}

void aimee_msgs__msg__CameraAction__rosidl_typesupport_introspection_c__CameraAction_fini_function(void * message_memory)
{
  aimee_msgs__msg__CameraAction__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__msg__CameraAction__rosidl_typesupport_introspection_c__CameraAction_message_member_array[4] = {
  {
    "action_type",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__CameraAction, action_type),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "target",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__CameraAction, target),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "confidence",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__CameraAction, confidence),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "execution_time",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__CameraAction, execution_time),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__msg__CameraAction__rosidl_typesupport_introspection_c__CameraAction_message_members = {
  "aimee_msgs__msg",  // message namespace
  "CameraAction",  // message name
  4,  // number of fields
  sizeof(aimee_msgs__msg__CameraAction),
  aimee_msgs__msg__CameraAction__rosidl_typesupport_introspection_c__CameraAction_message_member_array,  // message members
  aimee_msgs__msg__CameraAction__rosidl_typesupport_introspection_c__CameraAction_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__msg__CameraAction__rosidl_typesupport_introspection_c__CameraAction_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__msg__CameraAction__rosidl_typesupport_introspection_c__CameraAction_message_type_support_handle = {
  0,
  &aimee_msgs__msg__CameraAction__rosidl_typesupport_introspection_c__CameraAction_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, msg, CameraAction)() {
  aimee_msgs__msg__CameraAction__rosidl_typesupport_introspection_c__CameraAction_message_member_array[3].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Duration)();
  if (!aimee_msgs__msg__CameraAction__rosidl_typesupport_introspection_c__CameraAction_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__msg__CameraAction__rosidl_typesupport_introspection_c__CameraAction_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__msg__CameraAction__rosidl_typesupport_introspection_c__CameraAction_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
