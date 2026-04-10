// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aimee_msgs:msg/RobotState.idl
// generated code does not contain a copyright notice
#include "aimee_msgs/msg/detail/robot_state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `robot_name`
// Member `robot_type`
// Member `power_status`
// Member `current_action`
// Member `arm_pose_name`
// Member `camera_mode`
// Member `tracking_target`
// Member `active_skills`
// Member `current_skill_id`
// Member `errors`
// Member `warnings`
#include "rosidl_runtime_c/string_functions.h"
// Member `current_velocity`
#include "geometry_msgs/msg/detail/twist__functions.h"
// Member `odometry`
#include "nav_msgs/msg/detail/odometry__functions.h"
// Member `arm_state`
#include "sensor_msgs/msg/detail/joint_state__functions.h"
// Member `timestamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
aimee_msgs__msg__RobotState__init(aimee_msgs__msg__RobotState * msg)
{
  if (!msg) {
    return false;
  }
  // robot_name
  if (!rosidl_runtime_c__String__init(&msg->robot_name)) {
    aimee_msgs__msg__RobotState__fini(msg);
    return false;
  }
  // robot_type
  if (!rosidl_runtime_c__String__init(&msg->robot_type)) {
    aimee_msgs__msg__RobotState__fini(msg);
    return false;
  }
  // battery_level
  // is_charging
  // power_status
  if (!rosidl_runtime_c__String__init(&msg->power_status)) {
    aimee_msgs__msg__RobotState__fini(msg);
    return false;
  }
  // current_action
  if (!rosidl_runtime_c__String__init(&msg->current_action)) {
    aimee_msgs__msg__RobotState__fini(msg);
    return false;
  }
  // current_velocity
  if (!geometry_msgs__msg__Twist__init(&msg->current_velocity)) {
    aimee_msgs__msg__RobotState__fini(msg);
    return false;
  }
  // odometry
  if (!nav_msgs__msg__Odometry__init(&msg->odometry)) {
    aimee_msgs__msg__RobotState__fini(msg);
    return false;
  }
  // arm_state
  if (!sensor_msgs__msg__JointState__init(&msg->arm_state)) {
    aimee_msgs__msg__RobotState__fini(msg);
    return false;
  }
  // arm_is_moving
  // arm_pose_name
  if (!rosidl_runtime_c__String__init(&msg->arm_pose_name)) {
    aimee_msgs__msg__RobotState__fini(msg);
    return false;
  }
  // gripper_position
  // camera_mode
  if (!rosidl_runtime_c__String__init(&msg->camera_mode)) {
    aimee_msgs__msg__RobotState__fini(msg);
    return false;
  }
  // tracking_target
  if (!rosidl_runtime_c__String__init(&msg->tracking_target)) {
    aimee_msgs__msg__RobotState__fini(msg);
    return false;
  }
  // active_skills
  if (!rosidl_runtime_c__String__Sequence__init(&msg->active_skills, 0)) {
    aimee_msgs__msg__RobotState__fini(msg);
    return false;
  }
  // current_skill_id
  if (!rosidl_runtime_c__String__init(&msg->current_skill_id)) {
    aimee_msgs__msg__RobotState__fini(msg);
    return false;
  }
  // errors
  if (!rosidl_runtime_c__String__Sequence__init(&msg->errors, 0)) {
    aimee_msgs__msg__RobotState__fini(msg);
    return false;
  }
  // warnings
  if (!rosidl_runtime_c__String__Sequence__init(&msg->warnings, 0)) {
    aimee_msgs__msg__RobotState__fini(msg);
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__init(&msg->timestamp)) {
    aimee_msgs__msg__RobotState__fini(msg);
    return false;
  }
  return true;
}

