// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aimee_msgs:msg/TrackingCommand.idl
// generated code does not contain a copyright notice
#include "aimee_msgs/msg/detail/tracking_command__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `command`
// Member `mode`
// Member `target_type`
// Member `target_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `target_position`
#include "geometry_msgs/msg/detail/point__functions.h"
// Member `timestamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
aimee_msgs__msg__TrackingCommand__init(aimee_msgs__msg__TrackingCommand * msg)
{
  if (!msg) {
    return false;
  }
  // command
  if (!rosidl_runtime_c__String__init(&msg->command)) {
    aimee_msgs__msg__TrackingCommand__fini(msg);
    return false;
  }
  // mode
  if (!rosidl_runtime_c__String__init(&msg->mode)) {
    aimee_msgs__msg__TrackingCommand__fini(msg);
    return false;
  }
  // preset_id
  // zoom_level
  // target_type
  if (!rosidl_runtime_c__String__init(&msg->target_type)) {
    aimee_msgs__msg__TrackingCommand__fini(msg);
    return false;
  }
  // target_id
  if (!rosidl_runtime_c__String__init(&msg->target_id)) {
    aimee_msgs__msg__TrackingCommand__fini(msg);
    return false;
  }
  // target_position
  if (!geometry_msgs__msg__Point__init(&msg->target_position)) {
    aimee_msgs__msg__TrackingCommand__fini(msg);
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__init(&msg->timestamp)) {
    aimee_msgs__msg__TrackingCommand__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__msg__TrackingCommand__fini(aimee_msgs__msg__TrackingCommand * msg)
{
  if (!msg) {
    return;
  }
  // command
  rosidl_runtime_c__String__fini(&msg->command);
  // mode
  rosidl_runtime_c__String__fini(&msg->mode);
  // preset_id
  // zoom_level
  // target_type
  rosidl_runtime_c__String__fini(&msg->target_type);
  // target_id
  rosidl_runtime_c__String__fini(&msg->target_id);
  // target_position
  geometry_msgs__msg__Point__fini(&msg->target_position);
  // timestamp
  builtin_interfaces__msg__Time__fini(&msg->timestamp);
}

bool
aimee_msgs__msg__TrackingCommand__are_equal(const aimee_msgs__msg__TrackingCommand * lhs, const aimee_msgs__msg__TrackingCommand * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // command
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->command), &(rhs->command)))
  {
    return false;
  }
  // mode
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->mode), &(rhs->mode)))
  {
    return false;
  }
  // preset_id
  if (lhs->preset_id != rhs->preset_id) {
    return false;
  }
  // zoom_level
  if (lhs->zoom_level != rhs->zoom_level) {
    return false;
  }
  // target_type
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->target_type), &(rhs->target_type)))
  {
    return false;
  }
  // target_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->target_id), &(rhs->target_id)))
  {
    return false;
  }
  // target_position
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->target_position), &(rhs->target_position)))
  {
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->timestamp), &(rhs->timestamp)))
  {
    return false;
  }
  return true;
}

bool
aimee_msgs__msg__TrackingCommand__copy(
  const aimee_msgs__msg__TrackingCommand * input,
  aimee_msgs__msg__TrackingCommand * output)
{
  if (!input || !output) {
    return false;
  }
  // command
  if (!rosidl_runtime_c__String__copy(
      &(input->command), &(output->command)))
  {
    return false;
  }
  // mode
  if (!rosidl_runtime_c__String__copy(
      &(input->mode), &(output->mode)))
  {
    return false;
  }
  // preset_id
  output->preset_id = input->preset_id;
  // zoom_level
  output->zoom_level = input->zoom_level;
  // target_type
  if (!rosidl_runtime_c__String__copy(
      &(input->target_type), &(output->target_type)))
  {
    return false;
  }
  // target_id
  if (!rosidl_runtime_c__String__copy(
      &(input->target_id), &(output->target_id)))
  {
    return false;
  }
  // target_position
  if (!geometry_msgs__msg__Point__copy(
      &(input->target_position), &(output->target_position)))
  {
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->timestamp), &(output->timestamp)))
  {
    return false;
  }
  return true;
}

aimee_msgs__msg__TrackingCommand *
aimee_msgs__msg__TrackingCommand__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__TrackingCommand * msg = (aimee_msgs__msg__TrackingCommand *)allocator.allocate(sizeof(aimee_msgs__msg__TrackingCommand), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__msg__TrackingCommand));
  bool success = aimee_msgs__msg__TrackingCommand__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__msg__TrackingCommand__destroy(aimee_msgs__msg__TrackingCommand * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__msg__TrackingCommand__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__msg__TrackingCommand__Sequence__init(aimee_msgs__msg__TrackingCommand__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__TrackingCommand * data = NULL;

  if (size) {
    data = (aimee_msgs__msg__TrackingCommand *)allocator.zero_allocate(size, sizeof(aimee_msgs__msg__TrackingCommand), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__msg__TrackingCommand__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__msg__TrackingCommand__fini(&data[i - 1]);
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
aimee_msgs__msg__TrackingCommand__Sequence__fini(aimee_msgs__msg__TrackingCommand__Sequence * array)
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
      aimee_msgs__msg__TrackingCommand__fini(&array->data[i]);
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

aimee_msgs__msg__TrackingCommand__Sequence *
aimee_msgs__msg__TrackingCommand__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__TrackingCommand__Sequence * array = (aimee_msgs__msg__TrackingCommand__Sequence *)allocator.allocate(sizeof(aimee_msgs__msg__TrackingCommand__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__msg__TrackingCommand__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__msg__TrackingCommand__Sequence__destroy(aimee_msgs__msg__TrackingCommand__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__msg__TrackingCommand__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__msg__TrackingCommand__Sequence__are_equal(const aimee_msgs__msg__TrackingCommand__Sequence * lhs, const aimee_msgs__msg__TrackingCommand__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__msg__TrackingCommand__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__msg__TrackingCommand__Sequence__copy(
  const aimee_msgs__msg__TrackingCommand__Sequence * input,
  aimee_msgs__msg__TrackingCommand__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__msg__TrackingCommand);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__msg__TrackingCommand * data =
      (aimee_msgs__msg__TrackingCommand *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__msg__TrackingCommand__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__msg__TrackingCommand__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__msg__TrackingCommand__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
