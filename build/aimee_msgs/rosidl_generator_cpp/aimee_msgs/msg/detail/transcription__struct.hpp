// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aimee_msgs:msg/Transcription.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__TRANSCRIPTION__STRUCT_HPP_
#define AIMEE_MSGS__MSG__DETAIL__TRANSCRIPTION__STRUCT_HPP_

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
# define DEPRECATED__aimee_msgs__msg__Transcription __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__msg__Transcription __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Transcription_
{
  using Type = Transcription_<ContainerAllocator>;

  explicit Transcription_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : timestamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->text = "";
      this->confidence = 0.0f;
      this->source = "";
      this->is_command = false;
      this->is_partial = false;
      this->wake_word_detected = false;
      this->wake_word = "";
      this->session_id = "";
      this->correlation_id = "";
    }
  }

  explicit Transcription_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : text(_alloc),
    source(_alloc),
    wake_word(_alloc),
    timestamp(_alloc, _init),
    session_id(_alloc),
    correlation_id(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->text = "";
      this->confidence = 0.0f;
      this->source = "";
      this->is_command = false;
      this->is_partial = false;
      this->wake_word_detected = false;
      this->wake_word = "";
      this->session_id = "";
      this->correlation_id = "";
    }
  }

  // field types and members
  using _text_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _text_type text;
  using _confidence_type =
    float;
  _confidence_type confidence;
  using _source_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _source_type source;
  using _is_command_type =
    bool;
  _is_command_type is_command;
  using _is_partial_type =
    bool;
  _is_partial_type is_partial;
  using _wake_word_detected_type =
    bool;
  _wake_word_detected_type wake_word_detected;
  using _wake_word_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _wake_word_type wake_word;
  using _timestamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _timestamp_type timestamp;
  using _session_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _session_id_type session_id;
  using _correlation_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _correlation_id_type correlation_id;

  // setters for named parameter idiom
  Type & set__text(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->text = _arg;
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
  Type & set__is_command(
    const bool & _arg)
  {
    this->is_command = _arg;
    return *this;
  }
  Type & set__is_partial(
    const bool & _arg)
  {
    this->is_partial = _arg;
    return *this;
  }
  Type & set__wake_word_detected(
    const bool & _arg)
  {
    this->wake_word_detected = _arg;
    return *this;
  }
  Type & set__wake_word(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->wake_word = _arg;
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
  Type & set__correlation_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->correlation_id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::msg::Transcription_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::msg::Transcription_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::msg::Transcription_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::msg::Transcription_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::Transcription_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::Transcription_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::Transcription_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::Transcription_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::msg::Transcription_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::msg::Transcription_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__msg__Transcription
    std::shared_ptr<aimee_msgs::msg::Transcription_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__msg__Transcription
    std::shared_ptr<aimee_msgs::msg::Transcription_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Transcription_ & other) const
  {
    if (this->text != other.text) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    if (this->source != other.source) {
      return false;
    }
    if (this->is_command != other.is_command) {
      return false;
    }
    if (this->is_partial != other.is_partial) {
      return false;
    }
    if (this->wake_word_detected != other.wake_word_detected) {
      return false;
    }
    if (this->wake_word != other.wake_word) {
      return false;
    }
    if (this->timestamp != other.timestamp) {
      return false;
    }
    if (this->session_id != other.session_id) {
      return false;
    }
    if (this->correlation_id != other.correlation_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const Transcription_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Transcription_

// alias to use template instance with default allocator
using Transcription =
  aimee_msgs::msg::Transcription_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__TRANSCRIPTION__STRUCT_HPP_