void
aimee_msgs__msg__RobotState__fini(aimee_msgs__msg__RobotState * msg)
{
  if (!msg) {
    return;
  }
  // robot_name
  rosidl_runtime_c__String__fini(&msg->robot_name);
  // robot_type
  rosidl_runtime_c__String__fini(&msg->robot_type);
  // battery_level
  // is_charging
  // power_status
  rosidl_runtime_c__String__fini(&msg->power_status);
  // current_action
  rosidl_runtime_c__String__fini(&msg->current_action);
  // current_velocity
  geometry_msgs__msg__Twist__fini(&msg->current_velocity);
  // odometry
  nav_msgs__msg__Odometry__fini(&msg->odometry);
  // arm_state
  sensor_msgs__msg__JointState__fini(&msg->arm_state);
  // arm_is_moving
  // arm_pose_name
  rosidl_runtime_c__String__fini(&msg->arm_pose_name);
  // gripper_position
  // camera_mode
  rosidl_runtime_c__String__fini(&msg->camera_mode);
  // tracking_target
  rosidl_runtime_c__String__fini(&msg->tracking_target);
  // active_skills
  rosidl_runtime_c__String__Sequence__fini(&msg->active_skills);
  // current_skill_id
  rosidl_runtime_c__String__fini(&msg->current_skill_id);
  // errors
  rosidl_runtime_c__String__Sequence__fini(&msg->errors);
  // warnings
  rosidl_runtime_c__String__Sequence__fini(&msg->warnings);
  // timestamp
  builtin_interfaces__msg__Time__fini(&msg->timestamp);
}

bool
aimee_msgs__msg__RobotState__are_equal(const aimee_msgs__msg__RobotState * lhs, const aimee_msgs__msg__RobotState * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // robot_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->robot_name), &(rhs->robot_name)))
  {
    return false;
  }
  // robot_type
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->robot_type), &(rhs->robot_type)))
  {
    return false;
  }
  // battery_level
  if (lhs->battery_level != rhs->battery_level) {
    return false;
  }
  // is_charging
  if (lhs->is_charging != rhs->is_charging) {
    return false;
  }
  // power_status
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->power_status), &(rhs->power_status)))
  {
    return false;
  }
  // current_action
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->current_action), &(rhs->current_action)))
  {
    return false;
  }
  // current_velocity
  if (!geometry_msgs__msg__Twist__are_equal(
      &(lhs->current_velocity), &(rhs->current_velocity)))
  {
    return false;
  }
  // odometry
  if (!nav_msgs__msg__Odometry__are_equal(
      &(lhs->odometry), &(rhs->odometry)))
  {
    return false;
  }
  // arm_state
  if (!sensor_msgs__msg__JointState__are_equal(
      &(lhs->arm_state), &(rhs->arm_state)))
  {
    return false;
  }
  // arm_is_moving
  if (lhs->arm_is_moving != rhs->arm_is_moving) {
    return false;
  }
  // arm_pose_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->arm_pose_name), &(rhs->arm_pose_name)))
  {
    return false;
  }
  // gripper_position
  if (lhs->gripper_position != rhs->gripper_position) {
    return false;
  }
  // camera_mode
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->camera_mode), &(rhs->camera_mode)))
  {
    return false;
  }
  // tracking_target
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->tracking_target), &(rhs->tracking_target)))
  {
    return false;
  }
  // active_skills
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->active_skills), &(rhs->active_skills)))
  {
    return false;
  }
  // current_skill_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->current_skill_id), &(rhs->current_skill_id)))
  {
    return false;
  }
  // errors
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->errors), &(rhs->errors)))
  {
    return false;
  }
  // warnings
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->warnings), &(rhs->warnings)))
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
aimee_msgs__msg__RobotState__copy(
  const aimee_msgs__msg__RobotState * input,
  aimee_msgs__msg__RobotState * output)
{
  if (!input || !output) {
    return false;
  }
  // robot_name
  if (!rosidl_runtime_c__String__copy(
      &(input->robot_name), &(output->robot_name)))
  {
    return false;
  }
  // robot_type
  if (!rosidl_runtime_c__String__copy(
      &(input->robot_type), &(output->robot_type)))
  {
    return false;
  }
  // battery_level
  output->battery_level = input->battery_level;
  // is_charging
  output->is_charging = input->is_charging;
  // power_status
  if (!rosidl_runtime_c__String__copy(
      &(input->power_status), &(output->power_status)))
  {
    return false;
  }
  // current_action
  if (!rosidl_runtime_c__String__copy(
      &(input->current_action), &(output->current_action)))
  {
    return false;
  }
  // current_velocity
  if (!geometry_msgs__msg__Twist__copy(
      &(input->current_velocity), &(output->current_velocity)))
  {
    return false;
  }
  // odometry
  if (!nav_msgs__msg__Odometry__copy(
      &(input->odometry), &(output->odometry)))
  {
    return false;
  }
  // arm_state
  if (!sensor_msgs__msg__JointState__copy(
      &(input->arm_state), &(output->arm_state)))
  {
    return false;
  }
  // arm_is_moving
  output->arm_is_moving = input->arm_is_moving;
  // arm_pose_name
  if (!rosidl_runtime_c__String__copy(
      &(input->arm_pose_name), &(output->arm_pose_name)))
  {
    return false;
  }
  // gripper_position
  output->gripper_position = input->gripper_position;
  // camera_mode
  if (!rosidl_runtime_c__String__copy(
      &(input->camera_mode), &(output->camera_mode)))
  {
    return false;
  }
  // tracking_target
  if (!rosidl_runtime_c__String__copy(
      &(input->tracking_target), &(output->tracking_target)))
  {
    return false;
  }
  // active_skills
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->active_skills), &(output->active_skills)))
  {
    return false;
  }
  // current_skill_id
  if (!rosidl_runtime_c__String__copy(
      &(input->current_skill_id), &(output->current_skill_id)))
  {
    return false;
  }
  // errors
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->errors), &(output->errors)))
  {
    return false;
  }
  // warnings
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->warnings), &(output->warnings)))
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

