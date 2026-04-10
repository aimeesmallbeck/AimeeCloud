// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aimee_msgs:action/LLMGenerate.idl
// generated code does not contain a copyright notice
#include "aimee_msgs/action/detail/llm_generate__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `prompt`
// Member `system_context`
// Member `session_id`
#include "rosidl_runtime_c/string_functions.h"

bool
aimee_msgs__action__LLMGenerate_Goal__init(aimee_msgs__action__LLMGenerate_Goal * msg)
{
  if (!msg) {
    return false;
  }
  // prompt
  if (!rosidl_runtime_c__String__init(&msg->prompt)) {
    aimee_msgs__action__LLMGenerate_Goal__fini(msg);
    return false;
  }
  // system_context
  if (!rosidl_runtime_c__String__init(&msg->system_context)) {
    aimee_msgs__action__LLMGenerate_Goal__fini(msg);
    return false;
  }
  // max_tokens
  // temperature
  // stream
  // session_id
  if (!rosidl_runtime_c__String__init(&msg->session_id)) {
    aimee_msgs__action__LLMGenerate_Goal__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__action__LLMGenerate_Goal__fini(aimee_msgs__action__LLMGenerate_Goal * msg)
{
  if (!msg) {
    return;
  }
  // prompt
  rosidl_runtime_c__String__fini(&msg->prompt);
  // system_context
  rosidl_runtime_c__String__fini(&msg->system_context);
  // max_tokens
  // temperature
  // stream
  // session_id
  rosidl_runtime_c__String__fini(&msg->session_id);
}

bool
aimee_msgs__action__LLMGenerate_Goal__are_equal(const aimee_msgs__action__LLMGenerate_Goal * lhs, const aimee_msgs__action__LLMGenerate_Goal * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // prompt
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->prompt), &(rhs->prompt)))
  {
    return false;
  }
  // system_context
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->system_context), &(rhs->system_context)))
  {
    return false;
  }
  // max_tokens
  if (lhs->max_tokens != rhs->max_tokens) {
    return false;
  }
  // temperature
  if (lhs->temperature != rhs->temperature) {
    return false;
  }
  // stream
  if (lhs->stream != rhs->stream) {
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
aimee_msgs__action__LLMGenerate_Goal__copy(
  const aimee_msgs__action__LLMGenerate_Goal * input,
  aimee_msgs__action__LLMGenerate_Goal * output)
{
  if (!input || !output) {
    return false;
  }
  // prompt
  if (!rosidl_runtime_c__String__copy(
      &(input->prompt), &(output->prompt)))
  {
    return false;
  }
  // system_context
  if (!rosidl_runtime_c__String__copy(
      &(input->system_context), &(output->system_context)))
  {
    return false;
  }
  // max_tokens
  output->max_tokens = input->max_tokens;
  // temperature
  output->temperature = input->temperature;
  // stream
  output->stream = input->stream;
  // session_id
  if (!rosidl_runtime_c__String__copy(
      &(input->session_id), &(output->session_id)))
  {
    return false;
  }
  return true;
}

aimee_msgs__action__LLMGenerate_Goal *
aimee_msgs__action__LLMGenerate_Goal__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_Goal * msg = (aimee_msgs__action__LLMGenerate_Goal *)allocator.allocate(sizeof(aimee_msgs__action__LLMGenerate_Goal), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__action__LLMGenerate_Goal));
  bool success = aimee_msgs__action__LLMGenerate_Goal__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__action__LLMGenerate_Goal__destroy(aimee_msgs__action__LLMGenerate_Goal * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__action__LLMGenerate_Goal__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__action__LLMGenerate_Goal__Sequence__init(aimee_msgs__action__LLMGenerate_Goal__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_Goal * data = NULL;

  if (size) {
    data = (aimee_msgs__action__LLMGenerate_Goal *)allocator.zero_allocate(size, sizeof(aimee_msgs__action__LLMGenerate_Goal), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__action__LLMGenerate_Goal__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__action__LLMGenerate_Goal__fini(&data[i - 1]);
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
aimee_msgs__action__LLMGenerate_Goal__Sequence__fini(aimee_msgs__action__LLMGenerate_Goal__Sequence * array)
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
      aimee_msgs__action__LLMGenerate_Goal__fini(&array->data[i]);
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

aimee_msgs__action__LLMGenerate_Goal__Sequence *
aimee_msgs__action__LLMGenerate_Goal__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_Goal__Sequence * array = (aimee_msgs__action__LLMGenerate_Goal__Sequence *)allocator.allocate(sizeof(aimee_msgs__action__LLMGenerate_Goal__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__action__LLMGenerate_Goal__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__action__LLMGenerate_Goal__Sequence__destroy(aimee_msgs__action__LLMGenerate_Goal__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__action__LLMGenerate_Goal__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__action__LLMGenerate_Goal__Sequence__are_equal(const aimee_msgs__action__LLMGenerate_Goal__Sequence * lhs, const aimee_msgs__action__LLMGenerate_Goal__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__action__LLMGenerate_Goal__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__action__LLMGenerate_Goal__Sequence__copy(
  const aimee_msgs__action__LLMGenerate_Goal__Sequence * input,
  aimee_msgs__action__LLMGenerate_Goal__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__action__LLMGenerate_Goal);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__action__LLMGenerate_Goal * data =
      (aimee_msgs__action__LLMGenerate_Goal *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__action__LLMGenerate_Goal__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__action__LLMGenerate_Goal__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__action__LLMGenerate_Goal__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `response`
// Member `error_message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
aimee_msgs__action__LLMGenerate_Result__init(aimee_msgs__action__LLMGenerate_Result * msg)
{
  if (!msg) {
    return false;
  }
  // response
  if (!rosidl_runtime_c__String__init(&msg->response)) {
    aimee_msgs__action__LLMGenerate_Result__fini(msg);
    return false;
  }
  // success
  // error_message
  if (!rosidl_runtime_c__String__init(&msg->error_message)) {
    aimee_msgs__action__LLMGenerate_Result__fini(msg);
    return false;
  }
  // generation_time
  // tokens_generated
  // tokens_input
  return true;
}

void
aimee_msgs__action__LLMGenerate_Result__fini(aimee_msgs__action__LLMGenerate_Result * msg)
{
  if (!msg) {
    return;
  }
  // response
  rosidl_runtime_c__String__fini(&msg->response);
  // success
  // error_message
  rosidl_runtime_c__String__fini(&msg->error_message);
  // generation_time
  // tokens_generated
  // tokens_input
}

bool
aimee_msgs__action__LLMGenerate_Result__are_equal(const aimee_msgs__action__LLMGenerate_Result * lhs, const aimee_msgs__action__LLMGenerate_Result * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // response
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // error_message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->error_message), &(rhs->error_message)))
  {
    return false;
  }
  // generation_time
  if (lhs->generation_time != rhs->generation_time) {
    return false;
  }
  // tokens_generated
  if (lhs->tokens_generated != rhs->tokens_generated) {
    return false;
  }
  // tokens_input
  if (lhs->tokens_input != rhs->tokens_input) {
    return false;
  }
  return true;
}

bool
aimee_msgs__action__LLMGenerate_Result__copy(
  const aimee_msgs__action__LLMGenerate_Result * input,
  aimee_msgs__action__LLMGenerate_Result * output)
{
  if (!input || !output) {
    return false;
  }
  // response
  if (!rosidl_runtime_c__String__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  // success
  output->success = input->success;
  // error_message
  if (!rosidl_runtime_c__String__copy(
      &(input->error_message), &(output->error_message)))
  {
    return false;
  }
  // generation_time
  output->generation_time = input->generation_time;
  // tokens_generated
  output->tokens_generated = input->tokens_generated;
  // tokens_input
  output->tokens_input = input->tokens_input;
  return true;
}

aimee_msgs__action__LLMGenerate_Result *
aimee_msgs__action__LLMGenerate_Result__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_Result * msg = (aimee_msgs__action__LLMGenerate_Result *)allocator.allocate(sizeof(aimee_msgs__action__LLMGenerate_Result), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__action__LLMGenerate_Result));
  bool success = aimee_msgs__action__LLMGenerate_Result__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__action__LLMGenerate_Result__destroy(aimee_msgs__action__LLMGenerate_Result * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__action__LLMGenerate_Result__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__action__LLMGenerate_Result__Sequence__init(aimee_msgs__action__LLMGenerate_Result__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_Result * data = NULL;

  if (size) {
    data = (aimee_msgs__action__LLMGenerate_Result *)allocator.zero_allocate(size, sizeof(aimee_msgs__action__LLMGenerate_Result), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__action__LLMGenerate_Result__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__action__LLMGenerate_Result__fini(&data[i - 1]);
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
aimee_msgs__action__LLMGenerate_Result__Sequence__fini(aimee_msgs__action__LLMGenerate_Result__Sequence * array)
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
      aimee_msgs__action__LLMGenerate_Result__fini(&array->data[i]);
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

aimee_msgs__action__LLMGenerate_Result__Sequence *
aimee_msgs__action__LLMGenerate_Result__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_Result__Sequence * array = (aimee_msgs__action__LLMGenerate_Result__Sequence *)allocator.allocate(sizeof(aimee_msgs__action__LLMGenerate_Result__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__action__LLMGenerate_Result__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__action__LLMGenerate_Result__Sequence__destroy(aimee_msgs__action__LLMGenerate_Result__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__action__LLMGenerate_Result__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__action__LLMGenerate_Result__Sequence__are_equal(const aimee_msgs__action__LLMGenerate_Result__Sequence * lhs, const aimee_msgs__action__LLMGenerate_Result__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__action__LLMGenerate_Result__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__action__LLMGenerate_Result__Sequence__copy(
  const aimee_msgs__action__LLMGenerate_Result__Sequence * input,
  aimee_msgs__action__LLMGenerate_Result__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__action__LLMGenerate_Result);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__action__LLMGenerate_Result * data =
      (aimee_msgs__action__LLMGenerate_Result *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__action__LLMGenerate_Result__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__action__LLMGenerate_Result__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__action__LLMGenerate_Result__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `partial_response`
// Member `current_word`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
aimee_msgs__action__LLMGenerate_Feedback__init(aimee_msgs__action__LLMGenerate_Feedback * msg)
{
  if (!msg) {
    return false;
  }
  // partial_response
  if (!rosidl_runtime_c__String__init(&msg->partial_response)) {
    aimee_msgs__action__LLMGenerate_Feedback__fini(msg);
    return false;
  }
  // tokens_generated
  // tokens_total
  // is_complete
  // current_word
  if (!rosidl_runtime_c__String__init(&msg->current_word)) {
    aimee_msgs__action__LLMGenerate_Feedback__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__action__LLMGenerate_Feedback__fini(aimee_msgs__action__LLMGenerate_Feedback * msg)
{
  if (!msg) {
    return;
  }
  // partial_response
  rosidl_runtime_c__String__fini(&msg->partial_response);
  // tokens_generated
  // tokens_total
  // is_complete
  // current_word
  rosidl_runtime_c__String__fini(&msg->current_word);
}

bool
aimee_msgs__action__LLMGenerate_Feedback__are_equal(const aimee_msgs__action__LLMGenerate_Feedback * lhs, const aimee_msgs__action__LLMGenerate_Feedback * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // partial_response
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->partial_response), &(rhs->partial_response)))
  {
    return false;
  }
  // tokens_generated
  if (lhs->tokens_generated != rhs->tokens_generated) {
    return false;
  }
  // tokens_total
  if (lhs->tokens_total != rhs->tokens_total) {
    return false;
  }
  // is_complete
  if (lhs->is_complete != rhs->is_complete) {
    return false;
  }
  // current_word
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->current_word), &(rhs->current_word)))
  {
    return false;
  }
  return true;
}

bool
aimee_msgs__action__LLMGenerate_Feedback__copy(
  const aimee_msgs__action__LLMGenerate_Feedback * input,
  aimee_msgs__action__LLMGenerate_Feedback * output)
{
  if (!input || !output) {
    return false;
  }
  // partial_response
  if (!rosidl_runtime_c__String__copy(
      &(input->partial_response), &(output->partial_response)))
  {
    return false;
  }
  // tokens_generated
  output->tokens_generated = input->tokens_generated;
  // tokens_total
  output->tokens_total = input->tokens_total;
  // is_complete
  output->is_complete = input->is_complete;
  // current_word
  if (!rosidl_runtime_c__String__copy(
      &(input->current_word), &(output->current_word)))
  {
    return false;
  }
  return true;
}

aimee_msgs__action__LLMGenerate_Feedback *
aimee_msgs__action__LLMGenerate_Feedback__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_Feedback * msg = (aimee_msgs__action__LLMGenerate_Feedback *)allocator.allocate(sizeof(aimee_msgs__action__LLMGenerate_Feedback), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__action__LLMGenerate_Feedback));
  bool success = aimee_msgs__action__LLMGenerate_Feedback__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__action__LLMGenerate_Feedback__destroy(aimee_msgs__action__LLMGenerate_Feedback * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__action__LLMGenerate_Feedback__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__action__LLMGenerate_Feedback__Sequence__init(aimee_msgs__action__LLMGenerate_Feedback__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_Feedback * data = NULL;

  if (size) {
    data = (aimee_msgs__action__LLMGenerate_Feedback *)allocator.zero_allocate(size, sizeof(aimee_msgs__action__LLMGenerate_Feedback), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__action__LLMGenerate_Feedback__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__action__LLMGenerate_Feedback__fini(&data[i - 1]);
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
aimee_msgs__action__LLMGenerate_Feedback__Sequence__fini(aimee_msgs__action__LLMGenerate_Feedback__Sequence * array)
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
      aimee_msgs__action__LLMGenerate_Feedback__fini(&array->data[i]);
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

aimee_msgs__action__LLMGenerate_Feedback__Sequence *
aimee_msgs__action__LLMGenerate_Feedback__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_Feedback__Sequence * array = (aimee_msgs__action__LLMGenerate_Feedback__Sequence *)allocator.allocate(sizeof(aimee_msgs__action__LLMGenerate_Feedback__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__action__LLMGenerate_Feedback__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__action__LLMGenerate_Feedback__Sequence__destroy(aimee_msgs__action__LLMGenerate_Feedback__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__action__LLMGenerate_Feedback__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__action__LLMGenerate_Feedback__Sequence__are_equal(const aimee_msgs__action__LLMGenerate_Feedback__Sequence * lhs, const aimee_msgs__action__LLMGenerate_Feedback__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__action__LLMGenerate_Feedback__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__action__LLMGenerate_Feedback__Sequence__copy(
  const aimee_msgs__action__LLMGenerate_Feedback__Sequence * input,
  aimee_msgs__action__LLMGenerate_Feedback__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__action__LLMGenerate_Feedback);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__action__LLMGenerate_Feedback * data =
      (aimee_msgs__action__LLMGenerate_Feedback *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__action__LLMGenerate_Feedback__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__action__LLMGenerate_Feedback__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__action__LLMGenerate_Feedback__copy(
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
// #include "aimee_msgs/action/detail/llm_generate__functions.h"

bool
aimee_msgs__action__LLMGenerate_SendGoal_Request__init(aimee_msgs__action__LLMGenerate_SendGoal_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    aimee_msgs__action__LLMGenerate_SendGoal_Request__fini(msg);
    return false;
  }
  // goal
  if (!aimee_msgs__action__LLMGenerate_Goal__init(&msg->goal)) {
    aimee_msgs__action__LLMGenerate_SendGoal_Request__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__action__LLMGenerate_SendGoal_Request__fini(aimee_msgs__action__LLMGenerate_SendGoal_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // goal
  aimee_msgs__action__LLMGenerate_Goal__fini(&msg->goal);
}

bool
aimee_msgs__action__LLMGenerate_SendGoal_Request__are_equal(const aimee_msgs__action__LLMGenerate_SendGoal_Request * lhs, const aimee_msgs__action__LLMGenerate_SendGoal_Request * rhs)
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
  if (!aimee_msgs__action__LLMGenerate_Goal__are_equal(
      &(lhs->goal), &(rhs->goal)))
  {
    return false;
  }
  return true;
}

bool
aimee_msgs__action__LLMGenerate_SendGoal_Request__copy(
  const aimee_msgs__action__LLMGenerate_SendGoal_Request * input,
  aimee_msgs__action__LLMGenerate_SendGoal_Request * output)
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
  if (!aimee_msgs__action__LLMGenerate_Goal__copy(
      &(input->goal), &(output->goal)))
  {
    return false;
  }
  return true;
}

aimee_msgs__action__LLMGenerate_SendGoal_Request *
aimee_msgs__action__LLMGenerate_SendGoal_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_SendGoal_Request * msg = (aimee_msgs__action__LLMGenerate_SendGoal_Request *)allocator.allocate(sizeof(aimee_msgs__action__LLMGenerate_SendGoal_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__action__LLMGenerate_SendGoal_Request));
  bool success = aimee_msgs__action__LLMGenerate_SendGoal_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__action__LLMGenerate_SendGoal_Request__destroy(aimee_msgs__action__LLMGenerate_SendGoal_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__action__LLMGenerate_SendGoal_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence__init(aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_SendGoal_Request * data = NULL;

  if (size) {
    data = (aimee_msgs__action__LLMGenerate_SendGoal_Request *)allocator.zero_allocate(size, sizeof(aimee_msgs__action__LLMGenerate_SendGoal_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__action__LLMGenerate_SendGoal_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__action__LLMGenerate_SendGoal_Request__fini(&data[i - 1]);
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
aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence__fini(aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence * array)
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
      aimee_msgs__action__LLMGenerate_SendGoal_Request__fini(&array->data[i]);
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

aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence *
aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence * array = (aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence *)allocator.allocate(sizeof(aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence__destroy(aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence__are_equal(const aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence * lhs, const aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__action__LLMGenerate_SendGoal_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence__copy(
  const aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence * input,
  aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__action__LLMGenerate_SendGoal_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__action__LLMGenerate_SendGoal_Request * data =
      (aimee_msgs__action__LLMGenerate_SendGoal_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__action__LLMGenerate_SendGoal_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__action__LLMGenerate_SendGoal_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__action__LLMGenerate_SendGoal_Request__copy(
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
aimee_msgs__action__LLMGenerate_SendGoal_Response__init(aimee_msgs__action__LLMGenerate_SendGoal_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    aimee_msgs__action__LLMGenerate_SendGoal_Response__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__action__LLMGenerate_SendGoal_Response__fini(aimee_msgs__action__LLMGenerate_SendGoal_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
}

bool
aimee_msgs__action__LLMGenerate_SendGoal_Response__are_equal(const aimee_msgs__action__LLMGenerate_SendGoal_Response * lhs, const aimee_msgs__action__LLMGenerate_SendGoal_Response * rhs)
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
aimee_msgs__action__LLMGenerate_SendGoal_Response__copy(
  const aimee_msgs__action__LLMGenerate_SendGoal_Response * input,
  aimee_msgs__action__LLMGenerate_SendGoal_Response * output)
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

aimee_msgs__action__LLMGenerate_SendGoal_Response *
aimee_msgs__action__LLMGenerate_SendGoal_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_SendGoal_Response * msg = (aimee_msgs__action__LLMGenerate_SendGoal_Response *)allocator.allocate(sizeof(aimee_msgs__action__LLMGenerate_SendGoal_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__action__LLMGenerate_SendGoal_Response));
  bool success = aimee_msgs__action__LLMGenerate_SendGoal_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__action__LLMGenerate_SendGoal_Response__destroy(aimee_msgs__action__LLMGenerate_SendGoal_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__action__LLMGenerate_SendGoal_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence__init(aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_SendGoal_Response * data = NULL;

  if (size) {
    data = (aimee_msgs__action__LLMGenerate_SendGoal_Response *)allocator.zero_allocate(size, sizeof(aimee_msgs__action__LLMGenerate_SendGoal_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__action__LLMGenerate_SendGoal_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__action__LLMGenerate_SendGoal_Response__fini(&data[i - 1]);
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
aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence__fini(aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence * array)
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
      aimee_msgs__action__LLMGenerate_SendGoal_Response__fini(&array->data[i]);
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

aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence *
aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence * array = (aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence *)allocator.allocate(sizeof(aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence__destroy(aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence__are_equal(const aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence * lhs, const aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__action__LLMGenerate_SendGoal_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence__copy(
  const aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence * input,
  aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__action__LLMGenerate_SendGoal_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__action__LLMGenerate_SendGoal_Response * data =
      (aimee_msgs__action__LLMGenerate_SendGoal_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__action__LLMGenerate_SendGoal_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__action__LLMGenerate_SendGoal_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__action__LLMGenerate_SendGoal_Response__copy(
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
aimee_msgs__action__LLMGenerate_GetResult_Request__init(aimee_msgs__action__LLMGenerate_GetResult_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    aimee_msgs__action__LLMGenerate_GetResult_Request__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__action__LLMGenerate_GetResult_Request__fini(aimee_msgs__action__LLMGenerate_GetResult_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
}

bool
aimee_msgs__action__LLMGenerate_GetResult_Request__are_equal(const aimee_msgs__action__LLMGenerate_GetResult_Request * lhs, const aimee_msgs__action__LLMGenerate_GetResult_Request * rhs)
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
aimee_msgs__action__LLMGenerate_GetResult_Request__copy(
  const aimee_msgs__action__LLMGenerate_GetResult_Request * input,
  aimee_msgs__action__LLMGenerate_GetResult_Request * output)
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

aimee_msgs__action__LLMGenerate_GetResult_Request *
aimee_msgs__action__LLMGenerate_GetResult_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_GetResult_Request * msg = (aimee_msgs__action__LLMGenerate_GetResult_Request *)allocator.allocate(sizeof(aimee_msgs__action__LLMGenerate_GetResult_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__action__LLMGenerate_GetResult_Request));
  bool success = aimee_msgs__action__LLMGenerate_GetResult_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__action__LLMGenerate_GetResult_Request__destroy(aimee_msgs__action__LLMGenerate_GetResult_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__action__LLMGenerate_GetResult_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence__init(aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_GetResult_Request * data = NULL;

  if (size) {
    data = (aimee_msgs__action__LLMGenerate_GetResult_Request *)allocator.zero_allocate(size, sizeof(aimee_msgs__action__LLMGenerate_GetResult_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__action__LLMGenerate_GetResult_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__action__LLMGenerate_GetResult_Request__fini(&data[i - 1]);
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
aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence__fini(aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence * array)
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
      aimee_msgs__action__LLMGenerate_GetResult_Request__fini(&array->data[i]);
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

aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence *
aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence * array = (aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence *)allocator.allocate(sizeof(aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence__destroy(aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence__are_equal(const aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence * lhs, const aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__action__LLMGenerate_GetResult_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence__copy(
  const aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence * input,
  aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__action__LLMGenerate_GetResult_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__action__LLMGenerate_GetResult_Request * data =
      (aimee_msgs__action__LLMGenerate_GetResult_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__action__LLMGenerate_GetResult_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__action__LLMGenerate_GetResult_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__action__LLMGenerate_GetResult_Request__copy(
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
// #include "aimee_msgs/action/detail/llm_generate__functions.h"

bool
aimee_msgs__action__LLMGenerate_GetResult_Response__init(aimee_msgs__action__LLMGenerate_GetResult_Response * msg)
{
  if (!msg) {
    return false;
  }
  // status
  // result
  if (!aimee_msgs__action__LLMGenerate_Result__init(&msg->result)) {
    aimee_msgs__action__LLMGenerate_GetResult_Response__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__action__LLMGenerate_GetResult_Response__fini(aimee_msgs__action__LLMGenerate_GetResult_Response * msg)
{
  if (!msg) {
    return;
  }
  // status
  // result
  aimee_msgs__action__LLMGenerate_Result__fini(&msg->result);
}

bool
aimee_msgs__action__LLMGenerate_GetResult_Response__are_equal(const aimee_msgs__action__LLMGenerate_GetResult_Response * lhs, const aimee_msgs__action__LLMGenerate_GetResult_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  // result
  if (!aimee_msgs__action__LLMGenerate_Result__are_equal(
      &(lhs->result), &(rhs->result)))
  {
    return false;
  }
  return true;
}

bool
aimee_msgs__action__LLMGenerate_GetResult_Response__copy(
  const aimee_msgs__action__LLMGenerate_GetResult_Response * input,
  aimee_msgs__action__LLMGenerate_GetResult_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  // result
  if (!aimee_msgs__action__LLMGenerate_Result__copy(
      &(input->result), &(output->result)))
  {
    return false;
  }
  return true;
}

aimee_msgs__action__LLMGenerate_GetResult_Response *
aimee_msgs__action__LLMGenerate_GetResult_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_GetResult_Response * msg = (aimee_msgs__action__LLMGenerate_GetResult_Response *)allocator.allocate(sizeof(aimee_msgs__action__LLMGenerate_GetResult_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__action__LLMGenerate_GetResult_Response));
  bool success = aimee_msgs__action__LLMGenerate_GetResult_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__action__LLMGenerate_GetResult_Response__destroy(aimee_msgs__action__LLMGenerate_GetResult_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__action__LLMGenerate_GetResult_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence__init(aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_GetResult_Response * data = NULL;

  if (size) {
    data = (aimee_msgs__action__LLMGenerate_GetResult_Response *)allocator.zero_allocate(size, sizeof(aimee_msgs__action__LLMGenerate_GetResult_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__action__LLMGenerate_GetResult_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__action__LLMGenerate_GetResult_Response__fini(&data[i - 1]);
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
aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence__fini(aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence * array)
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
      aimee_msgs__action__LLMGenerate_GetResult_Response__fini(&array->data[i]);
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

aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence *
aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence * array = (aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence *)allocator.allocate(sizeof(aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence__destroy(aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence__are_equal(const aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence * lhs, const aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__action__LLMGenerate_GetResult_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence__copy(
  const aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence * input,
  aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__action__LLMGenerate_GetResult_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__action__LLMGenerate_GetResult_Response * data =
      (aimee_msgs__action__LLMGenerate_GetResult_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__action__LLMGenerate_GetResult_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__action__LLMGenerate_GetResult_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__action__LLMGenerate_GetResult_Response__copy(
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
// #include "aimee_msgs/action/detail/llm_generate__functions.h"

bool
aimee_msgs__action__LLMGenerate_FeedbackMessage__init(aimee_msgs__action__LLMGenerate_FeedbackMessage * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    aimee_msgs__action__LLMGenerate_FeedbackMessage__fini(msg);
    return false;
  }
  // feedback
  if (!aimee_msgs__action__LLMGenerate_Feedback__init(&msg->feedback)) {
    aimee_msgs__action__LLMGenerate_FeedbackMessage__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__action__LLMGenerate_FeedbackMessage__fini(aimee_msgs__action__LLMGenerate_FeedbackMessage * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // feedback
  aimee_msgs__action__LLMGenerate_Feedback__fini(&msg->feedback);
}

bool
aimee_msgs__action__LLMGenerate_FeedbackMessage__are_equal(const aimee_msgs__action__LLMGenerate_FeedbackMessage * lhs, const aimee_msgs__action__LLMGenerate_FeedbackMessage * rhs)
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
  if (!aimee_msgs__action__LLMGenerate_Feedback__are_equal(
      &(lhs->feedback), &(rhs->feedback)))
  {
    return false;
  }
  return true;
}

bool
aimee_msgs__action__LLMGenerate_FeedbackMessage__copy(
  const aimee_msgs__action__LLMGenerate_FeedbackMessage * input,
  aimee_msgs__action__LLMGenerate_FeedbackMessage * output)
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
  if (!aimee_msgs__action__LLMGenerate_Feedback__copy(
      &(input->feedback), &(output->feedback)))
  {
    return false;
  }
  return true;
}

aimee_msgs__action__LLMGenerate_FeedbackMessage *
aimee_msgs__action__LLMGenerate_FeedbackMessage__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_FeedbackMessage * msg = (aimee_msgs__action__LLMGenerate_FeedbackMessage *)allocator.allocate(sizeof(aimee_msgs__action__LLMGenerate_FeedbackMessage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__action__LLMGenerate_FeedbackMessage));
  bool success = aimee_msgs__action__LLMGenerate_FeedbackMessage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__action__LLMGenerate_FeedbackMessage__destroy(aimee_msgs__action__LLMGenerate_FeedbackMessage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__action__LLMGenerate_FeedbackMessage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence__init(aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_FeedbackMessage * data = NULL;

  if (size) {
    data = (aimee_msgs__action__LLMGenerate_FeedbackMessage *)allocator.zero_allocate(size, sizeof(aimee_msgs__action__LLMGenerate_FeedbackMessage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__action__LLMGenerate_FeedbackMessage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__action__LLMGenerate_FeedbackMessage__fini(&data[i - 1]);
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
aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence__fini(aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence * array)
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
      aimee_msgs__action__LLMGenerate_FeedbackMessage__fini(&array->data[i]);
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

aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence *
aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence * array = (aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence *)allocator.allocate(sizeof(aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence__destroy(aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence__are_equal(const aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence * lhs, const aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__action__LLMGenerate_FeedbackMessage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence__copy(
  const aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence * input,
  aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__action__LLMGenerate_FeedbackMessage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__action__LLMGenerate_FeedbackMessage * data =
      (aimee_msgs__action__LLMGenerate_FeedbackMessage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__action__LLMGenerate_FeedbackMessage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__action__LLMGenerate_FeedbackMessage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__action__LLMGenerate_FeedbackMessage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
