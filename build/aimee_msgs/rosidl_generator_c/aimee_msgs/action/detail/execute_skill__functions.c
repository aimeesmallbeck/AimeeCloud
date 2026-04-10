// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aimee_msgs:action/ExecuteSkill.idl
// generated code does not contain a copyright notice
#include "aimee_msgs/action/detail/execute_skill__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `skill_id`
// Member `user_input`
// Member `user_context`
// Member `session_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `robot_state`
#include "aimee_msgs/msg/detail/robot_state__functions.h"

bool
aimee_msgs__action__ExecuteSkill_Goal__init(aimee_msgs__action__ExecuteSkill_Goal * msg)
{
  if (!msg) {
    return false;
  }
  // skill_id
  if (!rosidl_runtime_c__String__init(&msg->skill_id)) {
    aimee_msgs__action__ExecuteSkill_Goal__fini(msg);
    return false;
  }
  // user_input
  if (!rosidl_runtime_c__String__init(&msg->user_input)) {
    aimee_msgs__action__ExecuteSkill_Goal__fini(msg);
    return false;
  }
  // robot_state
  if (!aimee_msgs__msg__RobotState__init(&msg->robot_state)) {
    aimee_msgs__action__ExecuteSkill_Goal__fini(msg);
    return false;
  }
  // user_context
  if (!rosidl_runtime_c__String__init(&msg->user_context)) {
    aimee_msgs__action__ExecuteSkill_Goal__fini(msg);
    return false;
  }
  // session_id
  if (!rosidl_runtime_c__String__init(&msg->session_id)) {
    aimee_msgs__action__ExecuteSkill_Goal__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__action__ExecuteSkill_Goal__fini(aimee_msgs__action__ExecuteSkill_Goal * msg)
{
  if (!msg) {
    return;
  }
  // skill_id
  rosidl_runtime_c__String__fini(&msg->skill_id);
  // user_input
  rosidl_runtime_c__String__fini(&msg->user_input);
  // robot_state
  aimee_msgs__msg__RobotState__fini(&msg->robot_state);
  // user_context
  rosidl_runtime_c__String__fini(&msg->user_context);
  // session_id
  rosidl_runtime_c__String__fini(&msg->session_id);
}

bool
aimee_msgs__action__ExecuteSkill_Goal__are_equal(const aimee_msgs__action__ExecuteSkill_Goal * lhs, const aimee_msgs__action__ExecuteSkill_Goal * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // skill_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->skill_id), &(rhs->skill_id)))
  {
    return false;
  }
  // user_input
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->user_input), &(rhs->user_input)))
  {
    return false;
  }
  // robot_state
  if (!aimee_msgs__msg__RobotState__are_equal(
      &(lhs->robot_state), &(rhs->robot_state)))
  {
    return false;
  }
  // user_context
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->user_context), &(rhs->user_context)))
  {
    return false;
  }
  // session_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->session_id), &(rhs->session_id)))
  {
    return false;
  }
  return true;
}

bool
aimee_msgs__action__ExecuteSkill_Goal__copy(
  const aimee_msgs__action__ExecuteSkill_Goal * input,
  aimee_msgs__action__ExecuteSkill_Goal * output)
{
  if (!input || !output) {
    return false;
  }
  // skill_id
  if (!rosidl_runtime_c__String__copy(
      &(input->skill_id), &(output->skill_id)))
  {
    return false;
  }
  // user_input
  if (!rosidl_runtime_c__String__copy(
      &(input->user_input), &(output->user_input)))
  {
    return false;
  }
  // robot_state
  if (!aimee_msgs__msg__RobotState__copy(
      &(input->robot_state), &(output->robot_state)))
  {
    return false;
  }
  // user_context
  if (!rosidl_runtime_c__String__copy(
      &(input->user_context), &(output->user_context)))
  {
    return false;
  }
  // session_id
  if (!rosidl_runtime_c__String__copy(
      &(input->session_id), &(output->session_id)))
  {
    return false;
  }
  return true;
}

