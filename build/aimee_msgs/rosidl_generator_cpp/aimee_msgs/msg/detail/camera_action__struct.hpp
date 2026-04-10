// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aimee_msgs:msg/CameraAction.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__CAMERA_ACTION__STRUCT_HPP_
#define AIMEE_MSGS__MSG__DETAIL__CAMERA_ACTION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'execution_time'
#include "builtin_interfaces/msg/detail/duration__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__msg__CameraAction __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__msg__CameraAction __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CameraAction_
{
  using Type = CameraAction_<ContainerAllocator>;

  explicit CameraAction_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : execution_time(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->action_type = "";
      this->target = "";
      this->confidence = 0.0f;
    }
  }

  explicit CameraAction_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : action_type(_alloc),
    target(_alloc),
    execution_time(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->action_type = "";
      this->target = "";
      this->confidence = 0.0f;
    }
  }

  // field types and members
  using _action_type_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _action_type_type action_type;
  using _target_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _target_type target;
  using _confidence_type =
    float;
  _confidence_type confidence;
  using _execution_time_type =
    builtin_interfaces::msg::Duration_<ContainerAllocator>;
  _execution_time_type execution_time;

  // setters for named parameter idiom
  Type & set__action_type(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->action_type = _arg;
    return *this;
  }
  Type & set__target(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->target = _arg;
    return *this;
  }
  Type & set__confidence(
    const float & _arg)
  {
    this->confidence = _arg;
    return *this;
  }
  Type & set__execution_time(
    const builtin_interfaces::msg::Duration_<ContainerAllocator> & _arg)
  {
    this->execution_time = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::msg::CameraAction_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::msg::CameraAction_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::msg::CameraAction_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::msg::CameraAction_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::CameraAction_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::CameraAction_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::CameraAction_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::CameraAction_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::msg::CameraAction_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::msg::CameraAction_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__msg__CameraAction
    std::shared_ptr<aimee_msgs::msg::CameraAction_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__msg__CameraAction
    std::shared_ptr<aimee_msgs::msg::CameraAction_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CameraAction_ & other) const
  {
    if (this->action_type != other.action_type) {
      return false;
    }
    if (this->target != other.target) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    if (this->execution_time != other.execution_time) {
      return false;
    }
    return true;
  }
  bool operator!=(const CameraAction_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CameraAction_

// alias to use template instance with default allocator
using CameraAction =
  aimee_msgs::msg::CameraAction_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__CAMERA_ACTION__STRUCT_HPP_
