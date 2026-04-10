
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__LLMGenerate_Goal() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__action__LLMGenerate_Goal__init(msg: *mut LLMGenerate_Goal) -> bool;
    fn aimee_msgs__action__LLMGenerate_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_Goal>, size: usize) -> bool;
    fn aimee_msgs__action__LLMGenerate_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_Goal>);
    fn aimee_msgs__action__LLMGenerate_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LLMGenerate_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_Goal>) -> bool;
}

// Corresponds to aimee_msgs__action__LLMGenerate_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LLMGenerate_Goal {
    /// Goal: Request for LLM generation
    /// User prompt
    pub prompt: rosidl_runtime_rs::String,

    /// System prompt/persona
    pub system_context: rosidl_runtime_rs::String,

    /// Maximum tokens to generate (default: 150)
    pub max_tokens: i32,

    /// Sampling temperature (default: 0.7)
    pub temperature: f32,

    /// Enable streaming feedback (default: true)
    pub stream: bool,

    /// Session identifier for context
    pub session_id: rosidl_runtime_rs::String,

}



impl Default for LLMGenerate_Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__action__LLMGenerate_Goal__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__action__LLMGenerate_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LLMGenerate_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LLMGenerate_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LLMGenerate_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/action/LLMGenerate_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__LLMGenerate_Goal() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__LLMGenerate_Result() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__action__LLMGenerate_Result__init(msg: *mut LLMGenerate_Result) -> bool;
    fn aimee_msgs__action__LLMGenerate_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_Result>, size: usize) -> bool;
    fn aimee_msgs__action__LLMGenerate_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_Result>);
    fn aimee_msgs__action__LLMGenerate_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LLMGenerate_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_Result>) -> bool;
}

// Corresponds to aimee_msgs__action__LLMGenerate_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LLMGenerate_Result {
    /// Complete generated text
    pub response: rosidl_runtime_rs::String,

    /// True if generation succeeded
    pub success: bool,

    /// Error details if failed
    pub error_message: rosidl_runtime_rs::String,

    /// Time taken in seconds
    pub generation_time: f32,

    /// Total tokens generated
    pub tokens_generated: i32,

    /// Input prompt tokens
    pub tokens_input: i32,

}



impl Default for LLMGenerate_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__action__LLMGenerate_Result__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__action__LLMGenerate_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LLMGenerate_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LLMGenerate_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LLMGenerate_Result where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/action/LLMGenerate_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__LLMGenerate_Result() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__LLMGenerate_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__action__LLMGenerate_Feedback__init(msg: *mut LLMGenerate_Feedback) -> bool;
    fn aimee_msgs__action__LLMGenerate_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_Feedback>, size: usize) -> bool;
    fn aimee_msgs__action__LLMGenerate_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_Feedback>);
    fn aimee_msgs__action__LLMGenerate_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LLMGenerate_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_Feedback>) -> bool;
}

// Corresponds to aimee_msgs__action__LLMGenerate_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LLMGenerate_Feedback {
    /// Cumulative text so far
    pub partial_response: rosidl_runtime_rs::String,

    /// Tokens generated so far
    pub tokens_generated: i32,

    /// Estimated total tokens
    pub tokens_total: i32,

    /// True if generation finished
    pub is_complete: bool,

    /// Currently generating word (optional)
    pub current_word: rosidl_runtime_rs::String,

}



impl Default for LLMGenerate_Feedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__action__LLMGenerate_Feedback__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__action__LLMGenerate_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LLMGenerate_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LLMGenerate_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LLMGenerate_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/action/LLMGenerate_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__LLMGenerate_Feedback() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__LLMGenerate_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__action__LLMGenerate_FeedbackMessage__init(msg: *mut LLMGenerate_FeedbackMessage) -> bool;
    fn aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_FeedbackMessage>, size: usize) -> bool;
    fn aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_FeedbackMessage>);
    fn aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LLMGenerate_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_FeedbackMessage>) -> bool;
}

// Corresponds to aimee_msgs__action__LLMGenerate_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LLMGenerate_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::LLMGenerate_Feedback,

}



impl Default for LLMGenerate_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__action__LLMGenerate_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__action__LLMGenerate_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LLMGenerate_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LLMGenerate_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LLMGenerate_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/action/LLMGenerate_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__LLMGenerate_FeedbackMessage() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__ExecuteSkill_Goal() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__action__ExecuteSkill_Goal__init(msg: *mut ExecuteSkill_Goal) -> bool;
    fn aimee_msgs__action__ExecuteSkill_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_Goal>, size: usize) -> bool;
    fn aimee_msgs__action__ExecuteSkill_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_Goal>);
    fn aimee_msgs__action__ExecuteSkill_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteSkill_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_Goal>) -> bool;
}

