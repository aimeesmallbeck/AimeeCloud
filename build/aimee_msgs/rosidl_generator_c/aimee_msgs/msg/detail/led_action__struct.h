// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aimee_msgs:msg/LEDAction.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__LED_ACTION__STRUCT_H_
#define AIMEE_MSGS__MSG__DETAIL__LED_ACTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'led_id'
// Member 'pattern'
#include "rosidl_runtime_c/string.h"
// Member 'color'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/LEDAction in the package aimee_msgs.
/**
  * LED action performed by a skill
  * Published in ExecuteSkill result
 */
typedef struct aimee_msgs__msg__LEDAction
{
  /// Which LED (matrix, status, etc.)
  rosidl_runtime_c__String led_id;
  /// RGB color values
  rosidl_runtime_c__uint8__Sequence color;
  /// solid, blink, pulse, rainbow
  rosidl_runtime_c__String pattern;
  /// How long to display
  float duration_sec;
} aimee_msgs__msg__LEDAction;

// Struct for a sequence of aimee_msgs__msg__LEDAction.
typedef struct aimee_msgs__msg__LEDAction__Sequence
{
  aimee_msgs__msg__LEDAction * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__msg__LEDAction__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIMEE_MSGS__MSG__DETAIL__LED_ACTION__STRUCT_H_
