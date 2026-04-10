
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to aimee_msgs__action__LLMGenerate_Goal

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LLMGenerate_Goal {
    /// Goal: Request for LLM generation
    /// User prompt
    pub prompt: std::string::String,

    /// System prompt/persona
    pub system_context: std::string::String,

    /// Maximum tokens to generate (default: 150)
    pub max_tokens: i32,

    /// Sampling temperature (default: 0.7)
    pub temperature: f32,

    /// Enable streaming feedback (default: true)
    pub stream: bool,

    /// Session identifier for context
    pub session_id: std::string::String,

}



impl Default for LLMGenerate_Goal {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::LLMGenerate_Goal::default())
  }
}

impl rosidl_runtime_rs::Message for LLMGenerate_Goal {
  type RmwMsg = super::action::rmw::LLMGenerate_Goal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        prompt: msg.prompt.as_str().into(),
        system_context: msg.system_context.as_str().into(),
        max_tokens: msg.max_tokens,
        temperature: msg.temperature,
        stream: msg.stream,
        session_id: msg.session_id.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        prompt: msg.prompt.as_str().into(),
        system_context: msg.system_context.as_str().into(),
      max_tokens: msg.max_tokens,
      temperature: msg.temperature,
      stream: msg.stream,
        session_id: msg.session_id.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      prompt: msg.prompt.to_string(),
      system_context: msg.system_context.to_string(),
      max_tokens: msg.max_tokens,
      temperature: msg.temperature,
      stream: msg.stream,
      session_id: msg.session_id.to_string(),
    }
  }
}


// Corresponds to aimee_msgs__action__LLMGenerate_Result

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LLMGenerate_Result {
    /// Complete generated text
    pub response: std::string::String,

    /// True if generation succeeded
    pub success: bool,

    /// Error details if failed
    pub error_message: std::string::String,

    /// Time taken in seconds
    pub generation_time: f32,

    /// Total tokens generated
    pub tokens_generated: i32,

    /// Input prompt tokens
    pub tokens_input: i32,

}



impl Default for LLMGenerate_Result {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::LLMGenerate_Result::default())
  }
}

impl rosidl_runtime_rs::Message for LLMGenerate_Result {
  type RmwMsg = super::action::rmw::LLMGenerate_Result;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        response: msg.response.as_str().into(),
        success: msg.success,
        error_message: msg.error_message.as_str().into(),
        generation_time: msg.generation_time,
        tokens_generated: msg.tokens_generated,
        tokens_input: msg.tokens_input,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        response: msg.response.as_str().into(),
      success: msg.success,
        error_message: msg.error_message.as_str().into(),
      generation_time: msg.generation_time,
      tokens_generated: msg.tokens_generated,
      tokens_input: msg.tokens_input,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      response: msg.response.to_string(),
      success: msg.success,
      error_message: msg.error_message.to_string(),
      generation_time: msg.generation_time,
      tokens_generated: msg.tokens_generated,
      tokens_input: msg.tokens_input,
    }
  }
}


// Corresponds to aimee_msgs__action__LLMGenerate_Feedback

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LLMGenerate_Feedback {
    /// Cumulative text so far
    pub partial_response: std::string::String,

    /// Tokens generated so far
    pub tokens_generated: i32,

    /// Estimated total tokens
    pub tokens_total: i32,

    /// True if generation finished
    pub is_complete: bool,

    /// Currently generating word (optional)
    pub current_word: std::string::String,

}



impl Default for LLMGenerate_Feedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::LLMGenerate_Feedback::default())
  }
}

impl rosidl_runtime_rs::Message for LLMGenerate_Feedback {
  type RmwMsg = super::action::rmw::LLMGenerate_Feedback;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        partial_response: msg.partial_response.as_str().into(),
        tokens_generated: msg.tokens_generated,
        tokens_total: msg.tokens_total,
        is_complete: msg.is_complete,
        current_word: msg.current_word.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        partial_response: msg.partial_response.as_str().into(),
      tokens_generated: msg.tokens_generated,
      tokens_total: msg.tokens_total,
      is_complete: msg.is_complete,
        current_word: msg.current_word.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      partial_response: msg.partial_response.to_string(),
      tokens_generated: msg.tokens_generated,
      tokens_total: msg.tokens_total,
      is_complete: msg.is_complete,
      current_word: msg.current_word.to_string(),
    }
  }
}


