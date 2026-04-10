// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aimee_msgs:msg/LEDAction.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__LED_ACTION__STRUCT_HPP_
#define AIMEE_MSGS__MSG__DETAIL__LED_ACTION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__aimee_msgs__msg__LEDAction __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__msg__LEDAction __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct LEDAction_
{
  using Type = LEDAction_<ContainerAllocator>;

  explicit LEDAction_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->led_id = "";
      this->pattern = "";
      this->duration_sec = 0.0f;
    }
  }

  explicit LEDAction_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : led_id(_alloc),
    pattern(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->led_id = "";
      this->pattern = "";
      this->duration_sec = 0.0f;
    }
  }

  // field types and members
  using _led_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _led_id_type led_id;
  using _color_type =
    std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>>;
  _color_type color;
  using _pattern_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _pattern_type pattern;
  using _duration_sec_type =
    float;
  _duration_sec_type duration_sec;

  // setters for named parameter idiom
  Type & set__led_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->led_id = _arg;
    return *this;
  }
  Type & set__color(
    const std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>> & _arg)
  {
    this->color = _arg;
    return *this;
  }
  Type & set__pattern(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->pattern = _arg;
    return *this;
  }
  Type & set__duration_sec(
    const float & _arg)
  {
    this->duration_sec = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::msg::LEDAction_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::msg::LEDAction_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::msg::LEDAction_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::msg::LEDAction_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::LEDAction_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::LEDAction_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::LEDAction_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::LEDAction_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::msg::LEDAction_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::msg::LEDAction_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__msg__LEDAction
    std::shared_ptr<aimee_msgs::msg::LEDAction_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__msg__LEDAction
    std::shared_ptr<aimee_msgs::msg::LEDAction_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LEDAction_ & other) const
  {
    if (this->led_id != other.led_id) {
      return false;
    }
    if (this->color != other.color) {
      return false;
    }
    if (this->pattern != other.pattern) {
      return false;
    }
    if (this->duration_sec != other.duration_sec) {
      return false;
    }
    return true;
  }
  bool operator!=(const LEDAction_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LEDAction_

// alias to use template instance with default allocator
using LEDAction =
  aimee_msgs::msg::LEDAction_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__LED_ACTION__STRUCT_HPP_
