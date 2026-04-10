// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aimee_msgs:msg/Transcription.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__TRANSCRIPTION__BUILDER_HPP_
#define AIMEE_MSGS__MSG__DETAIL__TRANSCRIPTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aimee_msgs/msg/detail/transcription__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aimee_msgs
{

namespace msg
{

namespace builder
{

class Init_Transcription_correlation_id
{
public:
  explicit Init_Transcription_correlation_id(::aimee_msgs::msg::Transcription & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::msg::Transcription correlation_id(::aimee_msgs::msg::Transcription::_correlation_id_type arg)
  {
    msg_.correlation_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::msg::Transcription msg_;
};

class Init_Transcription_session_id
{
public:
  explicit Init_Transcription_session_id(::aimee_msgs::msg::Transcription & msg)
  : msg_(msg)
  {}
  Init_Transcription_correlation_id session_id(::aimee_msgs::msg::Transcription::_session_id_type arg)
  {
    msg_.session_id = std::move(arg);
    return Init_Transcription_correlation_id(msg_);
  }

private:
  ::aimee_msgs::msg::Transcription msg_;
};

class Init_Transcription_timestamp
{
public:
  explicit Init_Transcription_timestamp(::aimee_msgs::msg::Transcription & msg)
  : msg_(msg)
  {}
  Init_Transcription_session_id timestamp(::aimee_msgs::msg::Transcription::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return Init_Transcription_session_id(msg_);
  }

private:
  ::aimee_msgs::msg::Transcription msg_;
};

class Init_Transcription_wake_word
{
public:
  explicit Init_Transcription_wake_word(::aimee_msgs::msg::Transcription & msg)
  : msg_(msg)
  {}
  Init_Transcription_timestamp wake_word(::aimee_msgs::msg::Transcription::_wake_word_type arg)
  {
    msg_.wake_word = std::move(arg);
    return Init_Transcription_timestamp(msg_);
  }

private:
  ::aimee_msgs::msg::Transcription msg_;
};

class Init_Transcription_wake_word_detected
{
public:
  explicit Init_Transcription_wake_word_detected(::aimee_msgs::msg::Transcription & msg)
  : msg_(msg)
  {}
  Init_Transcription_wake_word wake_word_detected(::aimee_msgs::msg::Transcription::_wake_word_detected_type arg)
  {
    msg_.wake_word_detected = std::move(arg);
    return Init_Transcription_wake_word(msg_);
  }

private:
  ::aimee_msgs::msg::Transcription msg_;
};

class Init_Transcription_is_partial
{
public:
  explicit Init_Transcription_is_partial(::aimee_msgs::msg::Transcription & msg)
  : msg_(msg)
  {}
  Init_Transcription_wake_word_detected is_partial(::aimee_msgs::msg::Transcription::_is_partial_type arg)
  {
    msg_.is_partial = std::move(arg);
    return Init_Transcription_wake_word_detected(msg_);
  }

private:
  ::aimee_msgs::msg::Transcription msg_;
};

class Init_Transcription_is_command
{
public:
  explicit Init_Transcription_is_command(::aimee_msgs::msg::Transcription & msg)
  : msg_(msg)
  {}
  Init_Transcription_is_partial is_command(::aimee_msgs::msg::Transcription::_is_command_type arg)
  {
    msg_.is_command = std::move(arg);
    return Init_Transcription_is_partial(msg_);
  }

private:
  ::aimee_msgs::msg::Transcription msg_;
};

class Init_Transcription_source
{
public:
  explicit Init_Transcription_source(::aimee_msgs::msg::Transcription & msg)
  : msg_(msg)
  {}
  Init_Transcription_is_command source(::aimee_msgs::msg::Transcription::_source_type arg)
  {
    msg_.source = std::move(arg);
    return Init_Transcription_is_command(msg_);
  }

private:
  ::aimee_msgs::msg::Transcription msg_;
};

class Init_Transcription_confidence
{
public:
  explicit Init_Transcription_confidence(::aimee_msgs::msg::Transcription & msg)
  : msg_(msg)
  {}
  Init_Transcription_source confidence(::aimee_msgs::msg::Transcription::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_Transcription_source(msg_);
  }

private:
  ::aimee_msgs::msg::Transcription msg_;
};

class Init_Transcription_text
{
public:
  Init_Transcription_text()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Transcription_confidence text(::aimee_msgs::msg::Transcription::_text_type arg)
  {
    msg_.text = std::move(arg);
    return Init_Transcription_confidence(msg_);
  }

private:
  ::aimee_msgs::msg::Transcription msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::msg::Transcription>()
{
  return aimee_msgs::msg::builder::Init_Transcription_text();
}

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__TRANSCRIPTION__BUILDER_HPP_
