// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aimee_msgs:msg/WakeWordDetection.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__WAKE_WORD_DETECTION__BUILDER_HPP_
#define AIMEE_MSGS__MSG__DETAIL__WAKE_WORD_DETECTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aimee_msgs/msg/detail/wake_word_detection__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aimee_msgs
{

namespace msg
{

namespace builder
{

class Init_WakeWordDetection_session_id
{
public:
  explicit Init_WakeWordDetection_session_id(::aimee_msgs::msg::WakeWordDetection & msg)
  : msg_(msg)
  {}
  ::aimee_msgs::msg::WakeWordDetection session_id(::aimee_msgs::msg::WakeWordDetection::_session_id_type arg)
  {
    msg_.session_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aimee_msgs::msg::WakeWordDetection msg_;
};

class Init_WakeWordDetection_timestamp
{
public:
  explicit Init_WakeWordDetection_timestamp(::aimee_msgs::msg::WakeWordDetection & msg)
  : msg_(msg)
  {}
  Init_WakeWordDetection_session_id timestamp(::aimee_msgs::msg::WakeWordDetection::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return Init_WakeWordDetection_session_id(msg_);
  }

private:
  ::aimee_msgs::msg::WakeWordDetection msg_;
};

class Init_WakeWordDetection_active
{
public:
  explicit Init_WakeWordDetection_active(::aimee_msgs::msg::WakeWordDetection & msg)
  : msg_(msg)
  {}
  Init_WakeWordDetection_timestamp active(::aimee_msgs::msg::WakeWordDetection::_active_type arg)
  {
    msg_.active = std::move(arg);
    return Init_WakeWordDetection_timestamp(msg_);
  }

private:
  ::aimee_msgs::msg::WakeWordDetection msg_;
};

class Init_WakeWordDetection_signal_energy
{
public:
  explicit Init_WakeWordDetection_signal_energy(::aimee_msgs::msg::WakeWordDetection & msg)
  : msg_(msg)
  {}
  Init_WakeWordDetection_active signal_energy(::aimee_msgs::msg::WakeWordDetection::_signal_energy_type arg)
  {
    msg_.signal_energy = std::move(arg);
    return Init_WakeWordDetection_active(msg_);
  }

private:
  ::aimee_msgs::msg::WakeWordDetection msg_;
};

class Init_WakeWordDetection_sample_index
{
public:
  explicit Init_WakeWordDetection_sample_index(::aimee_msgs::msg::WakeWordDetection & msg)
  : msg_(msg)
  {}
  Init_WakeWordDetection_signal_energy sample_index(::aimee_msgs::msg::WakeWordDetection::_sample_index_type arg)
  {
    msg_.sample_index = std::move(arg);
    return Init_WakeWordDetection_signal_energy(msg_);
  }

private:
  ::aimee_msgs::msg::WakeWordDetection msg_;
};

class Init_WakeWordDetection_source
{
public:
  explicit Init_WakeWordDetection_source(::aimee_msgs::msg::WakeWordDetection & msg)
  : msg_(msg)
  {}
  Init_WakeWordDetection_sample_index source(::aimee_msgs::msg::WakeWordDetection::_source_type arg)
  {
    msg_.source = std::move(arg);
    return Init_WakeWordDetection_sample_index(msg_);
  }

private:
  ::aimee_msgs::msg::WakeWordDetection msg_;
};

class Init_WakeWordDetection_confidence
{
public:
  explicit Init_WakeWordDetection_confidence(::aimee_msgs::msg::WakeWordDetection & msg)
  : msg_(msg)
  {}
  Init_WakeWordDetection_source confidence(::aimee_msgs::msg::WakeWordDetection::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_WakeWordDetection_source(msg_);
  }

private:
  ::aimee_msgs::msg::WakeWordDetection msg_;
};

class Init_WakeWordDetection_wake_word
{
public:
  Init_WakeWordDetection_wake_word()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_WakeWordDetection_confidence wake_word(::aimee_msgs::msg::WakeWordDetection::_wake_word_type arg)
  {
    msg_.wake_word = std::move(arg);
    return Init_WakeWordDetection_confidence(msg_);
  }

private:
  ::aimee_msgs::msg::WakeWordDetection msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aimee_msgs::msg::WakeWordDetection>()
{
  return aimee_msgs::msg::builder::Init_WakeWordDetection_wake_word();
}

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__WAKE_WORD_DETECTION__BUILDER_HPP_
