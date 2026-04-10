// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aimee_msgs:action/ExecuteSkill.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__ACTION__DETAIL__EXECUTE_SKILL__BUILDER_HPP_
#define AIMEE_MSGS__ACTION__DETAIL__EXECUTE_SKILL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aimee_msgs/action/detail/execute_skill__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aimee_msgs
{

namespace action
{

namespace builder
{

class Init_ExecuteSkill_Goal_session_id
{
public:
  explicit Init_ExecuteSkill_Goal_session_id(::aimee_msgs::action::ExecuteSkill_Goal & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::action::ExecuteSkill_Goal session_id(::aimee_msgs::action::ExecuteSkill_Goal::_session_id_type arg)
  {
    msg_.session_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_Goal msg_;
};

class Init_ExecuteSkill_Goal_user_context
{
public:
  explicit Init_ExecuteSkill_Goal_user_context(::aimee_msgs::action::ExecuteSkill_Goal & msg)
  : msg_(msg)
  {}
  Init_ExecuteSkill_Goal_session_id user_context(::aimee_msgs::action::ExecuteSkill_Goal::_user_context_type arg)
  {
    msg_.user_context = std::move(arg);
    return Init_ExecuteSkill_Goal_session_id(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_Goal msg_;
};

class Init_ExecuteSkill_Goal_robot_state
{
public:
  explicit Init_ExecuteSkill_Goal_robot_state(::aimee_msgs::action::ExecuteSkill_Goal & msg)
  : msg_(msg)
  {}
  Init_ExecuteSkill_Goal_user_context robot_state(::aimee_msgs::action::ExecuteSkill_Goal::_robot_state_type arg)
  {
    msg_.robot_state = std::move(arg);
    return Init_ExecuteSkill_Goal_user_context(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_Goal msg_;
};

class Init_ExecuteSkill_Goal_user_input
{
public:
  explicit Init_ExecuteSkill_Goal_user_input(::aimee_msgs::action::ExecuteSkill_Goal & msg)
  : msg_(msg)
  {}
  Init_ExecuteSkill_Goal_robot_state user_input(::aimee_msgs::action::ExecuteSkill_Goal::_user_input_type arg)
  {
    msg_.user_input = std::move(arg);
    return Init_ExecuteSkill_Goal_robot_state(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_Goal msg_;
};

class Init_ExecuteSkill_Goal_skill_id
{
public:
  Init_ExecuteSkill_Goal_skill_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteSkill_Goal_user_input skill_id(::aimee_msgs::action::ExecuteSkill_Goal::_skill_id_type arg)
  {
    msg_.skill_id = std::move(arg);
    return Init_ExecuteSkill_Goal_user_input(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::action::ExecuteSkill_Goal>()
{
  return aimee_msgs::action::builder::Init_ExecuteSkill_Goal_skill_id();
}

}  // namespace aimee_msgs


namespace aimee_msgs
{

namespace action
{

namespace builder
{

class Init_ExecuteSkill_Result_led_actions
{
public:
  explicit Init_ExecuteSkill_Result_led_actions(::aimee_msgs::action::ExecuteSkill_Result & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::action::ExecuteSkill_Result led_actions(::aimee_msgs::action::ExecuteSkill_Result::_led_actions_type arg)
  {
    msg_.led_actions = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_Result msg_;
};

class Init_ExecuteSkill_Result_camera_actions
{
public:
  explicit Init_ExecuteSkill_Result_camera_actions(::aimee_msgs::action::ExecuteSkill_Result & msg)
  : msg_(msg)
  {}
  Init_ExecuteSkill_Result_led_actions camera_actions(::aimee_msgs::action::ExecuteSkill_Result::_camera_actions_type arg)
  {
    msg_.camera_actions = std::move(arg);
    return Init_ExecuteSkill_Result_led_actions(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_Result msg_;
};

class Init_ExecuteSkill_Result_motor_actions
{
public:
  explicit Init_ExecuteSkill_Result_motor_actions(::aimee_msgs::action::ExecuteSkill_Result & msg)
  : msg_(msg)
  {}
  Init_ExecuteSkill_Result_camera_actions motor_actions(::aimee_msgs::action::ExecuteSkill_Result::_motor_actions_type arg)
  {
    msg_.motor_actions = std::move(arg);
    return Init_ExecuteSkill_Result_camera_actions(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_Result msg_;
};

class Init_ExecuteSkill_Result_error_message
{
public:
  explicit Init_ExecuteSkill_Result_error_message(::aimee_msgs::action::ExecuteSkill_Result & msg)
  : msg_(msg)
  {}
  Init_ExecuteSkill_Result_motor_actions error_message(::aimee_msgs::action::ExecuteSkill_Result::_error_message_type arg)
  {
    msg_.error_message = std::move(arg);
    return Init_ExecuteSkill_Result_motor_actions(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_Result msg_;
};

class Init_ExecuteSkill_Result_tts_audio_path
{
public:
  explicit Init_ExecuteSkill_Result_tts_audio_path(::aimee_msgs::action::ExecuteSkill_Result & msg)
  : msg_(msg)
  {}
  Init_ExecuteSkill_Result_error_message tts_audio_path(::aimee_msgs::action::ExecuteSkill_Result::_tts_audio_path_type arg)
  {
    msg_.tts_audio_path = std::move(arg);
    return Init_ExecuteSkill_Result_error_message(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_Result msg_;
};

class Init_ExecuteSkill_Result_response_text
{
public:
  explicit Init_ExecuteSkill_Result_response_text(::aimee_msgs::action::ExecuteSkill_Result & msg)
  : msg_(msg)
  {}
  Init_ExecuteSkill_Result_tts_audio_path response_text(::aimee_msgs::action::ExecuteSkill_Result::_response_text_type arg)
  {
    msg_.response_text = std::move(arg);
    return Init_ExecuteSkill_Result_tts_audio_path(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_Result msg_;
};

class Init_ExecuteSkill_Result_success
{
public:
  Init_ExecuteSkill_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteSkill_Result_response_text success(::aimee_msgs::action::ExecuteSkill_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_ExecuteSkill_Result_response_text(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::action::ExecuteSkill_Result>()
{
  return aimee_msgs::action::builder::Init_ExecuteSkill_Result_success();
}

}  // namespace aimee_msgs


namespace aimee_msgs
{

namespace action
{

namespace builder
{

class Init_ExecuteSkill_Feedback_can_cancel
{
public:
  explicit Init_ExecuteSkill_Feedback_can_cancel(::aimee_msgs::action::ExecuteSkill_Feedback & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::action::ExecuteSkill_Feedback can_cancel(::aimee_msgs::action::ExecuteSkill_Feedback::_can_cancel_type arg)
  {
    msg_.can_cancel = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_Feedback msg_;
};

class Init_ExecuteSkill_Feedback_progress
{
public:
  explicit Init_ExecuteSkill_Feedback_progress(::aimee_msgs::action::ExecuteSkill_Feedback & msg)
  : msg_(msg)
  {}
  Init_ExecuteSkill_Feedback_can_cancel progress(::aimee_msgs::action::ExecuteSkill_Feedback::_progress_type arg)
  {
    msg_.progress = std::move(arg);
    return Init_ExecuteSkill_Feedback_can_cancel(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_Feedback msg_;
};

class Init_ExecuteSkill_Feedback_current_action
{
public:
  explicit Init_ExecuteSkill_Feedback_current_action(::aimee_msgs::action::ExecuteSkill_Feedback & msg)
  : msg_(msg)
  {}
  Init_ExecuteSkill_Feedback_progress current_action(::aimee_msgs::action::ExecuteSkill_Feedback::_current_action_type arg)
  {
    msg_.current_action = std::move(arg);
    return Init_ExecuteSkill_Feedback_progress(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_Feedback msg_;
};

class Init_ExecuteSkill_Feedback_status
{
public:
  Init_ExecuteSkill_Feedback_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteSkill_Feedback_current_action status(::aimee_msgs::action::ExecuteSkill_Feedback::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_ExecuteSkill_Feedback_current_action(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::action::ExecuteSkill_Feedback>()
{
  return aimee_msgs::action::builder::Init_ExecuteSkill_Feedback_status();
}

}  // namespace aimee_msgs


namespace aimee_msgs
{

namespace action
{

namespace builder
{

class Init_ExecuteSkill_SendGoal_Request_goal
{
public:
  explicit Init_ExecuteSkill_SendGoal_Request_goal(::aimee_msgs::action::ExecuteSkill_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::action::ExecuteSkill_SendGoal_Request goal(::aimee_msgs::action::ExecuteSkill_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_SendGoal_Request msg_;
};

class Init_ExecuteSkill_SendGoal_Request_goal_id
{
public:
  Init_ExecuteSkill_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteSkill_SendGoal_Request_goal goal_id(::aimee_msgs::action::ExecuteSkill_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_ExecuteSkill_SendGoal_Request_goal(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::action::ExecuteSkill_SendGoal_Request>()
{
  return aimee_msgs::action::builder::Init_ExecuteSkill_SendGoal_Request_goal_id();
}

}  // namespace aimee_msgs


namespace aimee_msgs
{

namespace action
{

namespace builder
{

class Init_ExecuteSkill_SendGoal_Response_stamp
{
public:
  explicit Init_ExecuteSkill_SendGoal_Response_stamp(::aimee_msgs::action::ExecuteSkill_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::action::ExecuteSkill_SendGoal_Response stamp(::aimee_msgs::action::ExecuteSkill_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_SendGoal_Response msg_;
};

class Init_ExecuteSkill_SendGoal_Response_accepted
{
public:
  Init_ExecuteSkill_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteSkill_SendGoal_Response_stamp accepted(::aimee_msgs::action::ExecuteSkill_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_ExecuteSkill_SendGoal_Response_stamp(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::action::ExecuteSkill_SendGoal_Response>()
{
  return aimee_msgs::action::builder::Init_ExecuteSkill_SendGoal_Response_accepted();
}

}  // namespace aimee_msgs


namespace aimee_msgs
{

namespace action
{

namespace builder
{

class Init_ExecuteSkill_GetResult_Request_goal_id
{
public:
  Init_ExecuteSkill_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aimee_msgs::action::ExecuteSkill_GetResult_Request goal_id(::aimee_msgs::action::ExecuteSkill_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::action::ExecuteSkill_GetResult_Request>()
{
  return aimee_msgs::action::builder::Init_ExecuteSkill_GetResult_Request_goal_id();
}

}  // namespace aimee_msgs


namespace aimee_msgs
{

namespace action
{

namespace builder
{

class Init_ExecuteSkill_GetResult_Response_result
{
public:
  explicit Init_ExecuteSkill_GetResult_Response_result(::aimee_msgs::action::ExecuteSkill_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::action::ExecuteSkill_GetResult_Response result(::aimee_msgs::action::ExecuteSkill_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_GetResult_Response msg_;
};

class Init_ExecuteSkill_GetResult_Response_status
{
public:
  Init_ExecuteSkill_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteSkill_GetResult_Response_result status(::aimee_msgs::action::ExecuteSkill_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_ExecuteSkill_GetResult_Response_result(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::action::ExecuteSkill_GetResult_Response>()
{
  return aimee_msgs::action::builder::Init_ExecuteSkill_GetResult_Response_status();
}

}  // namespace aimee_msgs


namespace aimee_msgs
{

namespace action
{

namespace builder
{

class Init_ExecuteSkill_FeedbackMessage_feedback
{
public:
  explicit Init_ExecuteSkill_FeedbackMessage_feedback(::aimee_msgs::action::ExecuteSkill_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::action::ExecuteSkill_FeedbackMessage feedback(::aimee_msgs::action::ExecuteSkill_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_FeedbackMessage msg_;
};

class Init_ExecuteSkill_FeedbackMessage_goal_id
{
public:
  Init_ExecuteSkill_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteSkill_FeedbackMessage_feedback goal_id(::aimee_msgs::action::ExecuteSkill_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_ExecuteSkill_FeedbackMessage_feedback(msg_);
  }

private:
  ::aimee_msgs::action::ExecuteSkill_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::action::ExecuteSkill_FeedbackMessage>()
{
  return aimee_msgs::action::builder::Init_ExecuteSkill_FeedbackMessage_goal_id();
}

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__ACTION__DETAIL__EXECUTE_SKILL__BUILDER_HPP_
