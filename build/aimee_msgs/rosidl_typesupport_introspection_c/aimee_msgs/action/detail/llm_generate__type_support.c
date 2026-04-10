// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from aimee_msgs:action/LLMGenerate.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "aimee_msgs/action/detail/llm_generate__rosidl_typesupport_introspection_c.h"
#include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "aimee_msgs/action/detail/llm_generate__functions.h"
#include "aimee_msgs/action/detail/llm_generate__struct.h"


// Include directives for member types
// Member `prompt`
// Member `system_context`
// Member `session_id`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__action__LLMGenerate_Goal__rosidl_typesupport_introspection_c__LLMGenerate_Goal_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__action__LLMGenerate_Goal__init(message_memory);
}

void aimee_msgs__action__LLMGenerate_Goal__rosidl_typesupport_introspection_c__LLMGenerate_Goal_fini_function(void * message_memory)
{
  aimee_msgs__action__LLMGenerate_Goal__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__action__LLMGenerate_Goal__rosidl_typesupport_introspection_c__LLMGenerate_Goal_message_member_array[6] = {
  {
    "prompt",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Goal, prompt),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "system_context",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Goal, system_context),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "max_tokens",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Goal, max_tokens),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "temperature",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Goal, temperature),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "stream",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Goal, stream),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "session_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Goal, session_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__action__LLMGenerate_Goal__rosidl_typesupport_introspection_c__LLMGenerate_Goal_message_members = {
  "aimee_msgs__action",  // message namespace
  "LLMGenerate_Goal",  // message name
  6,  // number of fields
  sizeof(aimee_msgs__action__LLMGenerate_Goal),
  aimee_msgs__action__LLMGenerate_Goal__rosidl_typesupport_introspection_c__LLMGenerate_Goal_message_member_array,  // message members
  aimee_msgs__action__LLMGenerate_Goal__rosidl_typesupport_introspection_c__LLMGenerate_Goal_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__action__LLMGenerate_Goal__rosidl_typesupport_introspection_c__LLMGenerate_Goal_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__action__LLMGenerate_Goal__rosidl_typesupport_introspection_c__LLMGenerate_Goal_message_type_support_handle = {
  0,
  &aimee_msgs__action__LLMGenerate_Goal__rosidl_typesupport_introspection_c__LLMGenerate_Goal_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_Goal)() {
  if (!aimee_msgs__action__LLMGenerate_Goal__rosidl_typesupport_introspection_c__LLMGenerate_Goal_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__LLMGenerate_Goal__rosidl_typesupport_introspection_c__LLMGenerate_Goal_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__action__LLMGenerate_Goal__rosidl_typesupport_introspection_c__LLMGenerate_Goal_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "aimee_msgs/action/detail/llm_generate__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aimee_msgs/action/detail/llm_generate__functions.h"
// already included above
// #include "aimee_msgs/action/detail/llm_generate__struct.h"


// Include directives for member types
// Member `response`
// Member `error_message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__action__LLMGenerate_Result__rosidl_typesupport_introspection_c__LLMGenerate_Result_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__action__LLMGenerate_Result__init(message_memory);
}

void aimee_msgs__action__LLMGenerate_Result__rosidl_typesupport_introspection_c__LLMGenerate_Result_fini_function(void * message_memory)
{
  aimee_msgs__action__LLMGenerate_Result__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__action__LLMGenerate_Result__rosidl_typesupport_introspection_c__LLMGenerate_Result_message_member_array[6] = {
  {
    "response",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Result, response),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Result, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "error_message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Result, error_message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "generation_time",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Result, generation_time),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "tokens_generated",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Result, tokens_generated),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "tokens_input",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Result, tokens_input),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__action__LLMGenerate_Result__rosidl_typesupport_introspection_c__LLMGenerate_Result_message_members = {
  "aimee_msgs__action",  // message namespace
  "LLMGenerate_Result",  // message name
  6,  // number of fields
  sizeof(aimee_msgs__action__LLMGenerate_Result),
  aimee_msgs__action__LLMGenerate_Result__rosidl_typesupport_introspection_c__LLMGenerate_Result_message_member_array,  // message members
  aimee_msgs__action__LLMGenerate_Result__rosidl_typesupport_introspection_c__LLMGenerate_Result_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__action__LLMGenerate_Result__rosidl_typesupport_introspection_c__LLMGenerate_Result_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__action__LLMGenerate_Result__rosidl_typesupport_introspection_c__LLMGenerate_Result_message_type_support_handle = {
  0,
  &aimee_msgs__action__LLMGenerate_Result__rosidl_typesupport_introspection_c__LLMGenerate_Result_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_Result)() {
  if (!aimee_msgs__action__LLMGenerate_Result__rosidl_typesupport_introspection_c__LLMGenerate_Result_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__LLMGenerate_Result__rosidl_typesupport_introspection_c__LLMGenerate_Result_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__action__LLMGenerate_Result__rosidl_typesupport_introspection_c__LLMGenerate_Result_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "aimee_msgs/action/detail/llm_generate__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aimee_msgs/action/detail/llm_generate__functions.h"
// already included above
// #include "aimee_msgs/action/detail/llm_generate__struct.h"


// Include directives for member types
// Member `partial_response`
// Member `current_word`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__action__LLMGenerate_Feedback__rosidl_typesupport_introspection_c__LLMGenerate_Feedback_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__action__LLMGenerate_Feedback__init(message_memory);
}

void aimee_msgs__action__LLMGenerate_Feedback__rosidl_typesupport_introspection_c__LLMGenerate_Feedback_fini_function(void * message_memory)
{
  aimee_msgs__action__LLMGenerate_Feedback__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__action__LLMGenerate_Feedback__rosidl_typesupport_introspection_c__LLMGenerate_Feedback_message_member_array[5] = {
  {
    "partial_response",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Feedback, partial_response),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "tokens_generated",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Feedback, tokens_generated),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "tokens_total",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Feedback, tokens_total),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "is_complete",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Feedback, is_complete),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "current_word",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_Feedback, current_word),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__action__LLMGenerate_Feedback__rosidl_typesupport_introspection_c__LLMGenerate_Feedback_message_members = {
  "aimee_msgs__action",  // message namespace
  "LLMGenerate_Feedback",  // message name
  5,  // number of fields
  sizeof(aimee_msgs__action__LLMGenerate_Feedback),
  aimee_msgs__action__LLMGenerate_Feedback__rosidl_typesupport_introspection_c__LLMGenerate_Feedback_message_member_array,  // message members
  aimee_msgs__action__LLMGenerate_Feedback__rosidl_typesupport_introspection_c__LLMGenerate_Feedback_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__action__LLMGenerate_Feedback__rosidl_typesupport_introspection_c__LLMGenerate_Feedback_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__action__LLMGenerate_Feedback__rosidl_typesupport_introspection_c__LLMGenerate_Feedback_message_type_support_handle = {
  0,
  &aimee_msgs__action__LLMGenerate_Feedback__rosidl_typesupport_introspection_c__LLMGenerate_Feedback_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_Feedback)() {
  if (!aimee_msgs__action__LLMGenerate_Feedback__rosidl_typesupport_introspection_c__LLMGenerate_Feedback_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__LLMGenerate_Feedback__rosidl_typesupport_introspection_c__LLMGenerate_Feedback_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__action__LLMGenerate_Feedback__rosidl_typesupport_introspection_c__LLMGenerate_Feedback_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "aimee_msgs/action/detail/llm_generate__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aimee_msgs/action/detail/llm_generate__functions.h"
// already included above
// #include "aimee_msgs/action/detail/llm_generate__struct.h"


// Include directives for member types
// Member `goal_id`
#include "unique_identifier_msgs/msg/uuid.h"
// Member `goal_id`
#include "unique_identifier_msgs/msg/detail/uuid__rosidl_typesupport_introspection_c.h"
// Member `goal`
#include "aimee_msgs/action/llm_generate.h"
// Member `goal`
// already included above
// #include "aimee_msgs/action/detail/llm_generate__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__action__LLMGenerate_SendGoal_Request__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__action__LLMGenerate_SendGoal_Request__init(message_memory);
}

void aimee_msgs__action__LLMGenerate_SendGoal_Request__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Request_fini_function(void * message_memory)
{
  aimee_msgs__action__LLMGenerate_SendGoal_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__action__LLMGenerate_SendGoal_Request__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Request_message_member_array[2] = {
  {
    "goal_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_SendGoal_Request, goal_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "goal",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_SendGoal_Request, goal),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__action__LLMGenerate_SendGoal_Request__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Request_message_members = {
  "aimee_msgs__action",  // message namespace
  "LLMGenerate_SendGoal_Request",  // message name
  2,  // number of fields
  sizeof(aimee_msgs__action__LLMGenerate_SendGoal_Request),
  aimee_msgs__action__LLMGenerate_SendGoal_Request__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Request_message_member_array,  // message members
  aimee_msgs__action__LLMGenerate_SendGoal_Request__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__action__LLMGenerate_SendGoal_Request__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__action__LLMGenerate_SendGoal_Request__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Request_message_type_support_handle = {
  0,
  &aimee_msgs__action__LLMGenerate_SendGoal_Request__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_SendGoal_Request)() {
  aimee_msgs__action__LLMGenerate_SendGoal_Request__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unique_identifier_msgs, msg, UUID)();
  aimee_msgs__action__LLMGenerate_SendGoal_Request__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Request_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_Goal)();
  if (!aimee_msgs__action__LLMGenerate_SendGoal_Request__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Request_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__LLMGenerate_SendGoal_Request__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__action__LLMGenerate_SendGoal_Request__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "aimee_msgs/action/detail/llm_generate__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aimee_msgs/action/detail/llm_generate__functions.h"
// already included above
// #include "aimee_msgs/action/detail/llm_generate__struct.h"


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/time.h"
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__action__LLMGenerate_SendGoal_Response__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__action__LLMGenerate_SendGoal_Response__init(message_memory);
}

void aimee_msgs__action__LLMGenerate_SendGoal_Response__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Response_fini_function(void * message_memory)
{
  aimee_msgs__action__LLMGenerate_SendGoal_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__action__LLMGenerate_SendGoal_Response__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Response_message_member_array[2] = {
  {
    "accepted",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_SendGoal_Response, accepted),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "stamp",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_SendGoal_Response, stamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__action__LLMGenerate_SendGoal_Response__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Response_message_members = {
  "aimee_msgs__action",  // message namespace
  "LLMGenerate_SendGoal_Response",  // message name
  2,  // number of fields
  sizeof(aimee_msgs__action__LLMGenerate_SendGoal_Response),
  aimee_msgs__action__LLMGenerate_SendGoal_Response__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Response_message_member_array,  // message members
  aimee_msgs__action__LLMGenerate_SendGoal_Response__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__action__LLMGenerate_SendGoal_Response__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__action__LLMGenerate_SendGoal_Response__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Response_message_type_support_handle = {
  0,
  &aimee_msgs__action__LLMGenerate_SendGoal_Response__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_SendGoal_Response)() {
  aimee_msgs__action__LLMGenerate_SendGoal_Response__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Response_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Time)();
  if (!aimee_msgs__action__LLMGenerate_SendGoal_Response__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Response_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__LLMGenerate_SendGoal_Response__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__action__LLMGenerate_SendGoal_Response__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "aimee_msgs/action/detail/llm_generate__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_service_members = {
  "aimee_msgs__action",  // service namespace
  "LLMGenerate_SendGoal",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Request_message_type_support_handle,
  NULL  // response message
  // aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_Response_message_type_support_handle
};

static rosidl_service_type_support_t aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_service_type_support_handle = {
  0,
  &aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_SendGoal_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_SendGoal_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_SendGoal)() {
  if (!aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_service_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_SendGoal_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_SendGoal_Response)()->data;
  }

  return &aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_SendGoal_service_type_support_handle;
}

// already included above
// #include <stddef.h>
// already included above
// #include "aimee_msgs/action/detail/llm_generate__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aimee_msgs/action/detail/llm_generate__functions.h"
// already included above
// #include "aimee_msgs/action/detail/llm_generate__struct.h"


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/uuid.h"
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__action__LLMGenerate_GetResult_Request__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__action__LLMGenerate_GetResult_Request__init(message_memory);
}

void aimee_msgs__action__LLMGenerate_GetResult_Request__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Request_fini_function(void * message_memory)
{
  aimee_msgs__action__LLMGenerate_GetResult_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__action__LLMGenerate_GetResult_Request__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Request_message_member_array[1] = {
  {
    "goal_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_GetResult_Request, goal_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__action__LLMGenerate_GetResult_Request__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Request_message_members = {
  "aimee_msgs__action",  // message namespace
  "LLMGenerate_GetResult_Request",  // message name
  1,  // number of fields
  sizeof(aimee_msgs__action__LLMGenerate_GetResult_Request),
  aimee_msgs__action__LLMGenerate_GetResult_Request__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Request_message_member_array,  // message members
  aimee_msgs__action__LLMGenerate_GetResult_Request__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__action__LLMGenerate_GetResult_Request__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__action__LLMGenerate_GetResult_Request__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Request_message_type_support_handle = {
  0,
  &aimee_msgs__action__LLMGenerate_GetResult_Request__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_GetResult_Request)() {
  aimee_msgs__action__LLMGenerate_GetResult_Request__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unique_identifier_msgs, msg, UUID)();
  if (!aimee_msgs__action__LLMGenerate_GetResult_Request__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Request_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__LLMGenerate_GetResult_Request__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__action__LLMGenerate_GetResult_Request__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "aimee_msgs/action/detail/llm_generate__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aimee_msgs/action/detail/llm_generate__functions.h"
// already included above
// #include "aimee_msgs/action/detail/llm_generate__struct.h"


// Include directives for member types
// Member `result`
// already included above
// #include "aimee_msgs/action/llm_generate.h"
// Member `result`
// already included above
// #include "aimee_msgs/action/detail/llm_generate__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__action__LLMGenerate_GetResult_Response__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__action__LLMGenerate_GetResult_Response__init(message_memory);
}

void aimee_msgs__action__LLMGenerate_GetResult_Response__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Response_fini_function(void * message_memory)
{
  aimee_msgs__action__LLMGenerate_GetResult_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__action__LLMGenerate_GetResult_Response__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Response_message_member_array[2] = {
  {
    "status",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_GetResult_Response, status),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "result",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_GetResult_Response, result),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__action__LLMGenerate_GetResult_Response__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Response_message_members = {
  "aimee_msgs__action",  // message namespace
  "LLMGenerate_GetResult_Response",  // message name
  2,  // number of fields
  sizeof(aimee_msgs__action__LLMGenerate_GetResult_Response),
  aimee_msgs__action__LLMGenerate_GetResult_Response__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Response_message_member_array,  // message members
  aimee_msgs__action__LLMGenerate_GetResult_Response__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__action__LLMGenerate_GetResult_Response__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__action__LLMGenerate_GetResult_Response__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Response_message_type_support_handle = {
  0,
  &aimee_msgs__action__LLMGenerate_GetResult_Response__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_GetResult_Response)() {
  aimee_msgs__action__LLMGenerate_GetResult_Response__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Response_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_Result)();
  if (!aimee_msgs__action__LLMGenerate_GetResult_Response__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Response_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__LLMGenerate_GetResult_Response__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__action__LLMGenerate_GetResult_Response__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "aimee_msgs/action/detail/llm_generate__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_service_members = {
  "aimee_msgs__action",  // service namespace
  "LLMGenerate_GetResult",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Request_message_type_support_handle,
  NULL  // response message
  // aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_Response_message_type_support_handle
};

static rosidl_service_type_support_t aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_service_type_support_handle = {
  0,
  &aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_GetResult_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_GetResult_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_GetResult)() {
  if (!aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_service_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_GetResult_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_GetResult_Response)()->data;
  }

  return &aimee_msgs__action__detail__llm_generate__rosidl_typesupport_introspection_c__LLMGenerate_GetResult_service_type_support_handle;
}

// already included above
// #include <stddef.h>
// already included above
// #include "aimee_msgs/action/detail/llm_generate__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aimee_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aimee_msgs/action/detail/llm_generate__functions.h"
// already included above
// #include "aimee_msgs/action/detail/llm_generate__struct.h"


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/uuid.h"
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__rosidl_typesupport_introspection_c.h"
// Member `feedback`
// already included above
// #include "aimee_msgs/action/llm_generate.h"
// Member `feedback`
// already included above
// #include "aimee_msgs/action/detail/llm_generate__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aimee_msgs__action__LLMGenerate_FeedbackMessage__rosidl_typesupport_introspection_c__LLMGenerate_FeedbackMessage_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aimee_msgs__action__LLMGenerate_FeedbackMessage__init(message_memory);
}

void aimee_msgs__action__LLMGenerate_FeedbackMessage__rosidl_typesupport_introspection_c__LLMGenerate_FeedbackMessage_fini_function(void * message_memory)
{
  aimee_msgs__action__LLMGenerate_FeedbackMessage__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aimee_msgs__action__LLMGenerate_FeedbackMessage__rosidl_typesupport_introspection_c__LLMGenerate_FeedbackMessage_message_member_array[2] = {
  {
    "goal_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_FeedbackMessage, goal_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "feedback",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aimee_msgs__action__LLMGenerate_FeedbackMessage, feedback),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aimee_msgs__action__LLMGenerate_FeedbackMessage__rosidl_typesupport_introspection_c__LLMGenerate_FeedbackMessage_message_members = {
  "aimee_msgs__action",  // message namespace
  "LLMGenerate_FeedbackMessage",  // message name
  2,  // number of fields
  sizeof(aimee_msgs__action__LLMGenerate_FeedbackMessage),
  aimee_msgs__action__LLMGenerate_FeedbackMessage__rosidl_typesupport_introspection_c__LLMGenerate_FeedbackMessage_message_member_array,  // message members
  aimee_msgs__action__LLMGenerate_FeedbackMessage__rosidl_typesupport_introspection_c__LLMGenerate_FeedbackMessage_init_function,  // function to initialize message memory (memory has to be allocated)
  aimee_msgs__action__LLMGenerate_FeedbackMessage__rosidl_typesupport_introspection_c__LLMGenerate_FeedbackMessage_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aimee_msgs__action__LLMGenerate_FeedbackMessage__rosidl_typesupport_introspection_c__LLMGenerate_FeedbackMessage_message_type_support_handle = {
  0,
  &aimee_msgs__action__LLMGenerate_FeedbackMessage__rosidl_typesupport_introspection_c__LLMGenerate_FeedbackMessage_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aimee_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_FeedbackMessage)() {
  aimee_msgs__action__LLMGenerate_FeedbackMessage__rosidl_typesupport_introspection_c__LLMGenerate_FeedbackMessage_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unique_identifier_msgs, msg, UUID)();
  aimee_msgs__action__LLMGenerate_FeedbackMessage__rosidl_typesupport_introspection_c__LLMGenerate_FeedbackMessage_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aimee_msgs, action, LLMGenerate_Feedback)();
  if (!aimee_msgs__action__LLMGenerate_FeedbackMessage__rosidl_typesupport_introspection_c__LLMGenerate_FeedbackMessage_message_type_support_handle.typesupport_identifier) {
    aimee_msgs__action__LLMGenerate_FeedbackMessage__rosidl_typesupport_introspection_c__LLMGenerate_FeedbackMessage_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aimee_msgs__action__LLMGenerate_FeedbackMessage__rosidl_typesupport_introspection_c__LLMGenerate_FeedbackMessage_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
