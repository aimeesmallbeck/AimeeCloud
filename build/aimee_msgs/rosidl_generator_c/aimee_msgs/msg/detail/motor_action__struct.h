// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aimee_msgs:msg/MotorAction.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__MOTOR_ACTION__STRUCT_H_
#define AIMEE_MSGS__MSG__DETAIL__MOTOR_ACTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'motor_id'
// Member 'action_type'
#include "rosidl_runtime_c/string.h"
// Member 'values'
#include "rosidl_runtime_c/primitives_sequence.h"
// Member 'execution_time'
#include "builtin_interfaces/msg/detail/duration__struct.h"

/// Struct defined in msg/MotorAction in the package aimee_msgs.
/**
  * Motor action performed by a skill
  * Published in ExecuteSkill result
 */
typedef struct aimee_msgs__msg__MotorAction
{
  /// Motor identifier (left_track, right_track, arm_base, etc.)
  rosidl_runtime_c__String motor_id;
  /// move, stop, rotate, position
  rosidl_runtime_c__String action_type;
  /// Action values (speed, position, angle)
  rosidl_runtime_c__float__Sequence values;
  /// How long the action took
  builtin_interfaces__msg__Duration execution_time;
} aimee_msgs__msg__MotorAction;

// Struct for a sequence of aimee_msgs__msg__MotorAction.
typedef struct aimee_msgs__msg__MotorAction__Sequence
{
  aimee_msgs__msg__MotorAction * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__msg__MotorAction__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIMEE_MSGS__MSG__DETAIL__MOTOR_ACTION__STRUCT_H_