// Corresponds to aimee_msgs__action__ExecuteSkill_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSkill_Goal {
    /// Goal: Request to execute a skill
    /// Skill identifier
    pub skill_id: rosidl_runtime_rs::String,

    /// User's command/text
    pub user_input: rosidl_runtime_rs::String,

    /// Current robot state
    pub robot_state: super::super::msg::rmw::RobotState,

    /// JSON string with user context
    pub user_context: rosidl_runtime_rs::String,

    /// Session identifier
    pub session_id: rosidl_runtime_rs::String,

}



impl Default for ExecuteSkill_Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__action__ExecuteSkill_Goal__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__action__ExecuteSkill_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteSkill_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteSkill_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteSkill_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/action/ExecuteSkill_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__ExecuteSkill_Goal() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__ExecuteSkill_Result() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__action__ExecuteSkill_Result__init(msg: *mut ExecuteSkill_Result) -> bool;
    fn aimee_msgs__action__ExecuteSkill_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_Result>, size: usize) -> bool;
    fn aimee_msgs__action__ExecuteSkill_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_Result>);
    fn aimee_msgs__action__ExecuteSkill_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteSkill_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_Result>) -> bool;
}

// Corresponds to aimee_msgs__action__ExecuteSkill_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSkill_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

    /// Text response from skill
    pub response_text: rosidl_runtime_rs::String,

    /// Path to TTS audio file (if generated)
    pub tts_audio_path: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_message: rosidl_runtime_rs::String,

    /// Actions performed
    pub motor_actions: rosidl_runtime_rs::Sequence<super::super::msg::rmw::MotorAction>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub camera_actions: rosidl_runtime_rs::Sequence<super::super::msg::rmw::CameraAction>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub led_actions: rosidl_runtime_rs::Sequence<super::super::msg::rmw::LEDAction>,

}



impl Default for ExecuteSkill_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__action__ExecuteSkill_Result__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__action__ExecuteSkill_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteSkill_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteSkill_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteSkill_Result where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/action/ExecuteSkill_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__ExecuteSkill_Result() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__ExecuteSkill_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__action__ExecuteSkill_Feedback__init(msg: *mut ExecuteSkill_Feedback) -> bool;
    fn aimee_msgs__action__ExecuteSkill_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_Feedback>, size: usize) -> bool;
    fn aimee_msgs__action__ExecuteSkill_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_Feedback>);
    fn aimee_msgs__action__ExecuteSkill_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteSkill_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_Feedback>) -> bool;
}

// Corresponds to aimee_msgs__action__ExecuteSkill_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSkill_Feedback {
    /// "starting" | "executing" | "finalizing"
    pub status: rosidl_runtime_rs::String,

    /// Description of current action
    pub current_action: rosidl_runtime_rs::String,

    /// 0.0 to 1.0
    pub progress: f32,

    /// Whether skill can be cancelled now
    pub can_cancel: bool,

}



impl Default for ExecuteSkill_Feedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__action__ExecuteSkill_Feedback__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__action__ExecuteSkill_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteSkill_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteSkill_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteSkill_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/action/ExecuteSkill_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__ExecuteSkill_Feedback() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__ExecuteSkill_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__action__ExecuteSkill_FeedbackMessage__init(msg: *mut ExecuteSkill_FeedbackMessage) -> bool;
    fn aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_FeedbackMessage>, size: usize) -> bool;
    fn aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_FeedbackMessage>);
    fn aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteSkill_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_FeedbackMessage>) -> bool;
}

// Corresponds to aimee_msgs__action__ExecuteSkill_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSkill_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::ExecuteSkill_Feedback,

}



impl Default for ExecuteSkill_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__action__ExecuteSkill_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__action__ExecuteSkill_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteSkill_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteSkill_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteSkill_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/action/ExecuteSkill_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__ExecuteSkill_FeedbackMessage() }
  }
}




#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__LLMGenerate_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__action__LLMGenerate_SendGoal_Request__init(msg: *mut LLMGenerate_SendGoal_Request) -> bool;
    fn aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_SendGoal_Request>, size: usize) -> bool;
    fn aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_SendGoal_Request>);
    fn aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LLMGenerate_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_SendGoal_Request>) -> bool;
}

// Corresponds to aimee_msgs__action__LLMGenerate_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LLMGenerate_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::LLMGenerate_Goal,

}



impl Default for LLMGenerate_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__action__LLMGenerate_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__action__LLMGenerate_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LLMGenerate_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LLMGenerate_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LLMGenerate_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/action/LLMGenerate_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__LLMGenerate_SendGoal_Request() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__LLMGenerate_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__action__LLMGenerate_SendGoal_Response__init(msg: *mut LLMGenerate_SendGoal_Response) -> bool;
    fn aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_SendGoal_Response>, size: usize) -> bool;
    fn aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_SendGoal_Response>);
    fn aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LLMGenerate_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_SendGoal_Response>) -> bool;
}

