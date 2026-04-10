// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aimee_msgs:action/ExecuteSkill.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__ACTION__DETAIL__EXECUTE_SKILL__STRUCT_HPP_
#define AIMEE_MSGS__ACTION__DETAIL__EXECUTE_SKILL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'robot_state'
#include "aimee_msgs/msg/detail/robot_state__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__action__ExecuteSkill_Goal __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__action__ExecuteSkill_Goal __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteSkill_Goal_
{
  using Type = ExecuteSkill_Goal_<ContainerAllocator>;

  explicit ExecuteSkill_Goal_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : robot_state(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->skill_id = "";
      this->user_input = "";
      this->user_context = "";
      this->session_id = "";
    }
  }

  explicit ExecuteSkill_Goal_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : skill_id(_alloc),
    user_input(_alloc),
    robot_state(_alloc, _init),
    user_context(_alloc),
    session_id(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->skill_id = "";
      this->user_input = "";
      this->user_context = "";
      this->session_id = "";
    }
  }

  // field types and members
  using _skill_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _skill_id_type skill_id;
  using _user_input_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _user_input_type user_input;
  using _robot_state_type =
    aimee_msgs::msg::RobotState_<ContainerAllocator>;
  _robot_state_type robot_state;
  using _user_context_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _user_context_type user_context;
  using _session_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _session_id_type session_id;

  // setters for named parameter idiom
  Type & set__skill_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->skill_id = _arg;
    return *this;
  }
  Type & set__user_input(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->user_input = _arg;
    return *this;
  }
  Type & set__robot_state(
    const aimee_msgs::msg::RobotState_<ContainerAllocator> & _arg)
  {
    this->robot_state = _arg;
    return *this;
  }
  Type & set__user_context(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->user_context = _arg;
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
    aimee_msgs::action::ExecuteSkill_Goal_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::action::ExecuteSkill_Goal_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_Goal_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_Goal_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::ExecuteSkill_Goal_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::ExecuteSkill_Goal_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::ExecuteSkill_Goal_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::ExecuteSkill_Goal_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::action::ExecuteSkill_Goal_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::action::ExecuteSkill_Goal_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__action__ExecuteSkill_Goal
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_Goal_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__action__ExecuteSkill_Goal
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_Goal_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteSkill_Goal_ & other) const
  {
    if (this->skill_id != other.skill_id) {
      return false;
    }
    if (this->user_input != other.user_input) {
      return false;
    }
    if (this->robot_state != other.robot_state) {
      return false;
    }
    if (this->user_context != other.user_context) {
      return false;
    }
    if (this->session_id != other.session_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteSkill_Goal_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteSkill_Goal_

// alias to use template instance with default allocator
using ExecuteSkill_Goal =
  aimee_msgs::action::ExecuteSkill_Goal_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace aimee_msgs


// Include directives for member types
// Member 'motor_actions'
#include "aimee_msgs/msg/detail/motor_action__struct.hpp"
// Member 'camera_actions'
#include "aimee_msgs/msg/detail/camera_action__struct.hpp"
// Member 'led_actions'
#include "aimee_msgs/msg/detail/led_action__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__action__ExecuteSkill_Result __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__action__ExecuteSkill_Result __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteSkill_Result_
{
  using Type = ExecuteSkill_Result_<ContainerAllocator>;

  explicit ExecuteSkill_Result_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->response_text = "";
      this->tts_audio_path = "";
      this->error_message = "";
    }
  }

  explicit ExecuteSkill_Result_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : response_text(_alloc),
    tts_audio_path(_alloc),
    error_message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->response_text = "";
      this->tts_audio_path = "";
      this->error_message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _response_text_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _response_text_type response_text;
  using _tts_audio_path_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _tts_audio_path_type tts_audio_path;
  using _error_message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _error_message_type error_message;
  using _motor_actions_type =
    std::vector<aimee_msgs::msg::MotorAction_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<aimee_msgs::msg::MotorAction_<ContainerAllocator>>>;
  _motor_actions_type motor_actions;
  using _camera_actions_type =
    std::vector<aimee_msgs::msg::CameraAction_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<aimee_msgs::msg::CameraAction_<ContainerAllocator>>>;
  _camera_actions_type camera_actions;
  using _led_actions_type =
    std::vector<aimee_msgs::msg::LEDAction_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<aimee_msgs::msg::LEDAction_<ContainerAllocator>>>;
  _led_actions_type led_actions;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__response_text(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->response_text = _arg;
    return *this;
  }
  Type & set__tts_audio_path(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->tts_audio_path = _arg;
    return *this;
  }
  Type & set__error_message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->error_message = _arg;
    return *this;
  }
  Type & set__motor_actions(
    const std::vector<aimee_msgs::msg::MotorAction_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<aimee_msgs::msg::MotorAction_<ContainerAllocator>>> & _arg)
  {
    this->motor_actions = _arg;
    return *this;
  }
  Type & set__camera_actions(
    const std::vector<aimee_msgs::msg::CameraAction_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<aimee_msgs::msg::CameraAction_<ContainerAllocator>>> & _arg)
  {
    this->camera_actions = _arg;
    return *this;
  }
  Type & set__led_actions(
    const std::vector<aimee_msgs::msg::LEDAction_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<aimee_msgs::msg::LEDAction_<ContainerAllocator>>> & _arg)
  {
    this->led_actions = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::action::ExecuteSkill_Result_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::action::ExecuteSkill_Result_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_Result_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_Result_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::ExecuteSkill_Result_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::ExecuteSkill_Result_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::ExecuteSkill_Result_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::ExecuteSkill_Result_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::action::ExecuteSkill_Result_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::action::ExecuteSkill_Result_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__action__ExecuteSkill_Result
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_Result_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__action__ExecuteSkill_Result
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_Result_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteSkill_Result_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->response_text != other.response_text) {
      return false;
    }
    if (this->tts_audio_path != other.tts_audio_path) {
      return false;
    }
    if (this->error_message != other.error_message) {
      return false;
    }
    if (this->motor_actions != other.motor_actions) {
      return false;
    }
    if (this->camera_actions != other.camera_actions) {
      return false;
    }
    if (this->led_actions != other.led_actions) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteSkill_Result_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteSkill_Result_

