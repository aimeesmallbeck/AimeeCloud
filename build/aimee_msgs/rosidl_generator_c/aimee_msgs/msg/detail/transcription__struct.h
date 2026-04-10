// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aimee_msgs:msg/Transcription.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__TRANSCRIPTION__STRUCT_H_
#define AIMEE_MSGS__MSG__DETAIL__TRANSCRIPTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'text'
// Member 'source'
// Member 'wake_word'
// Member 'session_id'
// Member 'correlation_id'
#include "rosidl_runtime_c/string.h"
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in msg/Transcription in the package aimee_msgs.
/**
  * Voice transcription message
  * Published by: Voice Manager (ASR)
  * Subscribed by: Intent Router
 */
typedef struct aimee_msgs__msg__Transcription
{
  /// Transcribed text
  rosidl_runtime_c__String text;
  /// ASR confidence (0.0-1.0)
  float confidence;
  /// vosk | whisper | cloud
  rosidl_runtime_c__String source;
  /// True if this is a command (post-wake-word)
  bool is_command;
  /// True if this is a partial result (streaming)
  bool is_partial;
  /// Wake word info
  /// True if preceded by wake word
  bool wake_word_detected;
  /// Which wake word was detected
  rosidl_runtime_c__String wake_word;
  /// Metadata
  builtin_interfaces__msg__Time timestamp;
  rosidl_runtime_c__String session_id;
  rosidl_runtime_c__String correlation_id;
} aimee_msgs__msg__Transcription;

// Struct for a sequence of aimee_msgs__msg__Transcription.
typedef struct aimee_msgs__msg__Transcription__Sequence
{
  aimee_msgs__msg__Transcription * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__msg__Transcription__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIMEE_MSGS__MSG__DETAIL__TRANSCRIPTION__STRUCT_H_
