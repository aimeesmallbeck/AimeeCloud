// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aimee_msgs:msg/LEDAction.idl
// generated code does not contain a copyright notice
#include "aimee_msgs/msg/detail/led_action__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `led_id`
// Member `pattern`
#include "rosidl_runtime_c/string_functions.h"
// Member `color`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
aimee_msgs__msg__LEDAction__init(aimee_msgs__msg__LEDAction * msg)
{
  if (!msg) {
    return false;
  }
  // led_id
  if (!rosidl_runtime_c__String__init(&msg->led_id)) {
    aimee_msgs__msg__LEDAction__fini(msg);
    return false;
  }
  // color
  if (!rosidl_runtime_c__uint8__Sequence__init(&msg->color, 0)) {
    aimee_msgs__msg__LEDAction__fini(msg);
    return false;
  }
  // pattern
  if (!rosidl_runtime_c__String__init(&msg->pattern)) {
    aimee_msgs__msg__LEDAction__fini(msg);
    return false;
  }
  // duration_sec
  return true;
}

void
aimee_msgs__msg__LEDAction__fini(aimee_msgs__msg__LEDAction * msg)
{
  if (!msg) {
    return;
  }
  // led_id
  rosidl_runtime_c__String__fini(&msg->led_id);
  // color
  rosidl_runtime_c__uint8__Sequence__fini(&msg->color);
  // pattern
  rosidl_runtime_c__String__fini(&msg->pattern);
  // duration_sec
}

bool
aimee_msgs__msg__LEDAction__are_equal(const aimee_msgs__msg__LEDAction * lhs, const aimee_msgs__msg__LEDAction * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // led_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->led_id), &(rhs->led_id)))
  {
    return false;
  }
  // color
  if (!rosidl_runtime_c__uint8__Sequence__are_equal(
      &(lhs->color), &(rhs->color)))
  {
    return false;
  }
  // pattern
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->pattern), &(rhs->pattern)))
  {
    return false;
  }
  // duration_sec
  if (lhs->duration_sec != rhs->duration_sec) {
    return false;
  }
  return true;
}

bool
aimee_msgs__msg__LEDAction__copy(
  const aimee_msgs__msg__LEDAction * input,
  aimee_msgs__msg__LEDAction * output)
{
  if (!input || !output) {
    return false;
  }
  // led_id
  if (!rosidl_runtime_c__String__copy(
      &(input->led_id), &(output->led_id)))
  {
    return false;
  }
  // color
  if (!rosidl_runtime_c__uint8__Sequence__copy(
      &(input->color), &(output->color)))
  {
    return false;
  }
  // pattern
  if (!rosidl_runtime_c__String__copy(
      &(input->pattern), &(output->pattern)))
  {
    return false;
  }
  // duration_sec
  output->duration_sec = input->duration_sec;
  return true;
}

aimee_msgs__msg__LEDAction *
aimee_msgs__msg__LEDAction__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__LEDAction * msg = (aimee_msgs__msg__LEDAction *)allocator.allocate(sizeof(aimee_msgs__msg__LEDAction), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__msg__LEDAction));
  bool success = aimee_msgs__msg__LEDAction__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__msg__LEDAction__destroy(aimee_msgs__msg__LEDAction * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__msg__LEDAction__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__msg__LEDAction__Sequence__init(aimee_msgs__msg__LEDAction__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__LEDAction * data = NULL;

  if (size) {
    data = (aimee_msgs__msg__LEDAction *)allocator.zero_allocate(size, sizeof(aimee_msgs__msg__LEDAction), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__msg__LEDAction__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__msg__LEDAction__fini(&data[i - 1]);
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
aimee_msgs__msg__LEDAction__Sequence__fini(aimee_msgs__msg__LEDAction__Sequence * array)
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
      aimee_msgs__msg__LEDAction__fini(&array->data[i]);
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

aimee_msgs__msg__LEDAction__Sequence *
aimee_msgs__msg__LEDAction__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__LEDAction__Sequence * array = (aimee_msgs__msg__LEDAction__Sequence *)allocator.allocate(sizeof(aimee_msgs__msg__LEDAction__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__msg__LEDAction__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__msg__LEDAction__Sequence__destroy(aimee_msgs__msg__LEDAction__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__msg__LEDAction__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__msg__LEDAction__Sequence__are_equal(const aimee_msgs__msg__LEDAction__Sequence * lhs, const aimee_msgs__msg__LEDAction__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__msg__LEDAction__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__msg__LEDAction__Sequence__copy(
  const aimee_msgs__msg__LEDAction__Sequence * input,
  aimee_msgs__msg__LEDAction__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__msg__LEDAction);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__msg__LEDAction * data =
      (aimee_msgs__msg__LEDAction *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__msg__LEDAction__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__msg__LEDAction__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__msg__LEDAction__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
