// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aimee_msgs:msg/Intent.idl
// generated code does not contain a copyright notice
#include "aimee_msgs/msg/detail/intent__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `intent_type`
// Member `action`
// Member `raw_text`
// Member `skill_name`
// Member `parameters_json`
// Member `session_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `timestamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
aimee_msgs__msg__Intent__init(aimee_msgs__msg__Intent * msg)
{
  if (!msg) {
    return false;
  }
  // intent_type
  if (!rosidl_runtime_c__String__init(&msg->intent_type)) {
    aimee_msgs__msg__Intent__fini(msg);
    return false;
  }
  // action
  if (!rosidl_runtime_c__String__init(&msg->action)) {
    aimee_msgs__msg__Intent__fini(msg);
    return false;
  }
  // confidence
  // raw_text
  if (!rosidl_runtime_c__String__init(&msg->raw_text)) {
    aimee_msgs__msg__Intent__fini(msg);
    return false;
  }
  // requires_skill
  // skill_name
  if (!rosidl_runtime_c__String__init(&msg->skill_name)) {
    aimee_msgs__msg__Intent__fini(msg);
    return false;
  }
  // parameters_json
  if (!rosidl_runtime_c__String__init(&msg->parameters_json)) {
    aimee_msgs__msg__Intent__fini(msg);
    return false;
  }
  // session_id
  if (!rosidl_runtime_c__String__init(&msg->session_id)) {
    aimee_msgs__msg__Intent__fini(msg);
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__init(&msg->timestamp)) {
    aimee_msgs__msg__Intent__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__msg__Intent__fini(aimee_msgs__msg__Intent * msg)
{
  if (!msg) {
    return;
  }
  // intent_type
  rosidl_runtime_c__String__fini(&msg->intent_type);
  // action
  rosidl_runtime_c__String__fini(&msg->action);
  // confidence
  // raw_text
  rosidl_runtime_c__String__fini(&msg->raw_text);
  // requires_skill
  // skill_name
  rosidl_runtime_c__String__fini(&msg->skill_name);
  // parameters_json
  rosidl_runtime_c__String__fini(&msg->parameters_json);
  // session_id
  rosidl_runtime_c__String__fini(&msg->session_id);
  // timestamp
  builtin_interfaces__msg__Time__fini(&msg->timestamp);
}

bool
aimee_msgs__msg__Intent__are_equal(const aimee_msgs__msg__Intent * lhs, const aimee_msgs__msg__Intent * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // intent_type
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->intent_type), &(rhs->intent_type)))
  {
    return false;
  }
  // action
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->action), &(rhs->action)))
  {
    return false;
  }
  // confidence
  if (lhs->confidence != rhs->confidence) {
    return false;
  }
  // raw_text
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->raw_text), &(rhs->raw_text)))
  {
    return false;
  }
  // requires_skill
  if (lhs->requires_skill != rhs->requires_skill) {
    return false;
  }
  // skill_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->skill_name), &(rhs->skill_name)))
  {
    return false;
  }
  // parameters_json
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->parameters_json), &(rhs->parameters_json)))
  {
    return false;
  }
  // session_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->session_id), &(rhs->session_id)))
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
aimee_msgs__msg__Intent__copy(
  const aimee_msgs__msg__Intent * input,
  aimee_msgs__msg__Intent * output)
{
  if (!input || !output) {
    return false;
  }
  // intent_type
  if (!rosidl_runtime_c__String__copy(
      &(input->intent_type), &(output->intent_type)))
  {
    return false;
  }
  // action
  if (!rosidl_runtime_c__String__copy(
      &(input->action), &(output->action)))
  {
    return false;
  }
  // confidence
  output->confidence = input->confidence;
  // raw_text
  if (!rosidl_runtime_c__String__copy(
      &(input->raw_text), &(output->raw_text)))
  {
    return false;
  }
  // requires_skill
  output->requires_skill = input->requires_skill;
  // skill_name
  if (!rosidl_runtime_c__String__copy(
      &(input->skill_name), &(output->skill_name)))
  {
    return false;
  }
  // parameters_json
  if (!rosidl_runtime_c__String__copy(
      &(input->parameters_json), &(output->parameters_json)))
  {
    return false;
  }
  // session_id
  if (!rosidl_runtime_c__String__copy(
      &(input->session_id), &(output->session_id)))
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

aimee_msgs__msg__Intent *
aimee_msgs__msg__Intent__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__Intent * msg = (aimee_msgs__msg__Intent *)allocator.allocate(sizeof(aimee_msgs__msg__Intent), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__msg__Intent));
  bool success = aimee_msgs__msg__Intent__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__msg__Intent__destroy(aimee_msgs__msg__Intent * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__msg__Intent__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__msg__Intent__Sequence__init(aimee_msgs__msg__Intent__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__Intent * data = NULL;

  if (size) {
    data = (aimee_msgs__msg__Intent *)allocator.zero_allocate(size, sizeof(aimee_msgs__msg__Intent), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__msg__Intent__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__msg__Intent__fini(&data[i - 1]);
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
aimee_msgs__msg__Intent__Sequence__fini(aimee_msgs__msg__Intent__Sequence * array)
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
      aimee_msgs__msg__Intent__fini(&array->data[i]);
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

aimee_msgs__msg__Intent__Sequence *
aimee_msgs__msg__Intent__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__Intent__Sequence * array = (aimee_msgs__msg__Intent__Sequence *)allocator.allocate(sizeof(aimee_msgs__msg__Intent__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__msg__Intent__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__msg__Intent__Sequence__destroy(aimee_msgs__msg__Intent__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__msg__Intent__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__msg__Intent__Sequence__are_equal(const aimee_msgs__msg__Intent__Sequence * lhs, const aimee_msgs__msg__Intent__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__msg__Intent__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__msg__Intent__Sequence__copy(
  const aimee_msgs__msg__Intent__Sequence * input,
  aimee_msgs__msg__Intent__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__msg__Intent);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__msg__Intent * data =
      (aimee_msgs__msg__Intent *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__msg__Intent__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__msg__Intent__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__msg__Intent__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
