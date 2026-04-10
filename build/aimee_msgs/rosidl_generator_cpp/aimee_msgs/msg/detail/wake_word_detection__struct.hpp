// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aimee_msgs:msg/WakeWordDetection.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__WAKE_WORD_DETECTION__STRUCT_HPP_
#define AIMEE_MSGS__MSG__DETAIL__WAKE_WORD_DETECTION__STRUCT_HPP_

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
# define DEPRECATED__aimee_msgs__msg__WakeWordDetection __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__msg__WakeWordDetection __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct WakeWordDetection_
{
  using Type = WakeWordDetection_<ContainerAllocator>;

  explicit WakeWordDetection_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : timestamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->wake_word = "";
      this->confidence = 0.0f;
      this->source = "";
      this->sample_index = 0;
      this->signal_energy = 0.0f;
      this->active = false;
      this->session_id = "";
    }
  }

  explicit WakeWordDetection_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : wake_word(_alloc),
    source(_alloc),
    timestamp(_alloc, _init),
    session_id(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->wake_word = "";
      this->confidence = 0.0f;
      this->source = "";
      this->sample_index = 0;
      this->signal_energy = 0.0f;
      this->active = false;
      this->session_id = "";
    }
  }

  // field types and members
  using _wake_word_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _wake_word_type wake_word;
  using _confidence_type =
    float;
  _confidence_type confidence;
  using _source_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _source_type source;
  using _sample_index_type =
    uint16_t;
  _sample_index_type sample_index;
  using _signal_energy_type =
    float;
  _signal_energy_type signal_energy;
  using _active_type =
    bool;
  _active_type active;
  using _timestamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _timestamp_type timestamp;
  using _session_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _session_id_type session_id;

  // setters for named parameter idiom
  Type & set__wake_word(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->wake_word = _arg;
    return *this;
  }
  Type & set__confidence(
    const float & _arg)
  {
    this->confidence = _arg;
    return *this;
  }
  Type & set__source(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->source = _arg;
    return *this;
  }
  Type & set__sample_index(
    const uint16_t & _arg)
  {
    this->sample_index = _arg;
    return *this;
  }
  Type & set__signal_energy(
    const float & _arg)
  {
    this->signal_energy = _arg;
    return *this;
  }
  Type & set__active(
    const bool & _arg)
  {
    this->active = _arg;
    return *this;
  }
  Type & set__timestamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->timestamp = _arg;
    return *this;
  }
  Type & set__session_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->session_id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::msg::WakeWordDetection_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::msg::WakeWordDetection_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::msg::WakeWordDetection_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::msg::WakeWordDetection_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::WakeWordDetection_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::WakeWordDetection_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::WakeWordDetection_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::WakeWordDetection_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::msg::WakeWordDetection_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::msg::WakeWordDetection_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__msg__WakeWordDetection
    std::shared_ptr<aimee_msgs::msg::WakeWordDetection_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__msg__WakeWordDetection
    std::shared_ptr<aimee_msgs::msg::WakeWordDetection_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const WakeWordDetection_ & other) const
  {
    if (this->wake_word != other.wake_word) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    if (this->source != other.source) {
      return false;
    }
    if (this->sample_index != other.sample_index) {
      return false;
    }
    if (this->signal_energy != other.signal_energy) {
      return false;
    }
    if (this->active != other.active) {
      return false;
    }
    if (this->timestamp != other.timestamp) {
      return false;
    }
    if (this->session_id != other.session_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const WakeWordDetection_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct WakeWordDetection_

// alias to use template instance with default allocator
using WakeWordDetection =
  aimee_msgs::msg::WakeWordDetection_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__WAKE_WORD_DETECTION__STRUCT_HPP_