// Corresponds to aimee_msgs__action__LLMGenerate_FeedbackMessage

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LLMGenerate_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::action::LLMGenerate_Feedback,

}



impl Default for LLMGenerate_FeedbackMessage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::LLMGenerate_FeedbackMessage::default())
  }
}

impl rosidl_runtime_rs::Message for LLMGenerate_FeedbackMessage {
  type RmwMsg = super::action::rmw::LLMGenerate_FeedbackMessage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        feedback: super::action::LLMGenerate_Feedback::into_rmw_message(std::borrow::Cow::Owned(msg.feedback)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        feedback: super::action::LLMGenerate_Feedback::into_rmw_message(std::borrow::Cow::Borrowed(&msg.feedback)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      feedback: super::action::LLMGenerate_Feedback::from_rmw_message(msg.feedback),
    }
  }
}


// Corresponds to aimee_msgs__action__ExecuteSkill_Goal

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSkill_Goal {
    /// Goal: Request to execute a skill
    /// Skill identifier
    pub skill_id: std::string::String,

    /// User's command/text
    pub user_input: std::string::String,

    /// Current robot state
    pub robot_state: super::msg::RobotState,

    /// JSON string with user context
    pub user_context: std::string::String,

    /// Session identifier
    pub session_id: std::string::String,

}



impl Default for ExecuteSkill_Goal {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecuteSkill_Goal::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteSkill_Goal {
  type RmwMsg = super::action::rmw::ExecuteSkill_Goal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        skill_id: msg.skill_id.as_str().into(),
        user_input: msg.user_input.as_str().into(),
        robot_state: super::msg::RobotState::into_rmw_message(std::borrow::Cow::Owned(msg.robot_state)).into_owned(),
        user_context: msg.user_context.as_str().into(),
        session_id: msg.session_id.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        skill_id: msg.skill_id.as_str().into(),
        user_input: msg.user_input.as_str().into(),
        robot_state: super::msg::RobotState::into_rmw_message(std::borrow::Cow::Borrowed(&msg.robot_state)).into_owned(),
        user_context: msg.user_context.as_str().into(),
        session_id: msg.session_id.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      skill_id: msg.skill_id.to_string(),
      user_input: msg.user_input.to_string(),
      robot_state: super::msg::RobotState::from_rmw_message(msg.robot_state),
      user_context: msg.user_context.to_string(),
      session_id: msg.session_id.to_string(),
    }
  }
}


// Corresponds to aimee_msgs__action__ExecuteSkill_Result

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSkill_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

    /// Text response from skill
    pub response_text: std::string::String,

    /// Path to TTS audio file (if generated)
    pub tts_audio_path: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_message: std::string::String,

    /// Actions performed
    pub motor_actions: Vec<super::msg::MotorAction>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub camera_actions: Vec<super::msg::CameraAction>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub led_actions: Vec<super::msg::LEDAction>,

}



