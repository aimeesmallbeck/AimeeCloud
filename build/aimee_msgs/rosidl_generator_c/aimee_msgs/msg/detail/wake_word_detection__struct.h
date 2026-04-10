// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aimee_msgs:msg/WakeWordDetection.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__WAKE_WORD_DETECTION__STRUCT_H_
#define AIMEE_MSGS__MSG__DETAIL__WAKE_WORD_DETECTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'wake_word'
// Member 'source'
// Member 'session_id'
#include "rosidl_runtime_c/string.h"
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in msg/WakeWordDetection in the package aimee_msgs.
/**
  * Wake word detection message
  * Published by: Wake Word Detection Brick (keyword spotting)
  * Subscribed by: Voice Manager, State Manager
 */
typedef struct aimee_msgs__msg__WakeWordDetection
{
  /// Detected wake word (e.g., "aimee", "hey_aimee")
  rosidl_runtime_c__String wake_word;
  /// Detection confidence (0.0-1.0)
  float confidence;
  /// Detection source (e.g., "edge_impulse", "porcupine")
  rosidl_runtime_c__String source;
  /// Detection context
  /// Audio sample index at detection
  uint16_t sample_index;
  /// Audio signal energy level
  float signal_energy;
  /// System state
  /// true when wake word is active/triggered
  /// false when wake word session ends
  bool active;
  /// Metadata
  builtin_interfaces__msg__Time timestamp;
  /// Unique session identifier
  rosidl_runtime_c__String session_id;
} aimee_msgs__msg__WakeWordDetection;

// Struct for a sequence of aimee_msgs__msg__WakeWordDetection.
typedef struct aimee_msgs__msg__WakeWordDetection__Sequence
{
  aimee_msgs__msg__WakeWordDetection * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__msg__WakeWordDetection__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIMEE_MSGS__MSG__DETAIL__WAKE_WORD_DETECTION__STRUCT_H_
