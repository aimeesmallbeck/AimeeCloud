// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aimee_msgs:msg/FaceDetection.idl
// generated code does not contain a copyright notice
#include "aimee_msgs/msg/detail/face_detection__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `face_id`
// Member `person_name`
// Member `camera_source`
#include "rosidl_runtime_c/string_functions.h"
// Member `face_landmarks`
#include "rosidl_runtime_c/primitives_sequence_functions.h"
// Member `position_3d`
#include "geometry_msgs/msg/detail/point__functions.h"
// Member `timestamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
aimee_msgs__msg__FaceDetection__init(aimee_msgs__msg__FaceDetection * msg)
{
  if (!msg) {
    return false;
  }
  // face_id
  if (!rosidl_runtime_c__String__init(&msg->face_id)) {
    aimee_msgs__msg__FaceDetection__fini(msg);
    return false;
  }
  // person_name
  if (!rosidl_runtime_c__String__init(&msg->person_name)) {
    aimee_msgs__msg__FaceDetection__fini(msg);
    return false;
  }
  // recognition_confidence
  // center_x
  // center_y
  // width
  // height
  // num_faces_detected
  // face_landmarks
  if (!rosidl_runtime_c__float__Sequence__init(&msg->face_landmarks, 0)) {
    aimee_msgs__msg__FaceDetection__fini(msg);
    return false;
  }
  // position_3d
  if (!geometry_msgs__msg__Point__init(&msg->position_3d)) {
    aimee_msgs__msg__FaceDetection__fini(msg);
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__init(&msg->timestamp)) {
    aimee_msgs__msg__FaceDetection__fini(msg);
    return false;
  }
  // camera_source
  if (!rosidl_runtime_c__String__init(&msg->camera_source)) {
    aimee_msgs__msg__FaceDetection__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__msg__FaceDetection__fini(aimee_msgs__msg__FaceDetection * msg)
{
  if (!msg) {
    return;
  }
  // face_id
  rosidl_runtime_c__String__fini(&msg->face_id);
  // person_name
  rosidl_runtime_c__String__fini(&msg->person_name);
  // recognition_confidence
  // center_x
  // center_y
  // width
  // height
  // num_faces_detected
  // face_landmarks
  rosidl_runtime_c__float__Sequence__fini(&msg->face_landmarks);
  // position_3d
  geometry_msgs__msg__Point__fini(&msg->position_3d);
  // timestamp
  builtin_interfaces__msg__Time__fini(&msg->timestamp);
  // camera_source
  rosidl_runtime_c__String__fini(&msg->camera_source);
}

bool
aimee_msgs__msg__FaceDetection__are_equal(const aimee_msgs__msg__FaceDetection * lhs, const aimee_msgs__msg__FaceDetection * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // face_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->face_id), &(rhs->face_id)))
  {
    return false;
  }
  // person_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->person_name), &(rhs->person_name)))
  {
    return false;
  }
  // recognition_confidence
  if (lhs->recognition_confidence != rhs->recognition_confidence) {
    return false;
  }
  // center_x
  if (lhs->center_x != rhs->center_x) {
    return false;
  }
  // center_y
  if (lhs->center_y != rhs->center_y) {
    return false;
  }
  // width
  if (lhs->width != rhs->width) {
    return false;
  }
  // height
  if (lhs->height != rhs->height) {
    return false;
  }
  // num_faces_detected
  if (lhs->num_faces_detected != rhs->num_faces_detected) {
    return false;
  }
  // face_landmarks
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->face_landmarks), &(rhs->face_landmarks)))
  {
    return false;
  }
  // position_3d
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->position_3d), &(rhs->position_3d)))
  {
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->timestamp), &(rhs->timestamp)))
  {
    return false;
  }
  // camera_source
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->camera_source), &(rhs->camera_source)))
  {
    return false;
  }
  return true;
}

bool
aimee_msgs__msg__FaceDetection__copy(
  const aimee_msgs__msg__FaceDetection * input,
  aimee_msgs__msg__FaceDetection * output)
{
  if (!input || !output) {
    return false;
  }
  // face_id
  if (!rosidl_runtime_c__String__copy(
      &(input->face_id), &(output->face_id)))
  {
    return false;
  }
  // person_name
  if (!rosidl_runtime_c__String__copy(
      &(input->person_name), &(output->person_name)))
  {
    return false;
  }
  // recognition_confidence
  output->recognition_confidence = input->recognition_confidence;
  // center_x
  output->center_x = input->center_x;
  // center_y
  output->center_y = input->center_y;
  // width
  output->width = input->width;
  // height
  output->height = input->height;
  // num_faces_detected
  output->num_faces_detected = input->num_faces_detected;
  // face_landmarks
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->face_landmarks), &(output->face_landmarks)))
  {
    return false;
  }
  // position_3d
  if (!geometry_msgs__msg__Point__copy(
      &(input->position_3d), &(output->position_3d)))
  {
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->timestamp), &(output->timestamp)))
  {
    return false;
  }
  // camera_source
  if (!rosidl_runtime_c__String__copy(
      &(input->camera_source), &(output->camera_source)))
  {
    return false;
  }
  return true;
}

aimee_msgs__msg__FaceDetection *
aimee_msgs__msg__FaceDetection__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__FaceDetection * msg = (aimee_msgs__msg__FaceDetection *)allocator.allocate(sizeof(aimee_msgs__msg__FaceDetection), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__msg__FaceDetection));
  bool success = aimee_msgs__msg__FaceDetection__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__msg__FaceDetection__destroy(aimee_msgs__msg__FaceDetection * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__msg__FaceDetection__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__msg__FaceDetection__Sequence__init(aimee_msgs__msg__FaceDetection__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__FaceDetection * data = NULL;

  if (size) {
    data = (aimee_msgs__msg__FaceDetection *)allocator.zero_allocate(size, sizeof(aimee_msgs__msg__FaceDetection), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__msg__FaceDetection__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__msg__FaceDetection__fini(&data[i - 1]);
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
aimee_msgs__msg__FaceDetection__Sequence__fini(aimee_msgs__msg__FaceDetection__Sequence * array)
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
      aimee_msgs__msg__FaceDetection__fini(&array->data[i]);
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

aimee_msgs__msg__FaceDetection__Sequence *
aimee_msgs__msg__FaceDetection__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__FaceDetection__Sequence * array = (aimee_msgs__msg__FaceDetection__Sequence *)allocator.allocate(sizeof(aimee_msgs__msg__FaceDetection__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__msg__FaceDetection__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__msg__FaceDetection__Sequence__destroy(aimee_msgs__msg__FaceDetection__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__msg__FaceDetection__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__msg__FaceDetection__Sequence__are_equal(const aimee_msgs__msg__FaceDetection__Sequence * lhs, const aimee_msgs__msg__FaceDetection__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__msg__FaceDetection__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__msg__FaceDetection__Sequence__copy(
  const aimee_msgs__msg__FaceDetection__Sequence * input,
  aimee_msgs__msg__FaceDetection__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__msg__FaceDetection);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__msg__FaceDetection * data =
      (aimee_msgs__msg__FaceDetection *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__msg__FaceDetection__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__msg__FaceDetection__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__msg__FaceDetection__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