impl Default for ExecuteSkill_Result {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecuteSkill_Result::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteSkill_Result {
  type RmwMsg = super::action::rmw::ExecuteSkill_Result;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        response_text: msg.response_text.as_str().into(),
        tts_audio_path: msg.tts_audio_path.as_str().into(),
        error_message: msg.error_message.as_str().into(),
        motor_actions: msg.motor_actions
          .into_iter()
          .map(|elem| super::msg::MotorAction::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        camera_actions: msg.camera_actions
          .into_iter()
          .map(|elem| super::msg::CameraAction::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        led_actions: msg.led_actions
          .into_iter()
          .map(|elem| super::msg::LEDAction::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        response_text: msg.response_text.as_str().into(),
        tts_audio_path: msg.tts_audio_path.as_str().into(),
        error_message: msg.error_message.as_str().into(),
        motor_actions: msg.motor_actions
          .iter()
          .map(|elem| super::msg::MotorAction::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        camera_actions: msg.camera_actions
          .iter()
          .map(|elem| super::msg::CameraAction::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        led_actions: msg.led_actions
          .iter()
          .map(|elem| super::msg::LEDAction::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      response_text: msg.response_text.to_string(),
      tts_audio_path: msg.tts_audio_path.to_string(),
      error_message: msg.error_message.to_string(),
      motor_actions: msg.motor_actions
          .into_iter()
          .map(super::msg::MotorAction::from_rmw_message)
          .collect(),
      camera_actions: msg.camera_actions
          .into_iter()
          .map(super::msg::CameraAction::from_rmw_message)
          .collect(),
      led_actions: msg.led_actions
          .into_iter()
          .map(super::msg::LEDAction::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to aimee_msgs__action__ExecuteSkill_Feedback

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSkill_Feedback {
    /// "starting" | "executing" | "finalizing"
    pub status: std::string::String,

    /// Description of current action
    pub current_action: std::string::String,

    /// 0.0 to 1.0
    pub progress: f32,

    /// Whether skill can be cancelled now
    pub can_cancel: bool,

}



impl Default for ExecuteSkill_Feedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecuteSkill_Feedback::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteSkill_Feedback {
  type RmwMsg = super::action::rmw::ExecuteSkill_Feedback;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status.as_str().into(),
        current_action: msg.current_action.as_str().into(),
        progress: msg.progress,
        can_cancel: msg.can_cancel,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status.as_str().into(),
        current_action: msg.current_action.as_str().into(),
      progress: msg.progress,
      can_cancel: msg.can_cancel,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status.to_string(),
      current_action: msg.current_action.to_string(),
      progress: msg.progress,
      can_cancel: msg.can_cancel,
    }
  }
}


// Corresponds to aimee_msgs__action__ExecuteSkill_FeedbackMessage

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSkill_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::action::ExecuteSkill_Feedback,

}



impl Default for ExecuteSkill_FeedbackMessage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecuteSkill_FeedbackMessage::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteSkill_FeedbackMessage {
  type RmwMsg = super::action::rmw::ExecuteSkill_FeedbackMessage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        feedback: super::action::ExecuteSkill_Feedback::into_rmw_message(std::borrow::Cow::Owned(msg.feedback)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        feedback: super::action::ExecuteSkill_Feedback::into_rmw_message(std::borrow::Cow::Borrowed(&msg.feedback)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      feedback: super::action::ExecuteSkill_Feedback::from_rmw_message(msg.feedback),
    }
  }
}






// Corresponds to aimee_msgs__action__LLMGenerate_SendGoal_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LLMGenerate_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::action::LLMGenerate_Goal,

}



impl Default for LLMGenerate_SendGoal_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::LLMGenerate_SendGoal_Request::default())
  }
}

impl rosidl_runtime_rs::Message for LLMGenerate_SendGoal_Request {
  type RmwMsg = super::action::rmw::LLMGenerate_SendGoal_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        goal: super::action::LLMGenerate_Goal::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        goal: super::action::LLMGenerate_Goal::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      goal: super::action::LLMGenerate_Goal::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to aimee_msgs__action__LLMGenerate_SendGoal_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LLMGenerate_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for LLMGenerate_SendGoal_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::LLMGenerate_SendGoal_Response::default())
  }
}

impl rosidl_runtime_rs::Message for LLMGenerate_SendGoal_Response {
  type RmwMsg = super::action::rmw::LLMGenerate_SendGoal_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to aimee_msgs__action__LLMGenerate_GetResult_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LLMGenerate_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,

}



impl Default for LLMGenerate_GetResult_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::LLMGenerate_GetResult_Request::default())
  }
}

impl rosidl_runtime_rs::Message for LLMGenerate_GetResult_Request {
  type RmwMsg = super::action::rmw::LLMGenerate_GetResult_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
    }
  }
}


// Corresponds to aimee_msgs__action__LLMGenerate_GetResult_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LLMGenerate_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::action::LLMGenerate_Result,

}



impl Default for LLMGenerate_GetResult_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::LLMGenerate_GetResult_Response::default())
  }
}

