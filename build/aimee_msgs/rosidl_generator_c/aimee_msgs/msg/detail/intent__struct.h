// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aimee_msgs:msg/Intent.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__INTENT__STRUCT_H_
#define AIMEE_MSGS__MSG__DETAIL__INTENT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'intent_type'
// Member 'action'
// Member 'raw_text'
// Member 'skill_name'
// Member 'parameters_json'
// Member 'session_id'
#include "rosidl_runtime_c/string.h"
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in msg/Intent in the package aimee_msgs.
/**
  * Intent classification message
  * Published by: Intent Router
  * Subscribed by: Skills, State Manager
 */
typedef struct aimee_msgs__msg__Intent
{
  /// Type of intent (greeting, movement, arm_control, etc.)
  rosidl_runtime_c__String intent_type;
  /// Specific action (move_forward, wave, etc.)
  rosidl_runtime_c__String action;
  /// Classification confidence (0.0-1.0)
  float confidence;
  /// Original user text
  rosidl_runtime_c__String raw_text;
  /// True if requires skill execution
  bool requires_skill;
  /// Name of skill to execute
  rosidl_runtime_c__String skill_name;
  /// Action parameters as JSON string
  rosidl_runtime_c__String parameters_json;
  /// Context
  /// Conversation session ID
  rosidl_runtime_c__String session_id;
  builtin_interfaces__msg__Time timestamp;
} aimee_msgs__msg__Intent;

// Struct for a sequence of aimee_msgs__msg__Intent.
typedef struct aimee_msgs__msg__Intent__Sequence
{
  aimee_msgs__msg__Intent * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__msg__Intent__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIMEE_MSGS__MSG__DETAIL__INTENT__STRUCT_H_
