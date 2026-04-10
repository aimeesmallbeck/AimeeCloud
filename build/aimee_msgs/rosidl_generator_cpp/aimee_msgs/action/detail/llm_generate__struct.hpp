// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aimee_msgs:action/LLMGenerate.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__ACTION__DETAIL__LLM_GENERATE__STRUCT_HPP_
#define AIMEE_MSGS__ACTION__DETAIL__LLM_GENERATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__aimee_msgs__action__LLMGenerate_Goal __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__action__LLMGenerate_Goal __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct LLMGenerate_Goal_
{
  using Type = LLMGenerate_Goal_<ContainerAllocator>;

  explicit LLMGenerate_Goal_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->prompt = "";
      this->system_context = "";
      this->max_tokens = 0l;
      this->temperature = 0.0f;
      this->stream = false;
      this->session_id = "";
    }
  }

  explicit LLMGenerate_Goal_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : prompt(_alloc),
    system_context(_alloc),
    session_id(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->prompt = "";
      this->system_context = "";
      this->max_tokens = 0l;
      this->temperature = 0.0f;
      this->stream = false;
      this->session_id = "";
    }
  }

  // field types and members
  using _prompt_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _prompt_type prompt;
  using _system_context_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _system_context_type system_context;
  using _max_tokens_type =
    int32_t;
  _max_tokens_type max_tokens;
  using _temperature_type =
    float;
  _temperature_type temperature;
  using _stream_type =
    bool;
  _stream_type stream;
  using _session_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _session_id_type session_id;

  // setters for named parameter idiom
  Type & set__prompt(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->prompt = _arg;
    return *this;
  }
  Type & set__system_context(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->system_context = _arg;
    return *this;
  }
  Type & set__max_tokens(
    const int32_t & _arg)
  {
    this->max_tokens = _arg;
    return *this;
  }
  Type & set__temperature(
    const float & _arg)
  {
    this->temperature = _arg;
    return *this;
  }
  Type & set__stream(
    const bool & _arg)
  {
    this->stream = _arg;
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
    aimee_msgs::action::LLMGenerate_Goal_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::action::LLMGenerate_Goal_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::action::LLMGenerate_Goal_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::action::LLMGenerate_Goal_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::LLMGenerate_Goal_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::LLMGenerate_Goal_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::LLMGenerate_Goal_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::LLMGenerate_Goal_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::action::LLMGenerate_Goal_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::action::LLMGenerate_Goal_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__action__LLMGenerate_Goal
    std::shared_ptr<aimee_msgs::action::LLMGenerate_Goal_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__action__LLMGenerate_Goal
    std::shared_ptr<aimee_msgs::action::LLMGenerate_Goal_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LLMGenerate_Goal_ & other) const
  {
    if (this->prompt != other.prompt) {
      return false;
    }
    if (this->system_context != other.system_context) {
      return false;
    }
    if (this->max_tokens != other.max_tokens) {
      return false;
    }
    if (this->temperature != other.temperature) {
      return false;
    }
    if (this->stream != other.stream) {
      return false;
    }
    if (this->session_id != other.session_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const LLMGenerate_Goal_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LLMGenerate_Goal_

// alias to use template instance with default allocator
using LLMGenerate_Goal =
  aimee_msgs::action::LLMGenerate_Goal_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace aimee_msgs


#ifndef _WIN32
# define DEPRECATED__aimee_msgs__action__LLMGenerate_Result __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__action__LLMGenerate_Result __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct LLMGenerate_Result_
{
  using Type = LLMGenerate_Result_<ContainerAllocator>;

  explicit LLMGenerate_Result_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->response = "";
      this->success = false;
      this->error_message = "";
      this->generation_time = 0.0f;
      this->tokens_generated = 0l;
      this->tokens_input = 0l;
    }
  }

  explicit LLMGenerate_Result_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : response(_alloc),
    error_message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->response = "";
      this->success = false;
      this->error_message = "";
      this->generation_time = 0.0f;
      this->tokens_generated = 0l;
      this->tokens_input = 0l;
    }
  }

  // field types and members
  using _response_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _response_type response;
  using _success_type =
    bool;
  _success_type success;
  using _error_message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _error_message_type error_message;
  using _generation_time_type =
    float;
  _generation_time_type generation_time;
  using _tokens_generated_type =
    int32_t;
  _tokens_generated_type tokens_generated;
  using _tokens_input_type =
    int32_t;
  _tokens_input_type tokens_input;

  // setters for named parameter idiom
  Type & set__response(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->response = _arg;
    return *this;
  }
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__error_message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->error_message = _arg;
    return *this;
  }
  Type & set__generation_time(
    const float & _arg)
  {
    this->generation_time = _arg;
    return *this;
  }
  Type & set__tokens_generated(
    const int32_t & _arg)
  {
    this->tokens_generated = _arg;
    return *this;
  }
  Type & set__tokens_input(
    const int32_t & _arg)
  {
    this->tokens_input = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::action::LLMGenerate_Result_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::action::LLMGenerate_Result_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::action::LLMGenerate_Result_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::action::LLMGenerate_Result_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::LLMGenerate_Result_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::LLMGenerate_Result_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::LLMGenerate_Result_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::LLMGenerate_Result_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::action::LLMGenerate_Result_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::action::LLMGenerate_Result_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__action__LLMGenerate_Result
    std::shared_ptr<aimee_msgs::action::LLMGenerate_Result_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__action__LLMGenerate_Result
    std::shared_ptr<aimee_msgs::action::LLMGenerate_Result_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LLMGenerate_Result_ & other) const
  {
    if (this->response != other.response) {
      return false;
    }
    if (this->success != other.success) {
      return false;
    }
    if (this->error_message != other.error_message) {
      return false;
    }
    if (this->generation_time != other.generation_time) {
      return false;
    }
    if (this->tokens_generated != other.tokens_generated) {
      return false;
    }
    if (this->tokens_input != other.tokens_input) {
      return false;
    }
    return true;
  }
  bool operator!=(const LLMGenerate_Result_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LLMGenerate_Result_

// alias to use template instance with default allocator
using LLMGenerate_Result =
  aimee_msgs::action::LLMGenerate_Result_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace aimee_msgs


#ifndef _WIN32
# define DEPRECATED__aimee_msgs__action__LLMGenerate_Feedback __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__action__LLMGenerate_Feedback __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct LLMGenerate_Feedback_
{
  using Type = LLMGenerate_Feedback_<ContainerAllocator>;

  explicit LLMGenerate_Feedback_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->partial_response = "";
      this->tokens_generated = 0l;
      this->tokens_total = 0l;
      this->is_complete = false;
      this->current_word = "";
    }
  }

  explicit LLMGenerate_Feedback_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : partial_response(_alloc),
    current_word(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->partial_response = "";
      this->tokens_generated = 0l;
      this->tokens_total = 0l;
      this->is_complete = false;
      this->current_word = "";
    }
  }

  // field types and members
  using _partial_response_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _partial_response_type partial_response;
  using _tokens_generated_type =
    int32_t;
  _tokens_generated_type tokens_generated;
  using _tokens_total_type =
    int32_t;
  _tokens_total_type tokens_total;
  using _is_complete_type =
    bool;
  _is_complete_type is_complete;
  using _current_word_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _current_word_type current_word;

  // setters for named parameter idiom
  Type & set__partial_response(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->partial_response = _arg;
    return *this;
  }
  Type & set__tokens_generated(
    const int32_t & _arg)
  {
    this->tokens_generated = _arg;
    return *this;
  }
  Type & set__tokens_total(
    const int32_t & _arg)
  {
    this->tokens_total = _arg;
    return *this;
  }
  Type & set__is_complete(
    const bool & _arg)
  {
    this->is_complete = _arg;
    return *this;
  }
  Type & set__current_word(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->current_word = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::action::LLMGenerate_Feedback_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::action::LLMGenerate_Feedback_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::action::LLMGenerate_Feedback_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::action::LLMGenerate_Feedback_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::LLMGenerate_Feedback_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::LLMGenerate_Feedback_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::LLMGenerate_Feedback_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::LLMGenerate_Feedback_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::action::LLMGenerate_Feedback_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::action::LLMGenerate_Feedback_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__action__LLMGenerate_Feedback
    std::shared_ptr<aimee_msgs::action::LLMGenerate_Feedback_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__action__LLMGenerate_Feedback
    std::shared_ptr<aimee_msgs::action::LLMGenerate_Feedback_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LLMGenerate_Feedback_ & other) const
  {
    if (this->partial_response != other.partial_response) {
      return false;
    }
    if (this->tokens_generated != other.tokens_generated) {
      return false;
    }
    if (this->tokens_total != other.tokens_total) {
      return false;
    }
    if (this->is_complete != other.is_complete) {
      return false;
    }
    if (this->current_word != other.current_word) {
      return false;
    }
    return true;
  }
  bool operator!=(const LLMGenerate_Feedback_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LLMGenerate_Feedback_

// alias to use template instance with default allocator
using LLMGenerate_Feedback =
  aimee_msgs::action::LLMGenerate_Feedback_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace aimee_msgs


// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'goal'
#include "aimee_msgs/action/detail/llm_generate__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__action__LLMGenerate_SendGoal_Request __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__action__LLMGenerate_SendGoal_Request __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct LLMGenerate_SendGoal_Request_
{
  using Type = LLMGenerate_SendGoal_Request_<ContainerAllocator>;

  explicit LLMGenerate_SendGoal_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    goal(_init)
  {
    (void)_init;
  }

  explicit LLMGenerate_SendGoal_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    aimee_msgs::action::LLMGenerate_Goal_<ContainerAllocator>;
  _goal_type goal;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__goal(
    const aimee_msgs::action::LLMGenerate_Goal_<ContainerAllocator> & _arg)
  {
    this->goal = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::action::LLMGenerate_SendGoal_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::action::LLMGenerate_SendGoal_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::action::LLMGenerate_SendGoal_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::action::LLMGenerate_SendGoal_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::LLMGenerate_SendGoal_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::LLMGenerate_SendGoal_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::LLMGenerate_SendGoal_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::LLMGenerate_SendGoal_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::action::LLMGenerate_SendGoal_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::action::LLMGenerate_SendGoal_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__action__LLMGenerate_SendGoal_Request
    std::shared_ptr<aimee_msgs::action::LLMGenerate_SendGoal_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__action__LLMGenerate_SendGoal_Request
    std::shared_ptr<aimee_msgs::action::LLMGenerate_SendGoal_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LLMGenerate_SendGoal_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->goal != other.goal) {
      return false;
    }
    return true;
  }
  bool operator!=(const LLMGenerate_SendGoal_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LLMGenerate_SendGoal_Request_

// alias to use template instance with default allocator
using LLMGenerate_SendGoal_Request =
  aimee_msgs::action::LLMGenerate_SendGoal_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace aimee_msgs


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__action__LLMGenerate_SendGoal_Response __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__action__LLMGenerate_SendGoal_Response __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct LLMGenerate_SendGoal_Response_
{
  using Type = LLMGenerate_SendGoal_Response_<ContainerAllocator>;

  explicit LLMGenerate_SendGoal_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  explicit LLMGenerate_SendGoal_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    aimee_msgs::action::LLMGenerate_SendGoal_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::action::LLMGenerate_SendGoal_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::action::LLMGenerate_SendGoal_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::action::LLMGenerate_SendGoal_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::LLMGenerate_SendGoal_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::LLMGenerate_SendGoal_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::LLMGenerate_SendGoal_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::LLMGenerate_SendGoal_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::action::LLMGenerate_SendGoal_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::action::LLMGenerate_SendGoal_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__action__LLMGenerate_SendGoal_Response
    std::shared_ptr<aimee_msgs::action::LLMGenerate_SendGoal_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__action__LLMGenerate_SendGoal_Response
    std::shared_ptr<aimee_msgs::action::LLMGenerate_SendGoal_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LLMGenerate_SendGoal_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const LLMGenerate_SendGoal_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LLMGenerate_SendGoal_Response_

// alias to use template instance with default allocator
using LLMGenerate_SendGoal_Response =
  aimee_msgs::action::LLMGenerate_SendGoal_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace aimee_msgs

namespace aimee_msgs
{

namespace action
{

struct LLMGenerate_SendGoal
{
  using Request = aimee_msgs::action::LLMGenerate_SendGoal_Request;
  using Response = aimee_msgs::action::LLMGenerate_SendGoal_Response;
};

}  // namespace action

}  // namespace aimee_msgs


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__action__LLMGenerate_GetResult_Request __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__action__LLMGenerate_GetResult_Request __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct LLMGenerate_GetResult_Request_
{
  using Type = LLMGenerate_GetResult_Request_<ContainerAllocator>;

  explicit LLMGenerate_GetResult_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init)
  {
    (void)_init;
  }

  explicit LLMGenerate_GetResult_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    aimee_msgs::action::LLMGenerate_GetResult_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::action::LLMGenerate_GetResult_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::action::LLMGenerate_GetResult_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::action::LLMGenerate_GetResult_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::LLMGenerate_GetResult_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::LLMGenerate_GetResult_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::LLMGenerate_GetResult_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::LLMGenerate_GetResult_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::action::LLMGenerate_GetResult_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::action::LLMGenerate_GetResult_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__action__LLMGenerate_GetResult_Request
    std::shared_ptr<aimee_msgs::action::LLMGenerate_GetResult_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__action__LLMGenerate_GetResult_Request
    std::shared_ptr<aimee_msgs::action::LLMGenerate_GetResult_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LLMGenerate_GetResult_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const LLMGenerate_GetResult_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LLMGenerate_GetResult_Request_

// alias to use template instance with default allocator
using LLMGenerate_GetResult_Request =
  aimee_msgs::action::LLMGenerate_GetResult_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace aimee_msgs


// Include directives for member types
// Member 'result'
// already included above
// #include "aimee_msgs/action/detail/llm_generate__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__action__LLMGenerate_GetResult_Response __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__action__LLMGenerate_GetResult_Response __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct LLMGenerate_GetResult_Response_
{
  using Type = LLMGenerate_GetResult_Response_<ContainerAllocator>;

  explicit LLMGenerate_GetResult_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  explicit LLMGenerate_GetResult_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    aimee_msgs::action::LLMGenerate_Result_<ContainerAllocator>;
  _result_type result;

  // setters for named parameter idiom
  Type & set__status(
    const int8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__result(
    const aimee_msgs::action::LLMGenerate_Result_<ContainerAllocator> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::action::LLMGenerate_GetResult_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::action::LLMGenerate_GetResult_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::action::LLMGenerate_GetResult_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::action::LLMGenerate_GetResult_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::LLMGenerate_GetResult_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::LLMGenerate_GetResult_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::LLMGenerate_GetResult_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::LLMGenerate_GetResult_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::action::LLMGenerate_GetResult_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::action::LLMGenerate_GetResult_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__action__LLMGenerate_GetResult_Response
    std::shared_ptr<aimee_msgs::action::LLMGenerate_GetResult_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__action__LLMGenerate_GetResult_Response
    std::shared_ptr<aimee_msgs::action::LLMGenerate_GetResult_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LLMGenerate_GetResult_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const LLMGenerate_GetResult_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LLMGenerate_GetResult_Response_

// alias to use template instance with default allocator
using LLMGenerate_GetResult_Response =
  aimee_msgs::action::LLMGenerate_GetResult_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace aimee_msgs

namespace aimee_msgs
{

namespace action
{

struct LLMGenerate_GetResult
{
  using Request = aimee_msgs::action::LLMGenerate_GetResult_Request;
  using Response = aimee_msgs::action::LLMGenerate_GetResult_Response;
};

}  // namespace action

}  // namespace aimee_msgs


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'feedback'
// already included above
// #include "aimee_msgs/action/detail/llm_generate__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__action__LLMGenerate_FeedbackMessage __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__action__LLMGenerate_FeedbackMessage __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct LLMGenerate_FeedbackMessage_
{
  using Type = LLMGenerate_FeedbackMessage_<ContainerAllocator>;

  explicit LLMGenerate_FeedbackMessage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    feedback(_init)
  {
    (void)_init;
  }

  explicit LLMGenerate_FeedbackMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    aimee_msgs::action::LLMGenerate_Feedback_<ContainerAllocator>;
  _feedback_type feedback;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__feedback(
    const aimee_msgs::action::LLMGenerate_Feedback_<ContainerAllocator> & _arg)
  {
    this->feedback = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::action::LLMGenerate_FeedbackMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::action::LLMGenerate_FeedbackMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::action::LLMGenerate_FeedbackMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::action::LLMGenerate_FeedbackMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::LLMGenerate_FeedbackMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::LLMGenerate_FeedbackMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::action::LLMGenerate_FeedbackMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::action::LLMGenerate_FeedbackMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::action::LLMGenerate_FeedbackMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::action::LLMGenerate_FeedbackMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__action__LLMGenerate_FeedbackMessage
    std::shared_ptr<aimee_msgs::action::LLMGenerate_FeedbackMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__action__LLMGenerate_FeedbackMessage
    std::shared_ptr<aimee_msgs::action::LLMGenerate_FeedbackMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LLMGenerate_FeedbackMessage_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->feedback != other.feedback) {
      return false;
    }
    return true;
  }
  bool operator!=(const LLMGenerate_FeedbackMessage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LLMGenerate_FeedbackMessage_

// alias to use template instance with default allocator
using LLMGenerate_FeedbackMessage =
  aimee_msgs::action::LLMGenerate_FeedbackMessage_<std::allocator<void>>;

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

struct LLMGenerate
{
  /// The goal message defined in the action definition.
  using Goal = aimee_msgs::action::LLMGenerate_Goal;
  /// The result message defined in the action definition.
  using Result = aimee_msgs::action::LLMGenerate_Result;
  /// The feedback message defined in the action definition.
  using Feedback = aimee_msgs::action::LLMGenerate_Feedback;

  struct Impl
  {
    /// The send_goal service using a wrapped version of the goal message as a request.
    using SendGoalService = aimee_msgs::action::LLMGenerate_SendGoal;
    /// The get_result service using a wrapped version of the result message as a response.
    using GetResultService = aimee_msgs::action::LLMGenerate_GetResult;
    /// The feedback message with generic fields which wraps the feedback message.
    using FeedbackMessage = aimee_msgs::action::LLMGenerate_FeedbackMessage;

    /// The generic service to cancel a goal.
    using CancelGoalService = action_msgs::srv::CancelGoal;
    /// The generic message for the status of a goal.
    using GoalStatusMessage = action_msgs::msg::GoalStatusArray;
  };
};

typedef struct LLMGenerate LLMGenerate;

}  // namespace action

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__ACTION__DETAIL__LLM_GENERATE__STRUCT_HPP_
