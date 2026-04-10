// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aimee_msgs:msg/FaceDetection.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__FACE_DETECTION__STRUCT_H_
#define AIMEE_MSGS__MSG__DETAIL__FACE_DETECTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'face_id'
// Member 'person_name'
// Member 'camera_source'
#include "rosidl_runtime_c/string.h"
// Member 'face_landmarks'
#include "rosidl_runtime_c/primitives_sequence.h"
// Member 'position_3d'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in msg/FaceDetection in the package aimee_msgs.
/**
  * Face detection message
  * Published by: Vision Manager
  * Subscribed by: Skills, OBSBOT Controller
 */
typedef struct aimee_msgs__msg__FaceDetection
{
  /// Face identification
  /// Unique face identifier (or "unknown")
  rosidl_runtime_c__String face_id;
  /// Name if recognized, "unknown" otherwise
  rosidl_runtime_c__String person_name;
  float recognition_confidence;
  /// Face location (normalized coordinates 0.0-1.0)
  float center_x;
  float center_y;
  float width;
  float height;
  /// Additional face data
  /// Total faces in frame
  int32_t num_faces_detected;
  /// Optional: facial landmarks
  rosidl_runtime_c__float__Sequence face_landmarks;
  /// 3D position estimate (if available)
  geometry_msgs__msg__Point position_3d;
  /// Metadata
  builtin_interfaces__msg__Time timestamp;
  /// "obsbot_main" | "ov7670"
  rosidl_runtime_c__String camera_source;
} aimee_msgs__msg__FaceDetection;

// Struct for a sequence of aimee_msgs__msg__FaceDetection.
typedef struct aimee_msgs__msg__FaceDetection__Sequence
{
  aimee_msgs__msg__FaceDetection * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__msg__FaceDetection__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIMEE_MSGS__MSG__DETAIL__FACE_DETECTION__STRUCT_H_
