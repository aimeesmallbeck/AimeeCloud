// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aimee_msgs:action/LLMGenerate.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__ACTION__DETAIL__LLM_GENERATE__BUILDER_HPP_
#define AIMEE_MSGS__ACTION__DETAIL__LLM_GENERATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aimee_msgs/action/detail/llm_generate__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aimee_msgs
{

namespace action
{

namespace builder
{

class Init_LLMGenerate_Goal_session_id
{
public:
  explicit Init_LLMGenerate_Goal_session_id(::aimee_msgs::action::LLMGenerate_Goal & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::action::LLMGenerate_Goal session_id(::aimee_msgs::action::LLMGenerate_Goal::_session_id_type arg)
  {
    msg_.session_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Goal msg_;
};

class Init_LLMGenerate_Goal_stream
{
public:
  explicit Init_LLMGenerate_Goal_stream(::aimee_msgs::action::LLMGenerate_Goal & msg)
  : msg_(msg)
  {}
  Init_LLMGenerate_Goal_session_id stream(::aimee_msgs::action::LLMGenerate_Goal::_stream_type arg)
  {
    msg_.stream = std::move(arg);
    return Init_LLMGenerate_Goal_session_id(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Goal msg_;
};

class Init_LLMGenerate_Goal_temperature
{
public:
  explicit Init_LLMGenerate_Goal_temperature(::aimee_msgs::action::LLMGenerate_Goal & msg)
  : msg_(msg)
  {}
  Init_LLMGenerate_Goal_stream temperature(::aimee_msgs::action::LLMGenerate_Goal::_temperature_type arg)
  {
    msg_.temperature = std::move(arg);
    return Init_LLMGenerate_Goal_stream(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Goal msg_;
};

class Init_LLMGenerate_Goal_max_tokens
{
public:
  explicit Init_LLMGenerate_Goal_max_tokens(::aimee_msgs::action::LLMGenerate_Goal & msg)
  : msg_(msg)
  {}
  Init_LLMGenerate_Goal_temperature max_tokens(::aimee_msgs::action::LLMGenerate_Goal::_max_tokens_type arg)
  {
    msg_.max_tokens = std::move(arg);
    return Init_LLMGenerate_Goal_temperature(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Goal msg_;
};

class Init_LLMGenerate_Goal_system_context
{
public:
  explicit Init_LLMGenerate_Goal_system_context(::aimee_msgs::action::LLMGenerate_Goal & msg)
  : msg_(msg)
  {}
  Init_LLMGenerate_Goal_max_tokens system_context(::aimee_msgs::action::LLMGenerate_Goal::_system_context_type arg)
  {
    msg_.system_context = std::move(arg);
    return Init_LLMGenerate_Goal_max_tokens(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Goal msg_;
};

class Init_LLMGenerate_Goal_prompt
{
public:
  Init_LLMGenerate_Goal_prompt()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LLMGenerate_Goal_system_context prompt(::aimee_msgs::action::LLMGenerate_Goal::_prompt_type arg)
  {
    msg_.prompt = std::move(arg);
    return Init_LLMGenerate_Goal_system_context(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::action::LLMGenerate_Goal>()
{
  return aimee_msgs::action::builder::Init_LLMGenerate_Goal_prompt();
}

}  // namespace aimee_msgs


namespace aimee_msgs
{

namespace action
{

namespace builder
{

class Init_LLMGenerate_Result_tokens_input
{
public:
  explicit Init_LLMGenerate_Result_tokens_input(::aimee_msgs::action::LLMGenerate_Result & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::action::LLMGenerate_Result tokens_input(::aimee_msgs::action::LLMGenerate_Result::_tokens_input_type arg)
  {
    msg_.tokens_input = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Result msg_;
};

class Init_LLMGenerate_Result_tokens_generated
{
public:
  explicit Init_LLMGenerate_Result_tokens_generated(::aimee_msgs::action::LLMGenerate_Result & msg)
  : msg_(msg)
  {}
  Init_LLMGenerate_Result_tokens_input tokens_generated(::aimee_msgs::action::LLMGenerate_Result::_tokens_generated_type arg)
  {
    msg_.tokens_generated = std::move(arg);
    return Init_LLMGenerate_Result_tokens_input(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Result msg_;
};

class Init_LLMGenerate_Result_generation_time
{
public:
  explicit Init_LLMGenerate_Result_generation_time(::aimee_msgs::action::LLMGenerate_Result & msg)
  : msg_(msg)
  {}
  Init_LLMGenerate_Result_tokens_generated generation_time(::aimee_msgs::action::LLMGenerate_Result::_generation_time_type arg)
  {
    msg_.generation_time = std::move(arg);
    return Init_LLMGenerate_Result_tokens_generated(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Result msg_;
};

class Init_LLMGenerate_Result_error_message
{
public:
  explicit Init_LLMGenerate_Result_error_message(::aimee_msgs::action::LLMGenerate_Result & msg)
  : msg_(msg)
  {}
  Init_LLMGenerate_Result_generation_time error_message(::aimee_msgs::action::LLMGenerate_Result::_error_message_type arg)
  {
    msg_.error_message = std::move(arg);
    return Init_LLMGenerate_Result_generation_time(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Result msg_;
};

class Init_LLMGenerate_Result_success
{
public:
  explicit Init_LLMGenerate_Result_success(::aimee_msgs::action::LLMGenerate_Result & msg)
  : msg_(msg)
  {}
  Init_LLMGenerate_Result_error_message success(::aimee_msgs::action::LLMGenerate_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_LLMGenerate_Result_error_message(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Result msg_;
};

class Init_LLMGenerate_Result_response
{
public:
  Init_LLMGenerate_Result_response()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LLMGenerate_Result_success response(::aimee_msgs::action::LLMGenerate_Result::_response_type arg)
  {
    msg_.response = std::move(arg);
    return Init_LLMGenerate_Result_success(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::action::LLMGenerate_Result>()
{
  return aimee_msgs::action::builder::Init_LLMGenerate_Result_response();
}

}  // namespace aimee_msgs


namespace aimee_msgs
{

namespace action
{

namespace builder
{

class Init_LLMGenerate_Feedback_current_word
{
public:
  explicit Init_LLMGenerate_Feedback_current_word(::aimee_msgs::action::LLMGenerate_Feedback & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::action::LLMGenerate_Feedback current_word(::aimee_msgs::action::LLMGenerate_Feedback::_current_word_type arg)
  {
    msg_.current_word = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Feedback msg_;
};

class Init_LLMGenerate_Feedback_is_complete
{
public:
  explicit Init_LLMGenerate_Feedback_is_complete(::aimee_msgs::action::LLMGenerate_Feedback & msg)
  : msg_(msg)
  {}
  Init_LLMGenerate_Feedback_current_word is_complete(::aimee_msgs::action::LLMGenerate_Feedback::_is_complete_type arg)
  {
    msg_.is_complete = std::move(arg);
    return Init_LLMGenerate_Feedback_current_word(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Feedback msg_;
};

class Init_LLMGenerate_Feedback_tokens_total
{
public:
  explicit Init_LLMGenerate_Feedback_tokens_total(::aimee_msgs::action::LLMGenerate_Feedback & msg)
  : msg_(msg)
  {}
  Init_LLMGenerate_Feedback_is_complete tokens_total(::aimee_msgs::action::LLMGenerate_Feedback::_tokens_total_type arg)
  {
    msg_.tokens_total = std::move(arg);
    return Init_LLMGenerate_Feedback_is_complete(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Feedback msg_;
};

class Init_LLMGenerate_Feedback_tokens_generated
{
public:
  explicit Init_LLMGenerate_Feedback_tokens_generated(::aimee_msgs::action::LLMGenerate_Feedback & msg)
  : msg_(msg)
  {}
  Init_LLMGenerate_Feedback_tokens_total tokens_generated(::aimee_msgs::action::LLMGenerate_Feedback::_tokens_generated_type arg)
  {
    msg_.tokens_generated = std::move(arg);
    return Init_LLMGenerate_Feedback_tokens_total(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Feedback msg_;
};

class Init_LLMGenerate_Feedback_partial_response
{
public:
  Init_LLMGenerate_Feedback_partial_response()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LLMGenerate_Feedback_tokens_generated partial_response(::aimee_msgs::action::LLMGenerate_Feedback::_partial_response_type arg)
  {
    msg_.partial_response = std::move(arg);
    return Init_LLMGenerate_Feedback_tokens_generated(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::action::LLMGenerate_Feedback>()
{
  return aimee_msgs::action::builder::Init_LLMGenerate_Feedback_partial_response();
}

}  // namespace aimee_msgs


namespace aimee_msgs
{

namespace action
{

namespace builder
{

class Init_LLMGenerate_SendGoal_Request_goal
{
public:
  explicit Init_LLMGenerate_SendGoal_Request_goal(::aimee_msgs::action::LLMGenerate_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::action::LLMGenerate_SendGoal_Request goal(::aimee_msgs::action::LLMGenerate_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_SendGoal_Request msg_;
};

class Init_LLMGenerate_SendGoal_Request_goal_id
{
public:
  Init_LLMGenerate_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LLMGenerate_SendGoal_Request_goal goal_id(::aimee_msgs::action::LLMGenerate_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_LLMGenerate_SendGoal_Request_goal(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::action::LLMGenerate_SendGoal_Request>()
{
  return aimee_msgs::action::builder::Init_LLMGenerate_SendGoal_Request_goal_id();
}

}  // namespace aimee_msgs


namespace aimee_msgs
{

namespace action
{

namespace builder
{

class Init_LLMGenerate_SendGoal_Response_stamp
{
public:
  explicit Init_LLMGenerate_SendGoal_Response_stamp(::aimee_msgs::action::LLMGenerate_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::action::LLMGenerate_SendGoal_Response stamp(::aimee_msgs::action::LLMGenerate_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_SendGoal_Response msg_;
};

class Init_LLMGenerate_SendGoal_Response_accepted
{
public:
  Init_LLMGenerate_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LLMGenerate_SendGoal_Response_stamp accepted(::aimee_msgs::action::LLMGenerate_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_LLMGenerate_SendGoal_Response_stamp(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::action::LLMGenerate_SendGoal_Response>()
{
  return aimee_msgs::action::builder::Init_LLMGenerate_SendGoal_Response_accepted();
}

}  // namespace aimee_msgs


namespace aimee_msgs
{

namespace action
{

namespace builder
{

class Init_LLMGenerate_GetResult_Request_goal_id
{
public:
  Init_LLMGenerate_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aimee_msgs::action::LLMGenerate_GetResult_Request goal_id(::aimee_msgs::action::LLMGenerate_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::action::LLMGenerate_GetResult_Request>()
{
  return aimee_msgs::action::builder::Init_LLMGenerate_GetResult_Request_goal_id();
}

}  // namespace aimee_msgs


namespace aimee_msgs
{

namespace action
{

namespace builder
{

class Init_LLMGenerate_GetResult_Response_result
{
public:
  explicit Init_LLMGenerate_GetResult_Response_result(::aimee_msgs::action::LLMGenerate_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::action::LLMGenerate_GetResult_Response result(::aimee_msgs::action::LLMGenerate_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_GetResult_Response msg_;
};

class Init_LLMGenerate_GetResult_Response_status
{
public:
  Init_LLMGenerate_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LLMGenerate_GetResult_Response_result status(::aimee_msgs::action::LLMGenerate_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_LLMGenerate_GetResult_Response_result(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::action::LLMGenerate_GetResult_Response>()
{
  return aimee_msgs::action::builder::Init_LLMGenerate_GetResult_Response_status();
}

}  // namespace aimee_msgs


namespace aimee_msgs
{

namespace action
{

namespace builder
{

class Init_LLMGenerate_FeedbackMessage_feedback
{
public:
  explicit Init_LLMGenerate_FeedbackMessage_feedback(::aimee_msgs::action::LLMGenerate_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::action::LLMGenerate_FeedbackMessage feedback(::aimee_msgs::action::LLMGenerate_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_FeedbackMessage msg_;
};

class Init_LLMGenerate_FeedbackMessage_goal_id
{
public:
  Init_LLMGenerate_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LLMGenerate_FeedbackMessage_feedback goal_id(::aimee_msgs::action::LLMGenerate_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_LLMGenerate_FeedbackMessage_feedback(msg_);
  }

private:
  ::aimee_msgs::action::LLMGenerate_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::action::LLMGenerate_FeedbackMessage>()
{
  return aimee_msgs::action::builder::Init_LLMGenerate_FeedbackMessage_goal_id();
}

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__ACTION__DETAIL__LLM_GENERATE__BUILDER_HPP_
