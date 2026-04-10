// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aimee_msgs:msg/Transcription.idl
// generated code does not contain a copyright notice
#include "aimee_msgs/msg/detail/transcription__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `text`
// Member `source`
// Member `wake_word`
// Member `session_id`
// Member `correlation_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `timestamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
aimee_msgs__msg__Transcription__init(aimee_msgs__msg__Transcription * msg)
{
  if (!msg) {
    return false;
  }
  // text
  if (!rosidl_runtime_c__String__init(&msg->text)) {
    aimee_msgs__msg__Transcription__fini(msg);
    return false;
  }
  // confidence
  // source
  if (!rosidl_runtime_c__String__init(&msg->source)) {
    aimee_msgs__msg__Transcription__fini(msg);
    return false;
  }
  // is_command
  // is_partial
  // wake_word_detected
  // wake_word
  if (!rosidl_runtime_c__String__init(&msg->wake_word)) {
    aimee_msgs__msg__Transcription__fini(msg);
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__init(&msg->timestamp)) {
    aimee_msgs__msg__Transcription__fini(msg);
    return false;
  }
  // session_id
  if (!rosidl_runtime_c__String__init(&msg->session_id)) {
    aimee_msgs__msg__Transcription__fini(msg);
    return false;
  }
  // correlation_id
  if (!rosidl_runtime_c__String__init(&msg->correlation_id)) {
    aimee_msgs__msg__Transcription__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__msg__Transcription__fini(aimee_msgs__msg__Transcription * msg)
{
  if (!msg) {
    return;
  }
  // text
  rosidl_runtime_c__String__fini(&msg->text);
  // confidence
  // source
  rosidl_runtime_c__String__fini(&msg->source);
  // is_command
  // is_partial
  // wake_word_detected
  // wake_word
  rosidl_runtime_c__String__fini(&msg->wake_word);
  // timestamp
  builtin_interfaces__msg__Time__fini(&msg->timestamp);
  // session_id
  rosidl_runtime_c__String__fini(&msg->session_id);
  // correlation_id
  rosidl_runtime_c__String__fini(&msg->correlation_id);
}

bool
aimee_msgs__msg__Transcription__are_equal(const aimee_msgs__msg__Transcription * lhs, const aimee_msgs__msg__Transcription * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // text
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->text), &(rhs->text)))
  {
    return false;
  }
  // confidence
  if (lhs->confidence != rhs->confidence) {
    return false;
  }
  // source
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->source), &(rhs->source)))
  {
    return false;
  }
  // is_command
  if (lhs->is_command != rhs->is_command) {
    return false;
  }
  // is_partial
  if (lhs->is_partial != rhs->is_partial) {
    return false;
  }
  // wake_word_detected
  if (lhs->wake_word_detected != rhs->wake_word_detected) {
    return false;
  }
  // wake_word
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->wake_word), &(rhs->wake_word)))
  {
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->timestamp), &(rhs->timestamp)))
  {
    return false;
  }
  // session_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->session_id), &(rhs->session_id)))
  {
    return false;
  }
  // correlation_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->correlation_id), &(rhs->correlation_id)))
  {
    return false;
  }
  return true;
}

bool
aimee_msgs__msg__Transcription__copy(
  const aimee_msgs__msg__Transcription * input,
  aimee_msgs__msg__Transcription * output)
{
  if (!input || !output) {
    return false;
  }
  // text
  if (!rosidl_runtime_c__String__copy(
      &(input->text), &(output->text)))
  {
    return false;
  }
  // confidence
  output->confidence = input->confidence;
  // source
  if (!rosidl_runtime_c__String__copy(
      &(input->source), &(output->source)))
  {
    return false;
  }
  // is_command
  output->is_command = input->is_command;
  // is_partial
  output->is_partial = input->is_partial;
  // wake_word_detected
  output->wake_word_detected = input->wake_word_detected;
  // wake_word
  if (!rosidl_runtime_c__String__copy(
      &(input->wake_word), &(output->wake_word)))
  {
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->timestamp), &(output->timestamp)))
  {
    return false;
  }
  // session_id
  if (!rosidl_runtime_c__String__copy(
      &(input->session_id), &(output->session_id)))
  {
    return false;
  }
  // correlation_id
  if (!rosidl_runtime_c__String__copy(
      &(input->correlation_id), &(output->correlation_id)))
  {
    return false;
  }
  return true;
}

aimee_msgs__msg__Transcription *
aimee_msgs__msg__Transcription__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__Transcription * msg = (aimee_msgs__msg__Transcription *)allocator.allocate(sizeof(aimee_msgs__msg__Transcription), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__msg__Transcription));
  bool success = aimee_msgs__msg__Transcription__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__msg__Transcription__destroy(aimee_msgs__msg__Transcription * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__msg__Transcription__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__msg__Transcription__Sequence__init(aimee_msgs__msg__Transcription__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__Transcription * data = NULL;

  if (size) {
    data = (aimee_msgs__msg__Transcription *)allocator.zero_allocate(size, sizeof(aimee_msgs__msg__Transcription), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__msg__Transcription__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__msg__Transcription__fini(&data[i - 1]);
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
aimee_msgs__msg__Transcription__Sequence__fini(aimee_msgs__msg__Transcription__Sequence * array)
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
      aimee_msgs__msg__Transcription__fini(&array->data[i]);
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

aimee_msgs__msg__Transcription__Sequence *
aimee_msgs__msg__Transcription__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__Transcription__Sequence * array = (aimee_msgs__msg__Transcription__Sequence *)allocator.allocate(sizeof(aimee_msgs__msg__Transcription__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__msg__Transcription__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__msg__Transcription__Sequence__destroy(aimee_msgs__msg__Transcription__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__msg__Transcription__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__msg__Transcription__Sequence__are_equal(const aimee_msgs__msg__Transcription__Sequence * lhs, const aimee_msgs__msg__Transcription__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__msg__Transcription__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__msg__Transcription__Sequence__copy(
  const aimee_msgs__msg__Transcription__Sequence * input,
  aimee_msgs__msg__Transcription__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__msg__Transcription);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__msg__Transcription * data =
      (aimee_msgs__msg__Transcription *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__msg__Transcription__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__msg__Transcription__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__msg__Transcription__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