aimee_msgs__action__ExecuteSkill_Goal *
aimee_msgs__action__ExecuteSkill_Goal__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_Goal * msg = (aimee_msgs__action__ExecuteSkill_Goal *)allocator.allocate(sizeof(aimee_msgs__action__ExecuteSkill_Goal), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__action__ExecuteSkill_Goal));
  bool success = aimee_msgs__action__ExecuteSkill_Goal__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__action__ExecuteSkill_Goal__destroy(aimee_msgs__action__ExecuteSkill_Goal * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__action__ExecuteSkill_Goal__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__action__ExecuteSkill_Goal__Sequence__init(aimee_msgs__action__ExecuteSkill_Goal__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_Goal * data = NULL;

  if (size) {
    data = (aimee_msgs__action__ExecuteSkill_Goal *)allocator.zero_allocate(size, sizeof(aimee_msgs__action__ExecuteSkill_Goal), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__action__ExecuteSkill_Goal__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__action__ExecuteSkill_Goal__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
aimee_msgs__action__ExecuteSkill_Goal__Sequence__fini(aimee_msgs__action__ExecuteSkill_Goal__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      aimee_msgs__action__ExecuteSkill_Goal__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

aimee_msgs__action__ExecuteSkill_Goal__Sequence *
aimee_msgs__action__ExecuteSkill_Goal__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_Goal__Sequence * array = (aimee_msgs__action__ExecuteSkill_Goal__Sequence *)allocator.allocate(sizeof(aimee_msgs__action__ExecuteSkill_Goal__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__action__ExecuteSkill_Goal__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__action__ExecuteSkill_Goal__Sequence__destroy(aimee_msgs__action__ExecuteSkill_Goal__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__action__ExecuteSkill_Goal__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__action__ExecuteSkill_Goal__Sequence__are_equal(const aimee_msgs__action__ExecuteSkill_Goal__Sequence * lhs, const aimee_msgs__action__ExecuteSkill_Goal__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__action__ExecuteSkill_Goal__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__action__ExecuteSkill_Goal__Sequence__copy(
  const aimee_msgs__action__ExecuteSkill_Goal__Sequence * input,
  aimee_msgs__action__ExecuteSkill_Goal__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__action__ExecuteSkill_Goal);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__action__ExecuteSkill_Goal * data =
      (aimee_msgs__action__ExecuteSkill_Goal *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__action__ExecuteSkill_Goal__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__action__ExecuteSkill_Goal__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__action__ExecuteSkill_Goal__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `response_text`
// Member `tts_audio_path`
// Member `error_message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"
// Member `motor_actions`
#include "aimee_msgs/msg/detail/motor_action__functions.h"
// Member `camera_actions`
#include "aimee_msgs/msg/detail/camera_action__functions.h"
// Member `led_actions`
#include "aimee_msgs/msg/detail/led_action__functions.h"

bool
aimee_msgs__action__ExecuteSkill_Result__init(aimee_msgs__action__ExecuteSkill_Result * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // response_text
  if (!rosidl_runtime_c__String__init(&msg->response_text)) {
    aimee_msgs__action__ExecuteSkill_Result__fini(msg);
    return false;
  }
  // tts_audio_path
  if (!rosidl_runtime_c__String__init(&msg->tts_audio_path)) {
    aimee_msgs__action__ExecuteSkill_Result__fini(msg);
    return false;
  }
  // error_message
  if (!rosidl_runtime_c__String__init(&msg->error_message)) {
    aimee_msgs__action__ExecuteSkill_Result__fini(msg);
    return false;
  }
  // motor_actions
  if (!aimee_msgs__msg__MotorAction__Sequence__init(&msg->motor_actions, 0)) {
    aimee_msgs__action__ExecuteSkill_Result__fini(msg);
    return false;
  }
  // camera_actions
  if (!aimee_msgs__msg__CameraAction__Sequence__init(&msg->camera_actions, 0)) {
    aimee_msgs__action__ExecuteSkill_Result__fini(msg);
    return false;
  }
  // led_actions
  if (!aimee_msgs__msg__LEDAction__Sequence__init(&msg->led_actions, 0)) {
    aimee_msgs__action__ExecuteSkill_Result__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__action__ExecuteSkill_Result__fini(aimee_msgs__action__ExecuteSkill_Result * msg)
{
  if (!msg) {
    return;
  }
  // success
  // response_text
  rosidl_runtime_c__String__fini(&msg->response_text);
  // tts_audio_path
  rosidl_runtime_c__String__fini(&msg->tts_audio_path);
  // error_message
  rosidl_runtime_c__String__fini(&msg->error_message);
  // motor_actions
  aimee_msgs__msg__MotorAction__Sequence__fini(&msg->motor_actions);
  // camera_actions
  aimee_msgs__msg__CameraAction__Sequence__fini(&msg->camera_actions);
  // led_actions
  aimee_msgs__msg__LEDAction__Sequence__fini(&msg->led_actions);
}

bool
aimee_msgs__action__ExecuteSkill_Result__are_equal(const aimee_msgs__action__ExecuteSkill_Result * lhs, const aimee_msgs__action__ExecuteSkill_Result * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // response_text
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->response_text), &(rhs->response_text)))
  {
    return false;
  }
  // tts_audio_path
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->tts_audio_path), &(rhs->tts_audio_path)))
  {
    return false;
  }
  // error_message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->error_message), &(rhs->error_message)))
  {
    return false;
  }
  // motor_actions
  if (!aimee_msgs__msg__MotorAction__Sequence__are_equal(
      &(lhs->motor_actions), &(rhs->motor_actions)))
  {
    return false;
  }
  // camera_actions
  if (!aimee_msgs__msg__CameraAction__Sequence__are_equal(
      &(lhs->camera_actions), &(rhs->camera_actions)))
  {
    return false;
  }
  // led_actions
  if (!aimee_msgs__msg__LEDAction__Sequence__are_equal(
      &(lhs->led_actions), &(rhs->led_actions)))
  {
    return false;
  }
  return true;
}

bool
aimee_msgs__action__ExecuteSkill_Result__copy(
  const aimee_msgs__action__ExecuteSkill_Result * input,
  aimee_msgs__action__ExecuteSkill_Result * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // response_text
  if (!rosidl_runtime_c__String__copy(
      &(input->response_text), &(output->response_text)))
  {
    return false;
  }
  // tts_audio_path
  if (!rosidl_runtime_c__String__copy(
      &(input->tts_audio_path), &(output->tts_audio_path)))
  {
    return false;
  }
  // error_message
  if (!rosidl_runtime_c__String__copy(
      &(input->error_message), &(output->error_message)))
  {
    return false;
  }
  // motor_actions
  if (!aimee_msgs__msg__MotorAction__Sequence__copy(
      &(input->motor_actions), &(output->motor_actions)))
  {
    return false;
  }
  // camera_actions
  if (!aimee_msgs__msg__CameraAction__Sequence__copy(
      &(input->camera_actions), &(output->camera_actions)))
  {
    return false;
  }
  // led_actions
  if (!aimee_msgs__msg__LEDAction__Sequence__copy(
      &(input->led_actions), &(output->led_actions)))
  {
    return false;
  }
  return true;
}

aimee_msgs__action__ExecuteSkill_Result *
aimee_msgs__action__ExecuteSkill_Result__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_Result * msg = (aimee_msgs__action__ExecuteSkill_Result *)allocator.allocate(sizeof(aimee_msgs__action__ExecuteSkill_Result), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__action__ExecuteSkill_Result));
  bool success = aimee_msgs__action__ExecuteSkill_Result__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__action__ExecuteSkill_Result__destroy(aimee_msgs__action__ExecuteSkill_Result * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__action__ExecuteSkill_Result__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__action__ExecuteSkill_Result__Sequence__init(aimee_msgs__action__ExecuteSkill_Result__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_Result * data = NULL;

  if (size) {
    data = (aimee_msgs__action__ExecuteSkill_Result *)allocator.zero_allocate(size, sizeof(aimee_msgs__action__ExecuteSkill_Result), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__action__ExecuteSkill_Result__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__action__ExecuteSkill_Result__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
aimee_msgs__action__ExecuteSkill_Result__Sequence__fini(aimee_msgs__action__ExecuteSkill_Result__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      aimee_msgs__action__ExecuteSkill_Result__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

aimee_msgs__action__ExecuteSkill_Result__Sequence *
aimee_msgs__action__ExecuteSkill_Result__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_Result__Sequence * array = (aimee_msgs__action__ExecuteSkill_Result__Sequence *)allocator.allocate(sizeof(aimee_msgs__action__ExecuteSkill_Result__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__action__ExecuteSkill_Result__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__action__ExecuteSkill_Result__Sequence__destroy(aimee_msgs__action__ExecuteSkill_Result__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__action__ExecuteSkill_Result__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__action__ExecuteSkill_Result__Sequence__are_equal(const aimee_msgs__action__ExecuteSkill_Result__Sequence * lhs, const aimee_msgs__action__ExecuteSkill_Result__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__action__ExecuteSkill_Result__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__action__ExecuteSkill_Result__Sequence__copy(
  const aimee_msgs__action__ExecuteSkill_Result__Sequence * input,
  aimee_msgs__action__ExecuteSkill_Result__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__action__ExecuteSkill_Result);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__action__ExecuteSkill_Result * data =
      (aimee_msgs__action__ExecuteSkill_Result *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__action__ExecuteSkill_Result__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__action__ExecuteSkill_Result__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__action__ExecuteSkill_Result__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `status`
// Member `current_action`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
aimee_msgs__action__ExecuteSkill_Feedback__init(aimee_msgs__action__ExecuteSkill_Feedback * msg)
{
  if (!msg) {
    return false;
  }
  // status
  if (!rosidl_runtime_c__String__init(&msg->status)) {
    aimee_msgs__action__ExecuteSkill_Feedback__fini(msg);
    return false;
  }
  // current_action
  if (!rosidl_runtime_c__String__init(&msg->current_action)) {
    aimee_msgs__action__ExecuteSkill_Feedback__fini(msg);
    return false;
  }
  // progress
  // can_cancel
  return true;
}

void
aimee_msgs__action__ExecuteSkill_Feedback__fini(aimee_msgs__action__ExecuteSkill_Feedback * msg)
{
  if (!msg) {
    return;
  }
  // status
  rosidl_runtime_c__String__fini(&msg->status);
  // current_action
  rosidl_runtime_c__String__fini(&msg->current_action);
  // progress
  // can_cancel
}

bool
aimee_msgs__action__ExecuteSkill_Feedback__are_equal(const aimee_msgs__action__ExecuteSkill_Feedback * lhs, const aimee_msgs__action__ExecuteSkill_Feedback * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->status), &(rhs->status)))
  {
    return false;
  }
  // current_action
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->current_action), &(rhs->current_action)))
  {
    return false;
  }
  // progress
  if (lhs->progress != rhs->progress) {
    return false;
  }
  // can_cancel
  if (lhs->can_cancel != rhs->can_cancel) {
    return false;
  }
  return true;
}

bool
aimee_msgs__action__ExecuteSkill_Feedback__copy(
  const aimee_msgs__action__ExecuteSkill_Feedback * input,
  aimee_msgs__action__ExecuteSkill_Feedback * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  if (!rosidl_runtime_c__String__copy(
      &(input->status), &(output->status)))
  {
    return false;
  }
  // current_action
  if (!rosidl_runtime_c__String__copy(
      &(input->current_action), &(output->current_action)))
  {
    return false;
  }
  // progress
  output->progress = input->progress;
  // can_cancel
  output->can_cancel = input->can_cancel;
  return true;
}

aimee_msgs__action__ExecuteSkill_Feedback *
aimee_msgs__action__ExecuteSkill_Feedback__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_Feedback * msg = (aimee_msgs__action__ExecuteSkill_Feedback *)allocator.allocate(sizeof(aimee_msgs__action__ExecuteSkill_Feedback), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__action__ExecuteSkill_Feedback));
  bool success = aimee_msgs__action__ExecuteSkill_Feedback__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__action__ExecuteSkill_Feedback__destroy(aimee_msgs__action__ExecuteSkill_Feedback * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__action__ExecuteSkill_Feedback__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__action__ExecuteSkill_Feedback__Sequence__init(aimee_msgs__action__ExecuteSkill_Feedback__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_Feedback * data = NULL;

  if (size) {
    data = (aimee_msgs__action__ExecuteSkill_Feedback *)allocator.zero_allocate(size, sizeof(aimee_msgs__action__ExecuteSkill_Feedback), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__action__ExecuteSkill_Feedback__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__action__ExecuteSkill_Feedback__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
aimee_msgs__action__ExecuteSkill_Feedback__Sequence__fini(aimee_msgs__action__ExecuteSkill_Feedback__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      aimee_msgs__action__ExecuteSkill_Feedback__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

aimee_msgs__action__ExecuteSkill_Feedback__Sequence *
aimee_msgs__action__ExecuteSkill_Feedback__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_Feedback__Sequence * array = (aimee_msgs__action__ExecuteSkill_Feedback__Sequence *)allocator.allocate(sizeof(aimee_msgs__action__ExecuteSkill_Feedback__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__action__ExecuteSkill_Feedback__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__action__ExecuteSkill_Feedback__Sequence__destroy(aimee_msgs__action__ExecuteSkill_Feedback__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__action__ExecuteSkill_Feedback__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__action__ExecuteSkill_Feedback__Sequence__are_equal(const aimee_msgs__action__ExecuteSkill_Feedback__Sequence * lhs, const aimee_msgs__action__ExecuteSkill_Feedback__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__action__ExecuteSkill_Feedback__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__action__ExecuteSkill_Feedback__Sequence__copy(
  const aimee_msgs__action__ExecuteSkill_Feedback__Sequence * input,
  aimee_msgs__action__ExecuteSkill_Feedback__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__action__ExecuteSkill_Feedback);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__action__ExecuteSkill_Feedback * data =
      (aimee_msgs__action__ExecuteSkill_Feedback *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__action__ExecuteSkill_Feedback__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__action__ExecuteSkill_Feedback__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__action__ExecuteSkill_Feedback__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
#include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `goal`
// already included above
// #include "aimee_msgs/action/detail/execute_skill__functions.h"

bool
aimee_msgs__action__ExecuteSkill_SendGoal_Request__init(aimee_msgs__action__ExecuteSkill_SendGoal_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    aimee_msgs__action__ExecuteSkill_SendGoal_Request__fini(msg);
    return false;
  }
  // goal
  if (!aimee_msgs__action__ExecuteSkill_Goal__init(&msg->goal)) {
    aimee_msgs__action__ExecuteSkill_SendGoal_Request__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__action__ExecuteSkill_SendGoal_Request__fini(aimee_msgs__action__ExecuteSkill_SendGoal_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // goal
  aimee_msgs__action__ExecuteSkill_Goal__fini(&msg->goal);
}

bool
aimee_msgs__action__ExecuteSkill_SendGoal_Request__are_equal(const aimee_msgs__action__ExecuteSkill_SendGoal_Request * lhs, const aimee_msgs__action__ExecuteSkill_SendGoal_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // goal
  if (!aimee_msgs__action__ExecuteSkill_Goal__are_equal(
      &(lhs->goal), &(rhs->goal)))
  {
    return false;
  }
  return true;
}

bool
aimee_msgs__action__ExecuteSkill_SendGoal_Request__copy(
  const aimee_msgs__action__ExecuteSkill_SendGoal_Request * input,
  aimee_msgs__action__ExecuteSkill_SendGoal_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // goal
  if (!aimee_msgs__action__ExecuteSkill_Goal__copy(
      &(input->goal), &(output->goal)))
  {
    return false;
  }
  return true;
}

aimee_msgs__action__ExecuteSkill_SendGoal_Request *
aimee_msgs__action__ExecuteSkill_SendGoal_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_SendGoal_Request * msg = (aimee_msgs__action__ExecuteSkill_SendGoal_Request *)allocator.allocate(sizeof(aimee_msgs__action__ExecuteSkill_SendGoal_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__action__ExecuteSkill_SendGoal_Request));
  bool success = aimee_msgs__action__ExecuteSkill_SendGoal_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__action__ExecuteSkill_SendGoal_Request__destroy(aimee_msgs__action__ExecuteSkill_SendGoal_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__action__ExecuteSkill_SendGoal_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence__init(aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_SendGoal_Request * data = NULL;

  if (size) {
    data = (aimee_msgs__action__ExecuteSkill_SendGoal_Request *)allocator.zero_allocate(size, sizeof(aimee_msgs__action__ExecuteSkill_SendGoal_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__action__ExecuteSkill_SendGoal_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__action__ExecuteSkill_SendGoal_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence__fini(aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      aimee_msgs__action__ExecuteSkill_SendGoal_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence *
aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence * array = (aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence *)allocator.allocate(sizeof(aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence__destroy(aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence__are_equal(const aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence * lhs, const aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__action__ExecuteSkill_SendGoal_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence__copy(
  const aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence * input,
  aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__action__ExecuteSkill_SendGoal_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__action__ExecuteSkill_SendGoal_Request * data =
      (aimee_msgs__action__ExecuteSkill_SendGoal_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__action__ExecuteSkill_SendGoal_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__action__ExecuteSkill_SendGoal_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__action__ExecuteSkill_SendGoal_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
aimee_msgs__action__ExecuteSkill_SendGoal_Response__init(aimee_msgs__action__ExecuteSkill_SendGoal_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    aimee_msgs__action__ExecuteSkill_SendGoal_Response__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__action__ExecuteSkill_SendGoal_Response__fini(aimee_msgs__action__ExecuteSkill_SendGoal_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
}

bool
aimee_msgs__action__ExecuteSkill_SendGoal_Response__are_equal(const aimee_msgs__action__ExecuteSkill_SendGoal_Response * lhs, const aimee_msgs__action__ExecuteSkill_SendGoal_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // accepted
  if (lhs->accepted != rhs->accepted) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->stamp), &(rhs->stamp)))
  {
    return false;
  }
  return true;
}

bool
aimee_msgs__action__ExecuteSkill_SendGoal_Response__copy(
  const aimee_msgs__action__ExecuteSkill_SendGoal_Response * input,
  aimee_msgs__action__ExecuteSkill_SendGoal_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // accepted
  output->accepted = input->accepted;
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  return true;
}

aimee_msgs__action__ExecuteSkill_SendGoal_Response *
aimee_msgs__action__ExecuteSkill_SendGoal_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_SendGoal_Response * msg = (aimee_msgs__action__ExecuteSkill_SendGoal_Response *)allocator.allocate(sizeof(aimee_msgs__action__ExecuteSkill_SendGoal_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__action__ExecuteSkill_SendGoal_Response));
  bool success = aimee_msgs__action__ExecuteSkill_SendGoal_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__action__ExecuteSkill_SendGoal_Response__destroy(aimee_msgs__action__ExecuteSkill_SendGoal_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__action__ExecuteSkill_SendGoal_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence__init(aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_SendGoal_Response * data = NULL;

  if (size) {
    data = (aimee_msgs__action__ExecuteSkill_SendGoal_Response *)allocator.zero_allocate(size, sizeof(aimee_msgs__action__ExecuteSkill_SendGoal_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__action__ExecuteSkill_SendGoal_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__action__ExecuteSkill_SendGoal_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence__fini(aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      aimee_msgs__action__ExecuteSkill_SendGoal_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence *
aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence * array = (aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence *)allocator.allocate(sizeof(aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence__destroy(aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence__are_equal(const aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence * lhs, const aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__action__ExecuteSkill_SendGoal_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence__copy(
  const aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence * input,
  aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__action__ExecuteSkill_SendGoal_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__action__ExecuteSkill_SendGoal_Response * data =
      (aimee_msgs__action__ExecuteSkill_SendGoal_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__action__ExecuteSkill_SendGoal_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__action__ExecuteSkill_SendGoal_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__action__ExecuteSkill_SendGoal_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"

bool
aimee_msgs__action__ExecuteSkill_GetResult_Request__init(aimee_msgs__action__ExecuteSkill_GetResult_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    aimee_msgs__action__ExecuteSkill_GetResult_Request__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__action__ExecuteSkill_GetResult_Request__fini(aimee_msgs__action__ExecuteSkill_GetResult_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
}

bool
aimee_msgs__action__ExecuteSkill_GetResult_Request__are_equal(const aimee_msgs__action__ExecuteSkill_GetResult_Request * lhs, const aimee_msgs__action__ExecuteSkill_GetResult_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  return true;
}

bool
aimee_msgs__action__ExecuteSkill_GetResult_Request__copy(
  const aimee_msgs__action__ExecuteSkill_GetResult_Request * input,
  aimee_msgs__action__ExecuteSkill_GetResult_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  return true;
}

aimee_msgs__action__ExecuteSkill_GetResult_Request *
aimee_msgs__action__ExecuteSkill_GetResult_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_GetResult_Request * msg = (aimee_msgs__action__ExecuteSkill_GetResult_Request *)allocator.allocate(sizeof(aimee_msgs__action__ExecuteSkill_GetResult_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__action__ExecuteSkill_GetResult_Request));
  bool success = aimee_msgs__action__ExecuteSkill_GetResult_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__action__ExecuteSkill_GetResult_Request__destroy(aimee_msgs__action__ExecuteSkill_GetResult_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__action__ExecuteSkill_GetResult_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence__init(aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_GetResult_Request * data = NULL;

  if (size) {
    data = (aimee_msgs__action__ExecuteSkill_GetResult_Request *)allocator.zero_allocate(size, sizeof(aimee_msgs__action__ExecuteSkill_GetResult_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__action__ExecuteSkill_GetResult_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__action__ExecuteSkill_GetResult_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence__fini(aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      aimee_msgs__action__ExecuteSkill_GetResult_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence *
aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence * array = (aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence *)allocator.allocate(sizeof(aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence__destroy(aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence__are_equal(const aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence * lhs, const aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__action__ExecuteSkill_GetResult_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence__copy(
  const aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence * input,
  aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__action__ExecuteSkill_GetResult_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__action__ExecuteSkill_GetResult_Request * data =
      (aimee_msgs__action__ExecuteSkill_GetResult_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__action__ExecuteSkill_GetResult_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__action__ExecuteSkill_GetResult_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__action__ExecuteSkill_GetResult_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `result`
// already included above
// #include "aimee_msgs/action/detail/execute_skill__functions.h"

bool
aimee_msgs__action__ExecuteSkill_GetResult_Response__init(aimee_msgs__action__ExecuteSkill_GetResult_Response * msg)
{
  if (!msg) {
    return false;
  }
  // status
  // result
  if (!aimee_msgs__action__ExecuteSkill_Result__init(&msg->result)) {
    aimee_msgs__action__ExecuteSkill_GetResult_Response__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__action__ExecuteSkill_GetResult_Response__fini(aimee_msgs__action__ExecuteSkill_GetResult_Response * msg)
{
  if (!msg) {
    return;
  }
  // status
  // result
  aimee_msgs__action__ExecuteSkill_Result__fini(&msg->result);
}

bool
aimee_msgs__action__ExecuteSkill_GetResult_Response__are_equal(const aimee_msgs__action__ExecuteSkill_GetResult_Response * lhs, const aimee_msgs__action__ExecuteSkill_GetResult_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  // result
  if (!aimee_msgs__action__ExecuteSkill_Result__are_equal(
      &(lhs->result), &(rhs->result)))
  {
    return false;
  }
  return true;
}

bool
aimee_msgs__action__ExecuteSkill_GetResult_Response__copy(
  const aimee_msgs__action__ExecuteSkill_GetResult_Response * input,
  aimee_msgs__action__ExecuteSkill_GetResult_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  // result
  if (!aimee_msgs__action__ExecuteSkill_Result__copy(
      &(input->result), &(output->result)))
  {
    return false;
  }
  return true;
}

aimee_msgs__action__ExecuteSkill_GetResult_Response *
aimee_msgs__action__ExecuteSkill_GetResult_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_GetResult_Response * msg = (aimee_msgs__action__ExecuteSkill_GetResult_Response *)allocator.allocate(sizeof(aimee_msgs__action__ExecuteSkill_GetResult_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__action__ExecuteSkill_GetResult_Response));
  bool success = aimee_msgs__action__ExecuteSkill_GetResult_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__action__ExecuteSkill_GetResult_Response__destroy(aimee_msgs__action__ExecuteSkill_GetResult_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__action__ExecuteSkill_GetResult_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence__init(aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_GetResult_Response * data = NULL;

  if (size) {
    data = (aimee_msgs__action__ExecuteSkill_GetResult_Response *)allocator.zero_allocate(size, sizeof(aimee_msgs__action__ExecuteSkill_GetResult_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__action__ExecuteSkill_GetResult_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__action__ExecuteSkill_GetResult_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence__fini(aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      aimee_msgs__action__ExecuteSkill_GetResult_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence *
aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence * array = (aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence *)allocator.allocate(sizeof(aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence__destroy(aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence__are_equal(const aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence * lhs, const aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__action__ExecuteSkill_GetResult_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence__copy(
  const aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence * input,
  aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__action__ExecuteSkill_GetResult_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__action__ExecuteSkill_GetResult_Response * data =
      (aimee_msgs__action__ExecuteSkill_GetResult_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__action__ExecuteSkill_GetResult_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__action__ExecuteSkill_GetResult_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__action__ExecuteSkill_GetResult_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `feedback`
// already included above
// #include "aimee_msgs/action/detail/execute_skill__functions.h"

bool
aimee_msgs__action__ExecuteSkill_FeedbackMessage__init(aimee_msgs__action__ExecuteSkill_FeedbackMessage * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    aimee_msgs__action__ExecuteSkill_FeedbackMessage__fini(msg);
    return false;
  }
  // feedback
  if (!aimee_msgs__action__ExecuteSkill_Feedback__init(&msg->feedback)) {
    aimee_msgs__action__ExecuteSkill_FeedbackMessage__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__action__ExecuteSkill_FeedbackMessage__fini(aimee_msgs__action__ExecuteSkill_FeedbackMessage * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // feedback
  aimee_msgs__action__ExecuteSkill_Feedback__fini(&msg->feedback);
}

bool
aimee_msgs__action__ExecuteSkill_FeedbackMessage__are_equal(const aimee_msgs__action__ExecuteSkill_FeedbackMessage * lhs, const aimee_msgs__action__ExecuteSkill_FeedbackMessage * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // feedback
  if (!aimee_msgs__action__ExecuteSkill_Feedback__are_equal(
      &(lhs->feedback), &(rhs->feedback)))
  {
    return false;
  }
  return true;
}

bool
aimee_msgs__action__ExecuteSkill_FeedbackMessage__copy(
  const aimee_msgs__action__ExecuteSkill_FeedbackMessage * input,
  aimee_msgs__action__ExecuteSkill_FeedbackMessage * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // feedback
  if (!aimee_msgs__action__ExecuteSkill_Feedback__copy(
      &(input->feedback), &(output->feedback)))
  {
    return false;
  }
  return true;
}

aimee_msgs__action__ExecuteSkill_FeedbackMessage *
aimee_msgs__action__ExecuteSkill_FeedbackMessage__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_FeedbackMessage * msg = (aimee_msgs__action__ExecuteSkill_FeedbackMessage *)allocator.allocate(sizeof(aimee_msgs__action__ExecuteSkill_FeedbackMessage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__action__ExecuteSkill_FeedbackMessage));
  bool success = aimee_msgs__action__ExecuteSkill_FeedbackMessage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__action__ExecuteSkill_FeedbackMessage__destroy(aimee_msgs__action__ExecuteSkill_FeedbackMessage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__action__ExecuteSkill_FeedbackMessage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence__init(aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_FeedbackMessage * data = NULL;

  if (size) {
    data = (aimee_msgs__action__ExecuteSkill_FeedbackMessage *)allocator.zero_allocate(size, sizeof(aimee_msgs__action__ExecuteSkill_FeedbackMessage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__action__ExecuteSkill_FeedbackMessage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__action__ExecuteSkill_FeedbackMessage__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence__fini(aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      aimee_msgs__action__ExecuteSkill_FeedbackMessage__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence *
aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence * array = (aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence *)allocator.allocate(sizeof(aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence__destroy(aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence__are_equal(const aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence * lhs, const aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__action__ExecuteSkill_FeedbackMessage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence__copy(
  const aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence * input,
  aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__action__ExecuteSkill_FeedbackMessage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__action__ExecuteSkill_FeedbackMessage * data =
      (aimee_msgs__action__ExecuteSkill_FeedbackMessage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__action__ExecuteSkill_FeedbackMessage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__action__ExecuteSkill_FeedbackMessage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__action__ExecuteSkill_FeedbackMessage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
