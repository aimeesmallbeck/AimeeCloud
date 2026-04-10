// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aimee_msgs:msg/RobotState.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__ROBOT_STATE__STRUCT_HPP_
#define AIMEE_MSGS__MSG__DETAIL__ROBOT_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'current_velocity'
#include "geometry_msgs/msg/detail/twist__struct.hpp"
// Member 'odometry'
#include "nav_msgs/msg/detail/odometry__struct.hpp"
// Member 'arm_state'
#include "sensor_msgs/msg/detail/joint_state__struct.hpp"
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__msg__RobotState __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__msg__RobotState __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct RobotState_
{
  using Type = RobotState_<ContainerAllocator>;

  explicit RobotState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : current_velocity(_init),
    odometry(_init),
    arm_state(_init),
    timestamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->robot_name = "";
      this->robot_type = "";
      this->battery_level = 0.0f;
      this->is_charging = false;
      this->power_status = "";
      this->current_action = "";
      this->arm_is_moving = false;
      this->arm_pose_name = "";
      this->gripper_position = 0.0f;
      this->camera_mode = "";
      this->tracking_target = "";
      this->current_skill_id = "";
    }
  }

  explicit RobotState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : robot_name(_alloc),
    robot_type(_alloc),
    power_status(_alloc),
    current_action(_alloc),
    current_velocity(_alloc, _init),
    odometry(_alloc, _init),
    arm_state(_alloc, _init),
    arm_pose_name(_alloc),
    camera_mode(_alloc),
    tracking_target(_alloc),
    current_skill_id(_alloc),
    timestamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->robot_name = "";
      this->robot_type = "";
      this->battery_level = 0.0f;
      this->is_charging = false;
      this->power_status = "";
      this->current_action = "";
      this->arm_is_moving = false;
      this->arm_pose_name = "";
      this->gripper_position = 0.0f;
      this->camera_mode = "";
      this->tracking_target = "";
      this->current_skill_id = "";
    }
  }

  // field types and members
  using _robot_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _robot_name_type robot_name;
  using _robot_type_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _robot_type_type robot_type;
  using _battery_level_type =
    float;
  _battery_level_type battery_level;
  using _is_charging_type =
    bool;
  _is_charging_type is_charging;
  using _power_status_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _power_status_type power_status;
  using _current_action_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _current_action_type current_action;
  using _current_velocity_type =
    geometry_msgs::msg::Twist_<ContainerAllocator>;
  _current_velocity_type current_velocity;
  using _odometry_type =
    nav_msgs::msg::Odometry_<ContainerAllocator>;
  _odometry_type odometry;
  using _arm_state_type =
    sensor_msgs::msg::JointState_<ContainerAllocator>;
  _arm_state_type arm_state;
  using _arm_is_moving_type =
    bool;
  _arm_is_moving_type arm_is_moving;
  using _arm_pose_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _arm_pose_name_type arm_pose_name;
  using _gripper_position_type =
    float;
  _gripper_position_type gripper_position;
  using _camera_mode_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _camera_mode_type camera_mode;
  using _tracking_target_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _tracking_target_type tracking_target;
  using _active_skills_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _active_skills_type active_skills;
  using _current_skill_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _current_skill_id_type current_skill_id;
  using _errors_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _errors_type errors;
  using _warnings_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _warnings_type warnings;
  using _timestamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _timestamp_type timestamp;

  // setters for named parameter idiom
  Type & set__robot_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->robot_name = _arg;
    return *this;
  }
  Type & set__robot_type(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->robot_type = _arg;
    return *this;
  }
  Type & set__battery_level(
    const float & _arg)
  {
    this->battery_level = _arg;
    return *this;
  }
  Type & set__is_charging(
    const bool & _arg)
  {
    this->is_charging = _arg;
    return *this;
  }
  Type & set__power_status(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->power_status = _arg;
    return *this;
  }
  Type & set__current_action(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->current_action = _arg;
    return *this;
  }
  Type & set__current_velocity(
    const geometry_msgs::msg::Twist_<ContainerAllocator> & _arg)
  {
    this->current_velocity = _arg;
    return *this;
  }
  Type & set__odometry(
    const nav_msgs::msg::Odometry_<ContainerAllocator> & _arg)
  {
    this->odometry = _arg;
    return *this;
  }
  Type & set__arm_state(
    const sensor_msgs::msg::JointState_<ContainerAllocator> & _arg)
  {
    this->arm_state = _arg;
    return *this;
  }
  Type & set__arm_is_moving(
    const bool & _arg)
  {
    this->arm_is_moving = _arg;
    return *this;
  }
  Type & set__arm_pose_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->arm_pose_name = _arg;
    return *this;
  }
  Type & set__gripper_position(
    const float & _arg)
  {
    this->gripper_position = _arg;
    return *this;
  }
  Type & set__camera_mode(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->camera_mode = _arg;
    return *this;
  }
  Type & set__tracking_target(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->tracking_target = _arg;
    return *this;
  }
  Type & set__active_skills(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->active_skills = _arg;
    return *this;
  }
  Type & set__current_skill_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->current_skill_id = _arg;
    return *this;
  }
  Type & set__errors(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->errors = _arg;
    return *this;
  }
  Type & set__warnings(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->warnings = _arg;
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
    aimee_msgs::msg::RobotState_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::msg::RobotState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::msg::RobotState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::msg::RobotState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::RobotState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::RobotState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::RobotState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::RobotState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::msg::RobotState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::msg::RobotState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__msg__RobotState
    std::shared_ptr<aimee_msgs::msg::RobotState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__msg__RobotState
    std::shared_ptr<aimee_msgs::msg::RobotState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RobotState_ & other) const
  {
    if (this->robot_name != other.robot_name) {
      return false;
    }
    if (this->robot_type != other.robot_type) {
      return false;
    }
    if (this->battery_level != other.battery_level) {
      return false;
    }
    if (this->is_charging != other.is_charging) {
      return false;
    }
    if (this->power_status != other.power_status) {
      return false;
    }
    if (this->current_action != other.current_action) {
      return false;
    }
    if (this->current_velocity != other.current_velocity) {
      return false;
    }
    if (this->odometry != other.odometry) {
      return false;
    }
    if (this->arm_state != other.arm_state) {
      return false;
    }
    if (this->arm_is_moving != other.arm_is_moving) {
      return false;
    }
    if (this->arm_pose_name != other.arm_pose_name) {
      return false;
    }
    if (this->gripper_position != other.gripper_position) {
      return false;
    }
    if (this->camera_mode != other.camera_mode) {
      return false;
    }
    if (this->tracking_target != other.tracking_target) {
      return false;
    }
    if (this->active_skills != other.active_skills) {
      return false;
    }
    if (this->current_skill_id != other.current_skill_id) {
      return false;
    }
    if (this->errors != other.errors) {
      return false;
    }
    if (this->warnings != other.warnings) {
      return false;
    }
    if (this->timestamp != other.timestamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const RobotState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RobotState_

// alias to use template instance with default allocator
using RobotState =
  aimee_msgs::msg::RobotState_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__ROBOT_STATE__STRUCT_HPP_