// alias to use template instance with default allocator
using ExecuteSkill_Result =
  aimee_msgs::action::ExecuteSkill_Result_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace aimee_msgs


#ifndef _WIN32
# define DEPRECATED__aimee_msgs__action__ExecuteSkill_Feedback __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__action__ExecuteSkill_Feedback __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteSkill_Feedback_
{
  using Type = ExecuteSkill_Feedback_<ContainerAllocator>;

  explicit ExecuteSkill_Feedback_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = "";
      this->current_action = "";
      this->progress = 0.0f;
      this->can_cancel = false;
    }
  }

  explicit ExecuteSkill_Feedback_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : status(_alloc),
    current_action(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = "";
      this->current_action = "";
      this->progress = 0.0f;
      this->can_cancel = false;
    }
  }

  // field types and members
  using _status_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _status_type status;
  using _current_action_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _current_action_type current_action;
  using _progress_type =
    float;
  _progress_type progress;
  using _can_cancel_type =
    bool;
  _can_cancel_type can_cancel;

  // setters for named parameter idiom
  Type & set__status(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__current_action(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->current_action = _arg;
    return *this;
  }
  Type & set__progress(
    const float & _arg)
  {
    this->progress = _arg;
    return *this;
  }
  Type & set__can_cancel(
    const bool & _arg)
  {
    this->can_cancel = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::action::ExecuteSkill_Feedback_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::action::ExecuteSkill_Feedback_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_Feedback_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_Feedback_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::ExecuteSkill_Feedback_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::ExecuteSkill_Feedback_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::ExecuteSkill_Feedback_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::ExecuteSkill_Feedback_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::action::ExecuteSkill_Feedback_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::action::ExecuteSkill_Feedback_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__action__ExecuteSkill_Feedback
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_Feedback_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__action__ExecuteSkill_Feedback
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_Feedback_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteSkill_Feedback_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->current_action != other.current_action) {
      return false;
    }
    if (this->progress != other.progress) {
      return false;
    }
    if (this->can_cancel != other.can_cancel) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteSkill_Feedback_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteSkill_Feedback_

// alias to use template instance with default allocator
using ExecuteSkill_Feedback =
  aimee_msgs::action::ExecuteSkill_Feedback_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace aimee_msgs


// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'goal'
#include "aimee_msgs/action/detail/execute_skill__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__action__ExecuteSkill_SendGoal_Request __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__action__ExecuteSkill_SendGoal_Request __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteSkill_SendGoal_Request_
{
  using Type = ExecuteSkill_SendGoal_Request_<ContainerAllocator>;

  explicit ExecuteSkill_SendGoal_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    goal(_init)
  {
    (void)_init;
  }

  explicit ExecuteSkill_SendGoal_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    goal(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _goal_type =
    aimee_msgs::action::ExecuteSkill_Goal_<ContainerAllocator>;
  _goal_type goal;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__goal(
    const aimee_msgs::action::ExecuteSkill_Goal_<ContainerAllocator> & _arg)
  {
    this->goal = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::action::ExecuteSkill_SendGoal_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::action::ExecuteSkill_SendGoal_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_SendGoal_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_SendGoal_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::ExecuteSkill_SendGoal_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::ExecuteSkill_SendGoal_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::ExecuteSkill_SendGoal_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::ExecuteSkill_SendGoal_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::action::ExecuteSkill_SendGoal_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::action::ExecuteSkill_SendGoal_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__action__ExecuteSkill_SendGoal_Request
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_SendGoal_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__action__ExecuteSkill_SendGoal_Request
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_SendGoal_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteSkill_SendGoal_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->goal != other.goal) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteSkill_SendGoal_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteSkill_SendGoal_Request_

// alias to use template instance with default allocator
using ExecuteSkill_SendGoal_Request =
  aimee_msgs::action::ExecuteSkill_SendGoal_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace aimee_msgs


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__action__ExecuteSkill_SendGoal_Response __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__action__ExecuteSkill_SendGoal_Response __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteSkill_SendGoal_Response_
{
  using Type = ExecuteSkill_SendGoal_Response_<ContainerAllocator>;

  explicit ExecuteSkill_SendGoal_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  explicit ExecuteSkill_SendGoal_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  // field types and members
  using _accepted_type =
    bool;
  _accepted_type accepted;
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;

  // setters for named parameter idiom
  Type & set__accepted(
    const bool & _arg)
  {
    this->accepted = _arg;
    return *this;
  }
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::action::ExecuteSkill_SendGoal_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::action::ExecuteSkill_SendGoal_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_SendGoal_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_SendGoal_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::ExecuteSkill_SendGoal_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::ExecuteSkill_SendGoal_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::ExecuteSkill_SendGoal_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::ExecuteSkill_SendGoal_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::action::ExecuteSkill_SendGoal_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::action::ExecuteSkill_SendGoal_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__action__ExecuteSkill_SendGoal_Response
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_SendGoal_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__action__ExecuteSkill_SendGoal_Response
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_SendGoal_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteSkill_SendGoal_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteSkill_SendGoal_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteSkill_SendGoal_Response_

// alias to use template instance with default allocator
using ExecuteSkill_SendGoal_Response =
  aimee_msgs::action::ExecuteSkill_SendGoal_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace aimee_msgs

namespace aimee_msgs
{

namespace action
{

struct ExecuteSkill_SendGoal
{
  using Request = aimee_msgs::action::ExecuteSkill_SendGoal_Request;
  using Response = aimee_msgs::action::ExecuteSkill_SendGoal_Response;
};

}  // namespace action

}  // namespace aimee_msgs


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__action__ExecuteSkill_GetResult_Request __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__action__ExecuteSkill_GetResult_Request __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteSkill_GetResult_Request_
{
  using Type = ExecuteSkill_GetResult_Request_<ContainerAllocator>;

  explicit ExecuteSkill_GetResult_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init)
  {
    (void)_init;
  }

  explicit ExecuteSkill_GetResult_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::action::ExecuteSkill_GetResult_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::action::ExecuteSkill_GetResult_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_GetResult_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_GetResult_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::ExecuteSkill_GetResult_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::ExecuteSkill_GetResult_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::ExecuteSkill_GetResult_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::ExecuteSkill_GetResult_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::action::ExecuteSkill_GetResult_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::action::ExecuteSkill_GetResult_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__action__ExecuteSkill_GetResult_Request
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_GetResult_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__action__ExecuteSkill_GetResult_Request
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_GetResult_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteSkill_GetResult_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteSkill_GetResult_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteSkill_GetResult_Request_

// alias to use template instance with default allocator
using ExecuteSkill_GetResult_Request =
  aimee_msgs::action::ExecuteSkill_GetResult_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace aimee_msgs


// Include directives for member types
// Member 'result'
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__action__ExecuteSkill_GetResult_Response __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__action__ExecuteSkill_GetResult_Response __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteSkill_GetResult_Response_
{
  using Type = ExecuteSkill_GetResult_Response_<ContainerAllocator>;

  explicit ExecuteSkill_GetResult_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  explicit ExecuteSkill_GetResult_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  // field types and members
  using _status_type =
    int8_t;
  _status_type status;
  using _result_type =
    aimee_msgs::action::ExecuteSkill_Result_<ContainerAllocator>;
  _result_type result;

  // setters for named parameter idiom
  Type & set__status(
    const int8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__result(
    const aimee_msgs::action::ExecuteSkill_Result_<ContainerAllocator> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::action::ExecuteSkill_GetResult_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::action::ExecuteSkill_GetResult_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_GetResult_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_GetResult_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::ExecuteSkill_GetResult_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::ExecuteSkill_GetResult_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::ExecuteSkill_GetResult_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::ExecuteSkill_GetResult_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::action::ExecuteSkill_GetResult_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::action::ExecuteSkill_GetResult_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__action__ExecuteSkill_GetResult_Response
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_GetResult_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__action__ExecuteSkill_GetResult_Response
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_GetResult_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteSkill_GetResult_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteSkill_GetResult_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteSkill_GetResult_Response_

// alias to use template instance with default allocator
using ExecuteSkill_GetResult_Response =
  aimee_msgs::action::ExecuteSkill_GetResult_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace aimee_msgs

namespace aimee_msgs
{

namespace action
{

struct ExecuteSkill_GetResult
{
  using Request = aimee_msgs::action::ExecuteSkill_GetResult_Request;
  using Response = aimee_msgs::action::ExecuteSkill_GetResult_Response;
};

}  // namespace action

}  // namespace aimee_msgs


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'feedback'
// already included above
// #include "aimee_msgs/action/detail/execute_skill__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__action__ExecuteSkill_FeedbackMessage __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__action__ExecuteSkill_FeedbackMessage __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteSkill_FeedbackMessage_
{
  using Type = ExecuteSkill_FeedbackMessage_<ContainerAllocator>;

  explicit ExecuteSkill_FeedbackMessage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    feedback(_init)
  {
    (void)_init;
  }

  explicit ExecuteSkill_FeedbackMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    feedback(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _feedback_type =
    aimee_msgs::action::ExecuteSkill_Feedback_<ContainerAllocator>;
  _feedback_type feedback;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__feedback(
    const aimee_msgs::action::ExecuteSkill_Feedback_<ContainerAllocator> & _arg)
  {
    this->feedback = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::action::ExecuteSkill_FeedbackMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::action::ExecuteSkill_FeedbackMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_FeedbackMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_FeedbackMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::ExecuteSkill_FeedbackMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::ExecuteSkill_FeedbackMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::ExecuteSkill_FeedbackMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::ExecuteSkill_FeedbackMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::action::ExecuteSkill_FeedbackMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::action::ExecuteSkill_FeedbackMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__action__ExecuteSkill_FeedbackMessage
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_FeedbackMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__action__ExecuteSkill_FeedbackMessage
    std::shared_ptr<aimee_msgs::action::ExecuteSkill_FeedbackMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteSkill_FeedbackMessage_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->feedback != other.feedback) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteSkill_FeedbackMessage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteSkill_FeedbackMessage_

// alias to use template instance with default allocator
using ExecuteSkill_FeedbackMessage =
  aimee_msgs::action::ExecuteSkill_FeedbackMessage_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace aimee_msgs

#include "action_msgs/srv/cancel_goal.hpp"
#include "action_msgs/msg/goal_info.hpp"
#include "action_msgs/msg/goal_status_array.hpp"

namespace aimee_msgs
{

namespace action
{

struct ExecuteSkill
{
  /// The goal message defined in the action definition.
  using Goal = aimee_msgs::action::ExecuteSkill_Goal;
  /// The result message defined in the action definition.
  using Result = aimee_msgs::action::ExecuteSkill_Result;
  /// The feedback message defined in the action definition.
  using Feedback = aimee_msgs::action::ExecuteSkill_Feedback;

  struct Impl
  {
    /// The send_goal service using a wrapped version of the goal message as a request.
    using SendGoalService = aimee_msgs::action::ExecuteSkill_SendGoal;
    /// The get_result service using a wrapped version of the result message as a response.
    using GetResultService = aimee_msgs::action::ExecuteSkill_GetResult;
    /// The feedback message with generic fields which wraps the feedback message.
    using FeedbackMessage = aimee_msgs::action::ExecuteSkill_FeedbackMessage;

    /// The generic service to cancel a goal.
    using CancelGoalService = action_msgs::srv::CancelGoal;
    /// The generic message for the status of a goal.
    using GoalStatusMessage = action_msgs::msg::GoalStatusArray;
  };
};

typedef struct ExecuteSkill ExecuteSkill;

}  // namespace action

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__ACTION__DETAIL__EXECUTE_SKILL__STRUCT_HPP_
