// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aimee_msgs:action/LLMGenerate.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__ACTION__DETAIL__LLM_GENERATE__STRUCT_H_
#define AIMEE_MSGS__ACTION__DETAIL__LLM_GENERATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'prompt'
// Member 'system_context'
// Member 'session_id'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/LLMGenerate in the package aimee_msgs.
typedef struct aimee_msgs__action__LLMGenerate_Goal
{
  /// Goal: Request for LLM generation
  /// User prompt
  rosidl_runtime_c__String prompt;
  /// System prompt/persona
  rosidl_runtime_c__String system_context;
  /// Maximum tokens to generate (default: 150)
  int32_t max_tokens;
  /// Sampling temperature (default: 0.7)
  float temperature;
  /// Enable streaming feedback (default: true)
  bool stream;
  /// Session identifier for context
  rosidl_runtime_c__String session_id;
} aimee_msgs__action__LLMGenerate_Goal;

// Struct for a sequence of aimee_msgs__action__LLMGenerate_Goal.
typedef struct aimee_msgs__action__LLMGenerate_Goal__Sequence
{
  aimee_msgs__action__LLMGenerate_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__action__LLMGenerate_Goal__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'response'
// Member 'error_message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/LLMGenerate in the package aimee_msgs.
typedef struct aimee_msgs__action__LLMGenerate_Result
{
  /// Complete generated text
  rosidl_runtime_c__String response;
  /// True if generation succeeded
  bool success;
  /// Error details if failed
  rosidl_runtime_c__String error_message;
  /// Time taken in seconds
  float generation_time;
  /// Total tokens generated
  int32_t tokens_generated;
  /// Input prompt tokens
  int32_t tokens_input;
} aimee_msgs__action__LLMGenerate_Result;

// Struct for a sequence of aimee_msgs__action__LLMGenerate_Result.
typedef struct aimee_msgs__action__LLMGenerate_Result__Sequence
{
  aimee_msgs__action__LLMGenerate_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__action__LLMGenerate_Result__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'partial_response'
// Member 'current_word'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/LLMGenerate in the package aimee_msgs.
typedef struct aimee_msgs__action__LLMGenerate_Feedback
{
  /// Cumulative text so far
  rosidl_runtime_c__String partial_response;
  /// Tokens generated so far
  int32_t tokens_generated;
  /// Estimated total tokens
  int32_t tokens_total;
  /// True if generation finished
  bool is_complete;
  /// Currently generating word (optional)
  rosidl_runtime_c__String current_word;
} aimee_msgs__action__LLMGenerate_Feedback;

// Struct for a sequence of aimee_msgs__action__LLMGenerate_Feedback.
typedef struct aimee_msgs__action__LLMGenerate_Feedback__Sequence
{
  aimee_msgs__action__LLMGenerate_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__action__LLMGenerate_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "aimee_msgs/action/detail/llm_generate__struct.h"

/// Struct defined in action/LLMGenerate in the package aimee_msgs.
typedef struct aimee_msgs__action__LLMGenerate_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  aimee_msgs__action__LLMGenerate_Goal goal;
} aimee_msgs__action__LLMGenerate_SendGoal_Request;

// Struct for a sequence of aimee_msgs__action__LLMGenerate_SendGoal_Request.
typedef struct aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence
{
  aimee_msgs__action__LLMGenerate_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/LLMGenerate in the package aimee_msgs.
typedef struct aimee_msgs__action__LLMGenerate_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} aimee_msgs__action__LLMGenerate_SendGoal_Response;

// Struct for a sequence of aimee_msgs__action__LLMGenerate_SendGoal_Response.
typedef struct aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence
{
  aimee_msgs__action__LLMGenerate_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/LLMGenerate in the package aimee_msgs.
typedef struct aimee_msgs__action__LLMGenerate_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} aimee_msgs__action__LLMGenerate_GetResult_Request;

// Struct for a sequence of aimee_msgs__action__LLMGenerate_GetResult_Request.
typedef struct aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence
{
  aimee_msgs__action__LLMGenerate_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "aimee_msgs/action/detail/llm_generate__struct.h"

/// Struct defined in action/LLMGenerate in the package aimee_msgs.
typedef struct aimee_msgs__action__LLMGenerate_GetResult_Response
{
  int8_t status;
  aimee_msgs__action__LLMGenerate_Result result;
} aimee_msgs__action__LLMGenerate_GetResult_Response;

// Struct for a sequence of aimee_msgs__action__LLMGenerate_GetResult_Response.
typedef struct aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence
{
  aimee_msgs__action__LLMGenerate_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "aimee_msgs/action/detail/llm_generate__struct.h"

/// Struct defined in action/LLMGenerate in the package aimee_msgs.
typedef struct aimee_msgs__action__LLMGenerate_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  aimee_msgs__action__LLMGenerate_Feedback feedback;
} aimee_msgs__action__LLMGenerate_FeedbackMessage;

// Struct for a sequence of aimee_msgs__action__LLMGenerate_FeedbackMessage.
typedef struct aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence
{
  aimee_msgs__action__LLMGenerate_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIMEE_MSGS__ACTION__DETAIL__LLM_GENERATE__STRUCT_H_