aimee_msgs__msg__RobotState *
aimee_msgs__msg__RobotState__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__RobotState * msg = (aimee_msgs__msg__RobotState *)allocator.allocate(sizeof(aimee_msgs__msg__RobotState), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aimee_msgs__msg__RobotState));
  bool success = aimee_msgs__msg__RobotState__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aimee_msgs__msg__RobotState__destroy(aimee_msgs__msg__RobotState * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aimee_msgs__msg__RobotState__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aimee_msgs__msg__RobotState__Sequence__init(aimee_msgs__msg__RobotState__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__RobotState * data = NULL;

  if (size) {
    data = (aimee_msgs__msg__RobotState *)allocator.zero_allocate(size, sizeof(aimee_msgs__msg__RobotState), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aimee_msgs__msg__RobotState__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aimee_msgs__msg__RobotState__fini(&data[i - 1]);
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
aimee_msgs__msg__RobotState__Sequence__fini(aimee_msgs__msg__RobotState__Sequence * array)
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
      aimee_msgs__msg__RobotState__fini(&array->data[i]);
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

aimee_msgs__msg__RobotState__Sequence *
aimee_msgs__msg__RobotState__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aimee_msgs__msg__RobotState__Sequence * array = (aimee_msgs__msg__RobotState__Sequence *)allocator.allocate(sizeof(aimee_msgs__msg__RobotState__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aimee_msgs__msg__RobotState__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aimee_msgs__msg__RobotState__Sequence__destroy(aimee_msgs__msg__RobotState__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aimee_msgs__msg__RobotState__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aimee_msgs__msg__RobotState__Sequence__are_equal(const aimee_msgs__msg__RobotState__Sequence * lhs, const aimee_msgs__msg__RobotState__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aimee_msgs__msg__RobotState__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aimee_msgs__msg__RobotState__Sequence__copy(
  const aimee_msgs__msg__RobotState__Sequence * input,
  aimee_msgs__msg__RobotState__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aimee_msgs__msg__RobotState);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aimee_msgs__msg__RobotState * data =
      (aimee_msgs__msg__RobotState *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aimee_msgs__msg__RobotState__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aimee_msgs__msg__RobotState__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aimee_msgs__msg__RobotState__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
