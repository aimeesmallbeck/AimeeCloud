// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aimee_msgs:msg/CameraAction.idl
// generated code does not contain a copyright notice
#include "aimee_msgs/msg/detail/camera_action__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `action_type`
// Member `target`
#include "rosidl_runtime_c/string_functions.h"
// Member `execution_time`
#include "builtin_interfaces/msg/detail/duration__functions.h"

bool
aimee_msgs__msg__CameraAction__init(aimee_msgs__msg__CameraAction * msg)
{
  if (!msg) {
    return false;
  }
  // action_type
  if (!rosidl_runtime_c__String__init(&msg->action_type)) {
    aimee_msgs__msg__CameraAction__fini(msg);
    return false;
  }
  // target
  if (!rosidl_runtime_c__String__init(&msg->target)) {
    aimee_msgs__msg__CameraAction__fini(msg);
    return false;
  }
  // confidence
  // execution_time
  if (!builtin_interfaces__msg__Duration__init(&msg->execution_time)) {
    aimee_msgs__msg__CameraAction__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__msg__CameraAction__fini(aimee_msgs__msg__CameraAction * msg)
{
  if (!msg) {
    return;
  }
  // action_type
  rosidl_runtime_c__String__fini(&msg->action_type);
  // target
  rosidl_runtime_c__String__fini(&msg->target);
  // confidence
  // execution_time
  builtin_interfaces__msg__Duration__fini(&msg->execution_time);
}

bool
aimee_msgs__msg__CameraAction__are_equal(const aimee_msgs__msg__CameraAction * lhs, const aimee_msgs__msg__CameraAction * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // action_type
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->action_type), &(rhs->action_type)))
  {
    return false;
  }
  // target
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->target), &(rhs->target)))
  {
    return false;
  }
  // confidence
  if (lhs->confidence != rhs->confidence) {
    return false;
  }
  // execution_time
  if (!builtin_interfaces__msg__Duration__are_equal(
      &(lhs->execution_time), &(rhs->execution_time)))
  {
    return false;
  }
  return true;
}

bool
aimee_msgs__msg__CameraAction__copy(
  const aimee_msgs__msg__CameraAction * input,
  aimee_msgs__msg__CameraAction * output)
{
  if (!input || !output) {
    return false;
  }
  // action_type
  if (!rosidl_runtime_c__String__copy(
      &(input->action_type), &(output->action_type)))
  {
    return false;
  }
  // target
  if (!rosidl_runtime_c__String__copy(
      &(input->target), &(output->target)))
  {
    return false;
  }
  // confidence
  output->confidence = input->confidence;
  // execution_time
  if (!builtin_interfaces__msg__Duration__copy(
      &(input->execution_time), &(output->execution_time)))
  {
    return false;
  }
  return true;
}

aimee_msgs__msg__CameraAction *
aimee_msgs__msg__CameraAction__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__CameraAction * msg = (aimee_msgs__msg__CameraAction *)allocator.allocate(sizeof(aimee_msgs__msg__CameraAction), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__msg__CameraAction));
  bool success = aimee_msgs__msg__CameraAction__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__msg__CameraAction__destroy(aimee_msgs__msg__CameraAction * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__msg__CameraAction__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__msg__CameraAction__Sequence__init(aimee_msgs__msg__CameraAction__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__CameraAction * data = NULL;

  if (size) {
    data = (aimee_msgs__msg__CameraAction *)allocator.zero_allocate(size, sizeof(aimee_msgs__msg__CameraAction), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__msg__CameraAction__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__msg__CameraAction__fini(&data[i - 1]);
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
aimee_msgs__msg__CameraAction__Sequence__fini(aimee_msgs__msg__CameraAction__Sequence * array)
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
      aimee_msgs__msg__CameraAction__fini(&array->data[i]);
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

aimee_msgs__msg__CameraAction__Sequence *
aimee_msgs__msg__CameraAction__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__CameraAction__Sequence * array = (aimee_msgs__msg__CameraAction__Sequence *)allocator.allocate(sizeof(aimee_msgs__msg__CameraAction__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__msg__CameraAction__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__msg__CameraAction__Sequence__destroy(aimee_msgs__msg__CameraAction__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__msg__CameraAction__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__msg__CameraAction__Sequence__are_equal(const aimee_msgs__msg__CameraAction__Sequence * lhs, const aimee_msgs__msg__CameraAction__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__msg__CameraAction__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__msg__CameraAction__Sequence__copy(
  const aimee_msgs__msg__CameraAction__Sequence * input,
  aimee_msgs__msg__CameraAction__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__msg__CameraAction);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__msg__CameraAction * data =
      (aimee_msgs__msg__CameraAction *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__msg__CameraAction__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__msg__CameraAction__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__msg__CameraAction__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