impl rosidl_runtime_rs::Message for LLMGenerate_GetResult_Response {
  type RmwMsg = super::action::rmw::LLMGenerate_GetResult_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        result: super::action::LLMGenerate_Result::into_rmw_message(std::borrow::Cow::Owned(msg.result)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
        result: super::action::LLMGenerate_Result::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      result: super::action::LLMGenerate_Result::from_rmw_message(msg.result),
    }
  }
}


// Corresponds to aimee_msgs__action__ExecuteSkill_SendGoal_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSkill_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::action::ExecuteSkill_Goal,

}



impl Default for ExecuteSkill_SendGoal_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecuteSkill_SendGoal_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteSkill_SendGoal_Request {
  type RmwMsg = super::action::rmw::ExecuteSkill_SendGoal_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        goal: super::action::ExecuteSkill_Goal::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        goal: super::action::ExecuteSkill_Goal::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      goal: super::action::ExecuteSkill_Goal::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to aimee_msgs__action__ExecuteSkill_SendGoal_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSkill_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for ExecuteSkill_SendGoal_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecuteSkill_SendGoal_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteSkill_SendGoal_Response {
  type RmwMsg = super::action::rmw::ExecuteSkill_SendGoal_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to aimee_msgs__action__ExecuteSkill_GetResult_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSkill_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,

}



impl Default for ExecuteSkill_GetResult_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecuteSkill_GetResult_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteSkill_GetResult_Request {
  type RmwMsg = super::action::rmw::ExecuteSkill_GetResult_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
    }
  }
}


// Corresponds to aimee_msgs__action__ExecuteSkill_GetResult_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSkill_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::action::ExecuteSkill_Result,

}



impl Default for ExecuteSkill_GetResult_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecuteSkill_GetResult_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteSkill_GetResult_Response {
  type RmwMsg = super::action::rmw::ExecuteSkill_GetResult_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        result: super::action::ExecuteSkill_Result::into_rmw_message(std::borrow::Cow::Owned(msg.result)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
        result: super::action::ExecuteSkill_Result::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      result: super::action::ExecuteSkill_Result::from_rmw_message(msg.result),
    }
  }
}






#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__aimee_msgs__action__LLMGenerate_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to aimee_msgs__action__LLMGenerate_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct LLMGenerate_SendGoal;

impl rosidl_runtime_rs::Service for LLMGenerate_SendGoal {
    type Request = LLMGenerate_SendGoal_Request;
    type Response = LLMGenerate_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__aimee_msgs__action__LLMGenerate_SendGoal() }
    }
}




#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__aimee_msgs__action__LLMGenerate_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to aimee_msgs__action__LLMGenerate_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct LLMGenerate_GetResult;

impl rosidl_runtime_rs::Service for LLMGenerate_GetResult {
    type Request = LLMGenerate_GetResult_Request;
    type Response = LLMGenerate_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__aimee_msgs__action__LLMGenerate_GetResult() }
    }
}




#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__aimee_msgs__action__ExecuteSkill_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to aimee_msgs__action__ExecuteSkill_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct ExecuteSkill_SendGoal;

impl rosidl_runtime_rs::Service for ExecuteSkill_SendGoal {
    type Request = ExecuteSkill_SendGoal_Request;
    type Response = ExecuteSkill_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__aimee_msgs__action__ExecuteSkill_SendGoal() }
    }
}




#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__aimee_msgs__action__ExecuteSkill_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to aimee_msgs__action__ExecuteSkill_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct ExecuteSkill_GetResult;

impl rosidl_runtime_rs::Service for ExecuteSkill_GetResult {
    type Request = ExecuteSkill_GetResult_Request;
    type Response = ExecuteSkill_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__aimee_msgs__action__ExecuteSkill_GetResult() }
    }
}






#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_action_type_support_handle__aimee_msgs__action__LLMGenerate() -> *const std::ffi::c_void;
}

// Corresponds to aimee_msgs__action__LLMGenerate
#[allow(missing_docs, non_camel_case_types)]
pub struct LLMGenerate;

