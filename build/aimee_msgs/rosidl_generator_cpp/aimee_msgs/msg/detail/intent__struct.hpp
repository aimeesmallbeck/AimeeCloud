// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aimee_msgs:msg/Intent.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__INTENT__STRUCT_HPP_
#define AIMEE_MSGS__MSG__DETAIL__INTENT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__msg__Intent __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__msg__Intent __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Intent_
{
  using Type = Intent_<ContainerAllocator>;

  explicit Intent_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : timestamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->intent_type = "";
      this->action = "";
      this->confidence = 0.0f;
      this->raw_text = "";
      this->requires_skill = false;
      this->skill_name = "";
      this->parameters_json = "";
      this->session_id = "";
    }
  }

  explicit Intent_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : intent_type(_alloc),
    action(_alloc),
    raw_text(_alloc),
    skill_name(_alloc),
    parameters_json(_alloc),
    session_id(_alloc),
    timestamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->intent_type = "";
      this->action = "";
      this->confidence = 0.0f;
      this->raw_text = "";
      this->requires_skill = false;
      this->skill_name = "";
      this->parameters_json = "";
      this->session_id = "";
    }
  }

  // field types and members
  using _intent_type_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _intent_type_type intent_type;
  using _action_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _action_type action;
  using _confidence_type =
    float;
  _confidence_type confidence;
  using _raw_text_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _raw_text_type raw_text;
  using _requires_skill_type =
    bool;
  _requires_skill_type requires_skill;
  using _skill_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _skill_name_type skill_name;
  using _parameters_json_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _parameters_json_type parameters_json;
  using _session_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _session_id_type session_id;
  using _timestamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _timestamp_type timestamp;

  // setters for named parameter idiom
  Type & set__intent_type(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->intent_type = _arg;
    return *this;
  }
  Type & set__action(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->action = _arg;
    return *this;
  }
  Type & set__confidence(
    const float & _arg)
  {
    this->confidence = _arg;
    return *this;
  }
  Type & set__raw_text(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->raw_text = _arg;
    return *this;
  }
  Type & set__requires_skill(
    const bool & _arg)
  {
    this->requires_skill = _arg;
    return *this;
  }
  Type & set__skill_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->skill_name = _arg;
    return *this;
  }
  Type & set__parameters_json(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->parameters_json = _arg;
    return *this;
  }
  Type & set__session_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->session_id = _arg;
    return *this;
  }
  Type & set__timestamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->timestamp = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::msg::Intent_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::msg::Intent_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::msg::Intent_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::msg::Intent_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::Intent_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::Intent_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::Intent_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::Intent_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::msg::Intent_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::msg::Intent_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__msg__Intent
    std::shared_ptr<aimee_msgs::msg::Intent_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__msg__Intent
    std::shared_ptr<aimee_msgs::msg::Intent_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Intent_ & other) const
  {
    if (this->intent_type != other.intent_type) {
      return false;
    }
    if (this->action != other.action) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    if (this->raw_text != other.raw_text) {
      return false;
    }
    if (this->requires_skill != other.requires_skill) {
      return false;
    }
    if (this->skill_name != other.skill_name) {
      return false;
    }
    if (this->parameters_json != other.parameters_json) {
      return false;
    }
    if (this->session_id != other.session_id) {
      return false;
    }
    if (this->timestamp != other.timestamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const Intent_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Intent_

// alias to use template instance with default allocator
using Intent =
  aimee_msgs::msg::Intent_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__INTENT__STRUCT_HPP_
