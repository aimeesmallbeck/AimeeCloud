// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aimee_msgs:msg/TrackingCommand.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__TRACKING_COMMAND__STRUCT_HPP_
#define AIMEE_MSGS__MSG__DETAIL__TRACKING_COMMAND__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'target_position'
#include "geometry_msgs/msg/detail/point__struct.hpp"
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__msg__TrackingCommand __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__msg__TrackingCommand __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TrackingCommand_
{
  using Type = TrackingCommand_<ContainerAllocator>;

  explicit TrackingCommand_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : target_position(_init),
    timestamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->command = "";
      this->mode = "";
      this->preset_id = 0l;
      this->zoom_level = 0l;
      this->target_type = "";
      this->target_id = "";
    }
  }

  explicit TrackingCommand_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : command(_alloc),
    mode(_alloc),
    target_type(_alloc),
    target_id(_alloc),
    target_position(_alloc, _init),
    timestamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->command = "";
      this->mode = "";
      this->preset_id = 0l;
      this->zoom_level = 0l;
      this->target_type = "";
      this->target_id = "";
    }
  }

  // field types and members
  using _command_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _command_type command;
  using _mode_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _mode_type mode;
  using _preset_id_type =
    int32_t;
  _preset_id_type preset_id;
  using _zoom_level_type =
    int32_t;
  _zoom_level_type zoom_level;
  using _target_type_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _target_type_type target_type;
  using _target_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _target_id_type target_id;
  using _target_position_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _target_position_type target_position;
  using _timestamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _timestamp_type timestamp;

  // setters for named parameter idiom
  Type & set__command(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->command = _arg;
    return *this;
  }
  Type & set__mode(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->mode = _arg;
    return *this;
  }
  Type & set__preset_id(
    const int32_t & _arg)
  {
    this->preset_id = _arg;
    return *this;
  }
  Type & set__zoom_level(
    const int32_t & _arg)
  {
    this->zoom_level = _arg;
    return *this;
  }
  Type & set__target_type(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->target_type = _arg;
    return *this;
  }
  Type & set__target_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->target_id = _arg;
    return *this;
  }
  Type & set__target_position(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->target_position = _arg;
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
    aimee_msgs::msg::TrackingCommand_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::msg::TrackingCommand_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::msg::TrackingCommand_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::msg::TrackingCommand_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::TrackingCommand_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::TrackingCommand_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::TrackingCommand_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::TrackingCommand_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::msg::TrackingCommand_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::msg::TrackingCommand_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__msg__TrackingCommand
    std::shared_ptr<aimee_msgs::msg::TrackingCommand_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__msg__TrackingCommand
    std::shared_ptr<aimee_msgs::msg::TrackingCommand_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TrackingCommand_ & other) const
  {
    if (this->command != other.command) {
      return false;
    }
    if (this->mode != other.mode) {
      return false;
    }
    if (this->preset_id != other.preset_id) {
      return false;
    }
    if (this->zoom_level != other.zoom_level) {
      return false;
    }
    if (this->target_type != other.target_type) {
      return false;
    }
    if (this->target_id != other.target_id) {
      return false;
    }
    if (this->target_position != other.target_position) {
      return false;
    }
    if (this->timestamp != other.timestamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const TrackingCommand_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TrackingCommand_

// alias to use template instance with default allocator
using TrackingCommand =
  aimee_msgs::msg::TrackingCommand_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__TRACKING_COMMAND__STRUCT_HPP_
