// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aimee_msgs:msg/CameraAction.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__CAMERA_ACTION__STRUCT_H_
#define AIMEE_MSGS__MSG__DETAIL__CAMERA_ACTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'action_type'
// Member 'target'
#include "rosidl_runtime_c/string.h"
// Member 'execution_time'
#include "builtin_interfaces/msg/detail/duration__struct.h"

/// Struct defined in msg/CameraAction in the package aimee_msgs.
/**
  * Camera action performed by a skill
  * Published in ExecuteSkill result
 */
typedef struct aimee_msgs__msg__CameraAction
{
  /// track_face, stop_tracking, look_at_me, etc.
  rosidl_runtime_c__String action_type;
  /// Target object/person
  rosidl_runtime_c__String target;
  /// Detection confidence
  float confidence;
  builtin_interfaces__msg__Duration execution_time;
} aimee_msgs__msg__CameraAction;

// Struct for a sequence of aimee_msgs__msg__CameraAction.
typedef struct aimee_msgs__msg__CameraAction__Sequence
{
  aimee_msgs__msg__CameraAction * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__msg__CameraAction__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIMEE_MSGS__MSG__DETAIL__CAMERA_ACTION__STRUCT_H_
