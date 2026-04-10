// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from aimee_msgs:msg/FaceDetection.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "aimee_msgs/msg/detail/face_detection__rosidl_typesupport_introspection_c.h"
#include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "aimee_msgs/msg/detail/face_detection__functions.h"
#include "aimee_msgs/msg/detail/face_detection__struct.h"


// Include directives for member types
// Member `face_id`
// Member `person_name`
// Member `camera_source`
#include "rosidl_runtime_c/string_functions.h"
// Member `face_landmarks`
#include "rosidl_runtime_c/primitives_sequence_functions.h"
// Member `position_3d`
#include "geometry_msgs/msg/point.h"
// Member `position_3d`
#include "geometry_msgs/msg/detail/point__rosidl_typesupport_introspection_c.h"
// Member `timestamp`
#include "builtin_interfaces/msg/time.h"
// Member `timestamp`
#include "builtin_interfaces/msg/detail/time__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__FaceDetection_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__msg__FaceDetection__init(message_memory);
}

void aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__FaceDetection_fini_function(void * message_memory)
{
  aimee_msgs__msg__FaceDetection__fini(message_memory);
}

size_t aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__size_function__FaceDetection__face_landmarks(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__get_const_function__FaceDetection__face_landmarks(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__get_function__FaceDetection__face_landmarks(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__fetch_function__FaceDetection__face_landmarks(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__get_const_function__FaceDetection__face_landmarks(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__assign_function__FaceDetection__face_landmarks(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__get_function__FaceDetection__face_landmarks(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__resize_function__FaceDetection__face_landmarks(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__FaceDetection_message_member_array[12] = {
  {
    "face_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__FaceDetection, face_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "person_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__FaceDetection, person_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "recognition_confidence",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__FaceDetection, recognition_confidence),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "center_x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__FaceDetection, center_x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "center_y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__FaceDetection, center_y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "width",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__FaceDetection, width),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "height",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__FaceDetection, height),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "num_faces_detected",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__FaceDetection, num_faces_detected),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "face_landmarks",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__FaceDetection, face_landmarks),  // bytes offset in struct
    NULL,  // default value
    aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__size_function__FaceDetection__face_landmarks,  // size() function pointer
    aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__get_const_function__FaceDetection__face_landmarks,  // get_const(index) function pointer
    aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__get_function__FaceDetection__face_landmarks,  // get(index) function pointer
    aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__fetch_function__FaceDetection__face_landmarks,  // fetch(index, &value) function pointer
    aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__assign_function__FaceDetection__face_landmarks,  // assign(index, value) function pointer
    aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__resize_function__FaceDetection__face_landmarks  // resize(index) function pointer
  },
  {
    "position_3d",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__FaceDetection, position_3d),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "timestamp",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__FaceDetection, timestamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "camera_source",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__msg__FaceDetection, camera_source),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__FaceDetection_message_members = {
  "aimee_msgs__msg",  // message namespace
  "FaceDetection",  // message name
  12,  // number of fields
  sizeof(aimee_msgs__msg__FaceDetection),
  aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__FaceDetection_message_member_array,  // message members
  aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__FaceDetection_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__FaceDetection_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__FaceDetection_message_type_support_handle = {
  0,
  &aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__FaceDetection_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, msg, FaceDetection)() {
  aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__FaceDetection_message_member_array[9].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Point)();
  aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__FaceDetection_message_member_array[10].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Time)();
  if (!aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__FaceDetection_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__FaceDetection_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__msg__FaceDetection__rosidl_typesupport_introspection_c__FaceDetection_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