impl rosidl_runtime_rs::Action for LLMGenerate {
  // --- Associated types for client library users ---
  /// The goal message defined in the action definition.
  type Goal = LLMGenerate_Goal;

  /// The result message defined in the action definition.
  type Result = LLMGenerate_Result;

  /// The feedback message defined in the action definition.
  type Feedback = LLMGenerate_Feedback;

  // --- Associated types for client library implementation ---
  /// The feedback message with generic fields which wraps the feedback message.
  type FeedbackMessage = super::action::LLMGenerate_FeedbackMessage;

  /// The send_goal service using a wrapped version of the goal message as a request.
  type SendGoalService = super::action::LLMGenerate_SendGoal;

  /// The generic service to cancel a goal.
  type CancelGoalService = action_msgs::srv::rmw::CancelGoal;

  /// The get_result service using a wrapped version of the result message as a response.
  type GetResultService = super::action::LLMGenerate_GetResult;

  // --- Methods for client library implementation ---
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_action_type_support_handle__aimee_msgs__action__LLMGenerate() }
  }

  fn create_goal_request(
    goal_id: &[u8; 16],
    goal: super::action::rmw::LLMGenerate_Goal,
  ) -> super::action::rmw::LLMGenerate_SendGoal_Request {
   super::action::rmw::LLMGenerate_SendGoal_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
      goal,
    }
  }

  fn split_goal_request(
    request: super::action::rmw::LLMGenerate_SendGoal_Request,
  ) -> (
    [u8; 16],
   super::action::rmw::LLMGenerate_Goal,
  ) {
    (request.goal_id.uuid, request.goal)
  }

  fn create_goal_response(
    accepted: bool,
    stamp: (i32, u32),
  ) -> super::action::rmw::LLMGenerate_SendGoal_Response {
   super::action::rmw::LLMGenerate_SendGoal_Response {
      accepted,
      stamp: builtin_interfaces::msg::rmw::Time {
        sec: stamp.0,
        nanosec: stamp.1,
      },
    }
  }

  fn get_goal_response_accepted(
    response: &super::action::rmw::LLMGenerate_SendGoal_Response,
  ) -> bool {
    response.accepted
  }

  fn get_goal_response_stamp(
    response: &super::action::rmw::LLMGenerate_SendGoal_Response,
  ) -> (i32, u32) {
    (response.stamp.sec, response.stamp.nanosec)
  }

  fn create_feedback_message(
    goal_id: &[u8; 16],
    feedback: super::action::rmw::LLMGenerate_Feedback,
  ) -> super::action::rmw::LLMGenerate_FeedbackMessage {
    let mut message = super::action::rmw::LLMGenerate_FeedbackMessage::default();
    message.goal_id.uuid = *goal_id;
    message.feedback = feedback;
    message
  }

  fn split_feedback_message(
    feedback: super::action::rmw::LLMGenerate_FeedbackMessage,
  ) -> (
    [u8; 16],
   super::action::rmw::LLMGenerate_Feedback,
  ) {
    (feedback.goal_id.uuid, feedback.feedback)
  }

  fn create_result_request(
    goal_id: &[u8; 16],
  ) -> super::action::rmw::LLMGenerate_GetResult_Request {
   super::action::rmw::LLMGenerate_GetResult_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
    }
  }

  fn get_result_request_uuid(
    request: &super::action::rmw::LLMGenerate_GetResult_Request,
  ) -> &[u8; 16] {
    &request.goal_id.uuid
  }

  fn create_result_response(
    status: i8,
    result: super::action::rmw::LLMGenerate_Result,
  ) -> super::action::rmw::LLMGenerate_GetResult_Response {
   super::action::rmw::LLMGenerate_GetResult_Response {
      status,
      result,
    }
  }

  fn split_result_response(
    response: super::action::rmw::LLMGenerate_GetResult_Response
  ) -> (
    i8,
   super::action::rmw::LLMGenerate_Result,
  ) {
    (response.status, response.result)
  }
}




#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_action_type_support_handle__aimee_msgs__action__ExecuteSkill() -> *const std::ffi::c_void;
}

// Corresponds to aimee_msgs__action__ExecuteSkill
#[allow(missing_docs, non_camel_case_types)]
pub struct ExecuteSkill;

