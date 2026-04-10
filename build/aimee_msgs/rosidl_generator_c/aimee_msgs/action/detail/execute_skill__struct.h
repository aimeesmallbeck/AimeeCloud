// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aimee_msgs:action/ExecuteSkill.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__ACTION__DETAIL__EXECUTE_SKILL__STRUCT_H_
#define AIMEE_MSGS__ACTION__DETAIL__EXECUTE_SKILL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'skill_id'
// Member 'user_input'
// Member 'user_context'
// Member 'session_id'
#include "rosidl_runtime_c/string.h"
// Member 'robot_state'
#include "aimee_msgs/msg/detail/robot_state__struct.h"

/// Struct defined in action/ExecuteSkill in the package aimee_msgs.
typedef struct aimee_msgs__action__ExecuteSkill_Goal
{
  /// Goal: Request to execute a skill
  /// Skill identifier
  rosidl_runtime_c__String skill_id;
  /// User's command/text
  rosidl_runtime_c__String user_input;
  /// Current robot state
  aimee_msgs__msg__RobotState robot_state;
  /// JSON string with user context
  rosidl_runtime_c__String user_context;
  /// Session identifier
  rosidl_runtime_c__String session_id;
} aimee_msgs__action__ExecuteSkill_Goal;

// Struct for a sequence of aimee_msgs__action__ExecuteSkill_Goal.
typedef struct aimee_msgs__action__ExecuteSkill_Goal__Sequence
{
  aimee_msgs__action__ExecuteSkill_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__action__ExecuteSkill_Goal__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'response_text'
// Member 'tts_audio_path'
// Member 'error_message'
// already included above
// #include "rosidl_runtime_c/string.h"
// Member 'motor_actions'
#include "aimee_msgs/msg/detail/motor_action__struct.h"
// Member 'camera_actions'
#include "aimee_msgs/msg/detail/camera_action__struct.h"
// Member 'led_actions'
#include "aimee_msgs/msg/detail/led_action__struct.h"

/// Struct defined in action/ExecuteSkill in the package aimee_msgs.
typedef struct aimee_msgs__action__ExecuteSkill_Result
{
  bool success;
  /// Text response from skill
  rosidl_runtime_c__String response_text;
  /// Path to TTS audio file (if generated)
  rosidl_runtime_c__String tts_audio_path;
  rosidl_runtime_c__String error_message;
  /// Actions performed
  aimee_msgs__msg__MotorAction__Sequence motor_actions;
  aimee_msgs__msg__CameraAction__Sequence camera_actions;
  aimee_msgs__msg__LEDAction__Sequence led_actions;
} aimee_msgs__action__ExecuteSkill_Result;

// Struct for a sequence of aimee_msgs__action__ExecuteSkill_Result.
typedef struct aimee_msgs__action__ExecuteSkill_Result__Sequence
{
  aimee_msgs__action__ExecuteSkill_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__action__ExecuteSkill_Result__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'status'
// Member 'current_action'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/ExecuteSkill in the package aimee_msgs.
typedef struct aimee_msgs__action__ExecuteSkill_Feedback
{
  /// "starting" | "executing" | "finalizing"
  rosidl_runtime_c__String status;
  /// Description of current action
  rosidl_runtime_c__String current_action;
  /// 0.0 to 1.0
  float progress;
  /// Whether skill can be cancelled now
  bool can_cancel;
} aimee_msgs__action__ExecuteSkill_Feedback;

// Struct for a sequence of aimee_msgs__action__ExecuteSkill_Feedback.
typedef struct aimee_msgs__action__ExecuteSkill_Feedback__Sequence
{
  aimee_msgs__action__ExecuteSkill_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__action__ExecuteSkill_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "aimee_msgs/action/detail/execute_skill__struct.h"

/// Struct defined in action/ExecuteSkill in the package aimee_msgs.
typedef struct aimee_msgs__action__ExecuteSkill_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  aimee_msgs__action__ExecuteSkill_Goal goal;
} aimee_msgs__action__ExecuteSkill_SendGoal_Request;

// Struct for a sequence of aimee_msgs__action__ExecuteSkill_SendGoal_Request.
typedef struct aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence
{
  aimee_msgs__action__ExecuteSkill_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/ExecuteSkill in the package aimee_msgs.
typedef struct aimee_msgs__action__ExecuteSkill_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} aimee_msgs__action__ExecuteSkill_SendGoal_Response;

// Struct for a sequence of aimee_msgs__action__ExecuteSkill_SendGoal_Response.
typedef struct aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence
{
  aimee_msgs__action__ExecuteSkill_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/ExecuteSkill in the package aimee_msgs.
typedef struct aimee_msgs__action__ExecuteSkill_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} aimee_msgs__action__ExecuteSkill_GetResult_Request;

// Struct for a sequence of aimee_msgs__action__ExecuteSkill_GetResult_Request.
typedef struct aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence
{
  aimee_msgs__action__ExecuteSkill_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.h"

/// Struct defined in action/ExecuteSkill in the package aimee_msgs.
typedef struct aimee_msgs__action__ExecuteSkill_GetResult_Response
{
  int8_t status;
  aimee_msgs__action__ExecuteSkill_Result result;
} aimee_msgs__action__ExecuteSkill_GetResult_Response;

// Struct for a sequence of aimee_msgs__action__ExecuteSkill_GetResult_Response.
typedef struct aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence
{
  aimee_msgs__action__ExecuteSkill_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.h"

/// Struct defined in action/ExecuteSkill in the package aimee_msgs.
typedef struct aimee_msgs__action__ExecuteSkill_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  aimee_msgs__action__ExecuteSkill_Feedback feedback;
} aimee_msgs__action__ExecuteSkill_FeedbackMessage;

// Struct for a sequence of aimee_msgs__action__ExecuteSkill_FeedbackMessage.
typedef struct aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence
{
  aimee_msgs__action__ExecuteSkill_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIMEE_MSGS__ACTION__DETAIL__EXECUTE_SKILL__STRUCT_H_