// Corresponds to aimee_msgs__action__LLMGenerate_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LLMGenerate_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for LLMGenerate_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__action__LLMGenerate_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__action__LLMGenerate_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LLMGenerate_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LLMGenerate_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LLMGenerate_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/action/LLMGenerate_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__LLMGenerate_SendGoal_Response() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__LLMGenerate_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__action__LLMGenerate_GetResult_Request__init(msg: *mut LLMGenerate_GetResult_Request) -> bool;
    fn aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_GetResult_Request>, size: usize) -> bool;
    fn aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_GetResult_Request>);
    fn aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LLMGenerate_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_GetResult_Request>) -> bool;
}

// Corresponds to aimee_msgs__action__LLMGenerate_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LLMGenerate_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for LLMGenerate_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__action__LLMGenerate_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__action__LLMGenerate_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LLMGenerate_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LLMGenerate_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LLMGenerate_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/action/LLMGenerate_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__LLMGenerate_GetResult_Request() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__LLMGenerate_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__action__LLMGenerate_GetResult_Response__init(msg: *mut LLMGenerate_GetResult_Response) -> bool;
    fn aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_GetResult_Response>, size: usize) -> bool;
    fn aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_GetResult_Response>);
    fn aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LLMGenerate_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<LLMGenerate_GetResult_Response>) -> bool;
}

// Corresponds to aimee_msgs__action__LLMGenerate_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LLMGenerate_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::LLMGenerate_Result,

}



impl Default for LLMGenerate_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__action__LLMGenerate_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__action__LLMGenerate_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LLMGenerate_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__LLMGenerate_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LLMGenerate_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LLMGenerate_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/action/LLMGenerate_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__LLMGenerate_GetResult_Response() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__ExecuteSkill_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__action__ExecuteSkill_SendGoal_Request__init(msg: *mut ExecuteSkill_SendGoal_Request) -> bool;
    fn aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_SendGoal_Request>, size: usize) -> bool;
    fn aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_SendGoal_Request>);
    fn aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteSkill_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_SendGoal_Request>) -> bool;
}

// Corresponds to aimee_msgs__action__ExecuteSkill_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSkill_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::ExecuteSkill_Goal,

}



impl Default for ExecuteSkill_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__action__ExecuteSkill_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__action__ExecuteSkill_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteSkill_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteSkill_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteSkill_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/action/ExecuteSkill_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__ExecuteSkill_SendGoal_Request() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__ExecuteSkill_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__action__ExecuteSkill_SendGoal_Response__init(msg: *mut ExecuteSkill_SendGoal_Response) -> bool;
    fn aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_SendGoal_Response>, size: usize) -> bool;
    fn aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_SendGoal_Response>);
    fn aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteSkill_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_SendGoal_Response>) -> bool;
}

// Corresponds to aimee_msgs__action__ExecuteSkill_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSkill_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for ExecuteSkill_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__action__ExecuteSkill_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__action__ExecuteSkill_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteSkill_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteSkill_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteSkill_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/action/ExecuteSkill_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__ExecuteSkill_SendGoal_Response() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__ExecuteSkill_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__action__ExecuteSkill_GetResult_Request__init(msg: *mut ExecuteSkill_GetResult_Request) -> bool;
    fn aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_GetResult_Request>, size: usize) -> bool;
    fn aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_GetResult_Request>);
    fn aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteSkill_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_GetResult_Request>) -> bool;
}

// Corresponds to aimee_msgs__action__ExecuteSkill_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSkill_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for ExecuteSkill_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__action__ExecuteSkill_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__action__ExecuteSkill_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteSkill_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteSkill_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteSkill_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/action/ExecuteSkill_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__ExecuteSkill_GetResult_Request() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__ExecuteSkill_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__action__ExecuteSkill_GetResult_Response__init(msg: *mut ExecuteSkill_GetResult_Response) -> bool;
    fn aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_GetResult_Response>, size: usize) -> bool;
    fn aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_GetResult_Response>);
    fn aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteSkill_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteSkill_GetResult_Response>) -> bool;
}

// Corresponds to aimee_msgs__action__ExecuteSkill_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSkill_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::ExecuteSkill_Result,

}



impl Default for ExecuteSkill_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__action__ExecuteSkill_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__action__ExecuteSkill_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteSkill_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__action__ExecuteSkill_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteSkill_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteSkill_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/action/ExecuteSkill_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__action__ExecuteSkill_GetResult_Response() }
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