impl rosidl_runtime_rs::Action for ExecuteSkill {
  // --- Associated types for client library users ---
  /// The goal message defined in the action definition.
  type Goal = ExecuteSkill_Goal;

  /// The result message defined in the action definition.
  type Result = ExecuteSkill_Result;

  /// The feedback message defined in the action definition.
  type Feedback = ExecuteSkill_Feedback;

  // --- Associated types for client library implementation ---
  /// The feedback message with generic fields which wraps the feedback message.
  type FeedbackMessage = super::action::ExecuteSkill_FeedbackMessage;

  /// The send_goal service using a wrapped version of the goal message as a request.
  type SendGoalService = super::action::ExecuteSkill_SendGoal;

  /// The generic service to cancel a goal.
  type CancelGoalService = action_msgs::srv::rmw::CancelGoal;

  /// The get_result service using a wrapped version of the result message as a response.
  type GetResultService = super::action::ExecuteSkill_GetResult;

  // --- Methods for client library implementation ---
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_action_type_support_handle__aimee_msgs__action__ExecuteSkill() }
  }

  fn create_goal_request(
    goal_id: &[u8; 16],
    goal: super::action::rmw::ExecuteSkill_Goal,
  ) -> super::action::rmw::ExecuteSkill_SendGoal_Request {
   super::action::rmw::ExecuteSkill_SendGoal_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
      goal,
    }
  }

  fn split_goal_request(
    request: super::action::rmw::ExecuteSkill_SendGoal_Request,
  ) -> (
    [u8; 16],
   super::action::rmw::ExecuteSkill_Goal,
  ) {
    (request.goal_id.uuid, request.goal)
  }

  fn create_goal_response(
    accepted: bool,
    stamp: (i32, u32),
  ) -> super::action::rmw::ExecuteSkill_SendGoal_Response {
   super::action::rmw::ExecuteSkill_SendGoal_Response {
      accepted,
      stamp: builtin_interfaces::msg::rmw::Time {
        sec: stamp.0,
        nanosec: stamp.1,
      },
    }
  }

  fn get_goal_response_accepted(
    response: &super::action::rmw::ExecuteSkill_SendGoal_Response,
  ) -> bool {
    response.accepted
  }

  fn get_goal_response_stamp(
    response: &super::action::rmw::ExecuteSkill_SendGoal_Response,
  ) -> (i32, u32) {
    (response.stamp.sec, response.stamp.nanosec)
  }

  fn create_feedback_message(
    goal_id: &[u8; 16],
    feedback: super::action::rmw::ExecuteSkill_Feedback,
  ) -> super::action::rmw::ExecuteSkill_FeedbackMessage {
    let mut message = super::action::rmw::ExecuteSkill_FeedbackMessage::default();
    message.goal_id.uuid = *goal_id;
    message.feedback = feedback;
    message
  }

  fn split_feedback_message(
    feedback: super::action::rmw::ExecuteSkill_FeedbackMessage,
  ) -> (
    [u8; 16],
   super::action::rmw::ExecuteSkill_Feedback,
  ) {
    (feedback.goal_id.uuid, feedback.feedback)
  }

  fn create_result_request(
    goal_id: &[u8; 16],
  ) -> super::action::rmw::ExecuteSkill_GetResult_Request {
   super::action::rmw::ExecuteSkill_GetResult_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
    }
  }

  fn get_result_request_uuid(
    request: &super::action::rmw::ExecuteSkill_GetResult_Request,
  ) -> &[u8; 16] {
    &request.goal_id.uuid
  }

  fn create_result_response(
    status: i8,
    result: super::action::rmw::ExecuteSkill_Result,
  ) -> super::action::rmw::ExecuteSkill_GetResult_Response {
   super::action::rmw::ExecuteSkill_GetResult_Response {
      status,
      result,
    }
  }

  fn split_result_response(
    response: super::action::rmw::ExecuteSkill_GetResult_Response
  ) -> (
    i8,
   super::action::rmw::ExecuteSkill_Result,
  ) {
    (response.status, response.result)
  }
}


