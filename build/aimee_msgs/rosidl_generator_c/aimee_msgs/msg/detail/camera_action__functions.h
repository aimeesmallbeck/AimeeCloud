// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from aimee_msgs:msg/CameraAction.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__CAMERA_ACTION__FUNCTIONS_H_
#define AIMEE_MSGS__MSG__DETAIL__CAMERA_ACTION__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "aimee_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "aimee_msgs/msg/detail/camera_action__struct.h"

/// Initialize msg/CameraAction message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * aimee_msgs__msg__CameraAction
 * )) before or use
 * aimee_msgs__msg__CameraAction__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_aimee_msgs
bool
aimee_msgs__msg__CameraAction__init(aimee_msgs__msg__CameraAction * msg);

/// Finalize msg/CameraAction message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_aimee_msgs
void
aimee_msgs__msg__CameraAction__fini(aimee_msgs__msg__CameraAction * msg);

/// Create msg/CameraAction message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * aimee_msgs__msg__CameraAction__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_aimee_msgs
aimee_msgs__msg__CameraAction *
aimee_msgs__msg__CameraAction__create();

/// Destroy msg/CameraAction message.
/**
 * It calls
 * aimee_msgs__msg__CameraAction__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_aimee_msgs
void
aimee_msgs__msg__CameraAction__destroy(aimee_msgs__msg__CameraAction * msg);

/// Check for msg/CameraAction message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_aimee_msgs
bool
aimee_msgs__msg__CameraAction__are_equal(const aimee_msgs__msg__CameraAction * lhs, const aimee_msgs__msg__CameraAction * rhs);

/// Copy a msg/CameraAction message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_aimee_msgs
bool
aimee_msgs__msg__CameraAction__copy(
  const aimee_msgs__msg__CameraAction * input,
  aimee_msgs__msg__CameraAction * output);

/// Initialize array of msg/CameraAction messages.
/**
 * It allocates the memory for the number of elements and calls
 * aimee_msgs__msg__CameraAction__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_aimee_msgs
bool
aimee_msgs__msg__CameraAction__Sequence__init(aimee_msgs__msg__CameraAction__Sequence * array, size_t size);

/// Finalize array of msg/CameraAction messages.
/**
 * It calls
 * aimee_msgs__msg__CameraAction__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_aimee_msgs
void
aimee_msgs__msg__CameraAction__Sequence__fini(aimee_msgs__msg__CameraAction__Sequence * array);

/// Create array of msg/CameraAction messages.
/**
 * It allocates the memory for the array and calls
 * aimee_msgs__msg__CameraAction__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_aimee_msgs
aimee_msgs__msg__CameraAction__Sequence *
aimee_msgs__msg__CameraAction__Sequence__create(size_t size);

/// Destroy array of msg/CameraAction messages.
/**
 * It calls
 * aimee_msgs__msg__CameraAction__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_aimee_msgs
void
aimee_msgs__msg__CameraAction__Sequence__destroy(aimee_msgs__msg__CameraAction__Sequence * array);

/// Check for msg/CameraAction message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_aimee_msgs
bool
aimee_msgs__msg__CameraAction__Sequence__are_equal(const aimee_msgs__msg__CameraAction__Sequence * lhs, const aimee_msgs__msg__CameraAction__Sequence * rhs);

/// Copy an array of msg/CameraAction messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_aimee_msgs
bool
aimee_msgs__msg__CameraAction__Sequence__copy(
  const aimee_msgs__msg__CameraAction__Sequence * input,
  aimee_msgs__msg__CameraAction__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // AIMEE_MSGS__MSG__DETAIL__CAMERA_ACTION__FUNCTIONS_H_
