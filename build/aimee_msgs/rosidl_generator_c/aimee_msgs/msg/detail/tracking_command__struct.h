// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aimee_msgs:msg/TrackingCommand.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__TRACKING_COMMAND__STRUCT_H_
#define AIMEE_MSGS__MSG__DETAIL__TRACKING_COMMAND__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'command'
// Member 'mode'
// Member 'target_type'
// Member 'target_id'
#include "rosidl_runtime_c/string.h"
// Member 'target_position'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in msg/TrackingCommand in the package aimee_msgs.
/**
  * Camera tracking command message
  * Published by: Skills, Face Recognition
  * Subscribed by: Vision Manager
 */
typedef struct aimee_msgs__msg__TrackingCommand
{
  /// "start" | "stop" | "preset" | "zoom" | "mode"
  rosidl_runtime_c__String command;
  /// "normal" | "upper_body" | "closeup" | "headless" | "desk" | "whiteboard" | "hand" | "group" | "off"
  rosidl_runtime_c__String mode;
  /// For "preset" command (1-3)
  int32_t preset_id;
  /// For "zoom" command (0-100)
  int32_t zoom_level;
  /// Target to track (for advanced tracking)
  /// "face" | "body" | "hand" | "object"
  rosidl_runtime_c__String target_type;
  /// Specific target identifier
  rosidl_runtime_c__String target_id;
  /// Last known position
  geometry_msgs__msg__Point target_position;
  /// Metadata
  builtin_interfaces__msg__Time timestamp;
} aimee_msgs__msg__TrackingCommand;

// Struct for a sequence of aimee_msgs__msg__TrackingCommand.
typedef struct aimee_msgs__msg__TrackingCommand__Sequence
{
  aimee_msgs__msg__TrackingCommand * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__msg__TrackingCommand__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIMEE_MSGS__MSG__DETAIL__TRACKING_COMMAND__STRUCT_H_
