// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aimee_msgs:msg/MotorAction.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__MOTOR_ACTION__STRUCT_HPP_
#define AIMEE_MSGS__MSG__DETAIL__MOTOR_ACTION__STRUCT_HPP_

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
# define DEPRECATED__aimee_msgs__msg__MotorAction __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__msg__MotorAction __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MotorAction_
{
  using Type = MotorAction_<ContainerAllocator>;

  explicit MotorAction_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : execution_time(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->motor_id = "";
      this->action_type = "";
    }
  }

  explicit MotorAction_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : motor_id(_alloc),
    action_type(_alloc),
    execution_time(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->motor_id = "";
      this->action_type = "";
    }
  }

  // field types and members
  using _motor_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _motor_id_type motor_id;
  using _action_type_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _action_type_type action_type;
  using _values_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _values_type values;
  using _execution_time_type =
    builtin_interfaces::msg::Duration_<ContainerAllocator>;
  _execution_time_type execution_time;

  // setters for named parameter idiom
  Type & set__motor_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->motor_id = _arg;
    return *this;
  }
  Type & set__action_type(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->action_type = _arg;
    return *this;
  }
  Type & set__values(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->values = _arg;
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
    aimee_msgs::msg::MotorAction_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::msg::MotorAction_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::msg::MotorAction_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::msg::MotorAction_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::MotorAction_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::MotorAction_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::MotorAction_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::MotorAction_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::msg::MotorAction_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::msg::MotorAction_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__msg__MotorAction
    std::shared_ptr<aimee_msgs::msg::MotorAction_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__msg__MotorAction
    std::shared_ptr<aimee_msgs::msg::MotorAction_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MotorAction_ & other) const
  {
    if (this->motor_id != other.motor_id) {
      return false;
    }
    if (this->action_type != other.action_type) {
      return false;
    }
    if (this->values != other.values) {
      return false;
    }
    if (this->execution_time != other.execution_time) {
      return false;
    }
    return true;
  }
  bool operator!=(const MotorAction_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MotorAction_

// alias to use template instance with default allocator
using MotorAction =
  aimee_msgs::msg::MotorAction_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__MOTOR_ACTION__STRUCT_HPP_
