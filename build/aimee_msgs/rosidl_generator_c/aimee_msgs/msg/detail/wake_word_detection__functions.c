// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aimee_msgs:msg/WakeWordDetection.idl
// generated code does not contain a copyright notice
#include "aimee_msgs/msg/detail/wake_word_detection__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `wake_word`
// Member `source`
// Member `session_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `timestamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
aimee_msgs__msg__WakeWordDetection__init(aimee_msgs__msg__WakeWordDetection * msg)
{
  if (!msg) {
    return false;
  }
  // wake_word
  if (!rosidl_runtime_c__String__init(&msg->wake_word)) {
    aimee_msgs__msg__WakeWordDetection__fini(msg);
    return false;
  }
  // confidence
  // source
  if (!rosidl_runtime_c__String__init(&msg->source)) {
    aimee_msgs__msg__WakeWordDetection__fini(msg);
    return false;
  }
  // sample_index
  // signal_energy
  // active
  // timestamp
  if (!builtin_interfaces__msg__Time__init(&msg->timestamp)) {
    aimee_msgs__msg__WakeWordDetection__fini(msg);
    return false;
  }
  // session_id
  if (!rosidl_runtime_c__String__init(&msg->session_id)) {
    aimee_msgs__msg__WakeWordDetection__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__msg__WakeWordDetection__fini(aimee_msgs__msg__WakeWordDetection * msg)
{
  if (!msg) {
    return;
  }
  // wake_word
  rosidl_runtime_c__String__fini(&msg->wake_word);
  // confidence
  // source
  rosidl_runtime_c__String__fini(&msg->source);
  // sample_index
  // signal_energy
  // active
  // timestamp
  builtin_interfaces__msg__Time__fini(&msg->timestamp);
  // session_id
  rosidl_runtime_c__String__fini(&msg->session_id);
}

bool
aimee_msgs__msg__WakeWordDetection__are_equal(const aimee_msgs__msg__WakeWordDetection * lhs, const aimee_msgs__msg__WakeWordDetection * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // wake_word
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->wake_word), &(rhs->wake_word)))
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
  // sample_index
  if (lhs->sample_index != rhs->sample_index) {
    return false;
  }
  // signal_energy
  if (lhs->signal_energy != rhs->signal_energy) {
    return false;
  }
  // active
  if (lhs->active != rhs->active) {
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
  return true;
}

bool
aimee_msgs__msg__WakeWordDetection__copy(
  const aimee_msgs__msg__WakeWordDetection * input,
  aimee_msgs__msg__WakeWordDetection * output)
{
  if (!input || !output) {
    return false;
  }
  // wake_word
  if (!rosidl_runtime_c__String__copy(
      &(input->wake_word), &(output->wake_word)))
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
  // sample_index
  output->sample_index = input->sample_index;
  // signal_energy
  output->signal_energy = input->signal_energy;
  // active
  output->active = input->active;
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
  return true;
}

aimee_msgs__msg__WakeWordDetection *
aimee_msgs__msg__WakeWordDetection__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__WakeWordDetection * msg = (aimee_msgs__msg__WakeWordDetection *)allocator.allocate(sizeof(aimee_msgs__msg__WakeWordDetection), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__msg__WakeWordDetection));
  bool success = aimee_msgs__msg__WakeWordDetection__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__msg__WakeWordDetection__destroy(aimee_msgs__msg__WakeWordDetection * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__msg__WakeWordDetection__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__msg__WakeWordDetection__Sequence__init(aimee_msgs__msg__WakeWordDetection__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__WakeWordDetection * data = NULL;

  if (size) {
    data = (aimee_msgs__msg__WakeWordDetection *)allocator.zero_allocate(size, sizeof(aimee_msgs__msg__WakeWordDetection), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__msg__WakeWordDetection__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__msg__WakeWordDetection__fini(&data[i - 1]);
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
aimee_msgs__msg__WakeWordDetection__Sequence__fini(aimee_msgs__msg__WakeWordDetection__Sequence * array)
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
      aimee_msgs__msg__WakeWordDetection__fini(&array->data[i]);
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

aimee_msgs__msg__WakeWordDetection__Sequence *
aimee_msgs__msg__WakeWordDetection__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__WakeWordDetection__Sequence * array = (aimee_msgs__msg__WakeWordDetection__Sequence *)allocator.allocate(sizeof(aimee_msgs__msg__WakeWordDetection__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__msg__WakeWordDetection__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__msg__WakeWordDetection__Sequence__destroy(aimee_msgs__msg__WakeWordDetection__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__msg__WakeWordDetection__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__msg__WakeWordDetection__Sequence__are_equal(const aimee_msgs__msg__WakeWordDetection__Sequence * lhs, const aimee_msgs__msg__WakeWordDetection__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__msg__WakeWordDetection__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__msg__WakeWordDetection__Sequence__copy(
  const aimee_msgs__msg__WakeWordDetection__Sequence * input,
  aimee_msgs__msg__WakeWordDetection__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__msg__WakeWordDetection);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__msg__WakeWordDetection * data =
      (aimee_msgs__msg__WakeWordDetection *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__msg__WakeWordDetection__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__msg__WakeWordDetection__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__msg__WakeWordDetection__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
