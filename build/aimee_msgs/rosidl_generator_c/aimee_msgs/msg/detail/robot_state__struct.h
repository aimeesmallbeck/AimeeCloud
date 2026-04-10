// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aimee_msgs:msg/RobotState.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__ROBOT_STATE__STRUCT_H_
#define AIMEE_MSGS__MSG__DETAIL__ROBOT_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'robot_name'
// Member 'robot_type'
// Member 'power_status'
// Member 'current_action'
// Member 'arm_pose_name'
// Member 'camera_mode'
// Member 'tracking_target'
// Member 'active_skills'
// Member 'current_skill_id'
// Member 'errors'
// Member 'warnings'
#include "rosidl_runtime_c/string.h"
// Member 'current_velocity'
#include "geometry_msgs/msg/detail/twist__struct.h"
// Member 'odometry'
#include "nav_msgs/msg/detail/odometry__struct.h"
// Member 'arm_state'
#include "sensor_msgs/msg/detail/joint_state__struct.h"
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in msg/RobotState in the package aimee_msgs.
/**
  * Complete robot state message
  * Published by: State Manager (aggregates from all nodes)
  * Subscribed by: Skills, Cloud Bridge
 */
typedef struct aimee_msgs__msg__RobotState
{
  /// Identity
  /// "ron" or "wren"
  rosidl_runtime_c__String robot_name;
  /// "ugv_arm" | "wave_rover"
  rosidl_runtime_c__String robot_type;
  /// Power
  /// 0.0 to 100.0
  float battery_level;
  bool is_charging;
  /// "normal" | "low" | "critical"
  rosidl_runtime_c__String power_status;
  /// Motion state
  /// "idle" | "moving" | "executing_skill"
  rosidl_runtime_c__String current_action;
  geometry_msgs__msg__Twist current_velocity;
  nav_msgs__msg__Odometry odometry;
  /// Arm state (if applicable)
  sensor_msgs__msg__JointState arm_state;
  bool arm_is_moving;
  /// "home" | "ready" | "custom"
  rosidl_runtime_c__String arm_pose_name;
  /// Gripper state
  /// 0.0 (closed) to 1.0 (open)
  float gripper_position;
  /// Camera state
  /// "idle" | "tracking" | "manual"
  rosidl_runtime_c__String camera_mode;
  /// "none" | "face" | "body" | "hand"
  rosidl_runtime_c__String tracking_target;
  /// Active skills
  rosidl_runtime_c__String__Sequence active_skills;
  rosidl_runtime_c__String current_skill_id;
  /// System health
  /// List of active errors
  rosidl_runtime_c__String__Sequence errors;
  /// List of active warnings
  rosidl_runtime_c__String__Sequence warnings;
  /// Metadata
  builtin_interfaces__msg__Time timestamp;
} aimee_msgs__msg__RobotState;

// Struct for a sequence of aimee_msgs__msg__RobotState.
typedef struct aimee_msgs__msg__RobotState__Sequence
{
  aimee_msgs__msg__RobotState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__msg__RobotState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIMEE_MSGS__MSG__DETAIL__ROBOT_STATE__STRUCT_H_
