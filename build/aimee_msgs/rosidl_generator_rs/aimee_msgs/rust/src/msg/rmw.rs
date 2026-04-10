#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__Intent() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__msg__Intent__init(msg: *mut Intent) -> bool;
    fn aimee_msgs__msg__Intent__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Intent>, size: usize) -> bool;
    fn aimee_msgs__msg__Intent__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Intent>);
    fn aimee_msgs__msg__Intent__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Intent>, out_seq: *mut rosidl_runtime_rs::Sequence<Intent>) -> bool;
}

// Corresponds to aimee_msgs__msg__Intent
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Intent classification message
/// Published by: Intent Router
/// Subscribed by: Skills, State Manager

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Intent {
    /// Type of intent (greeting, movement, arm_control, etc.)
    pub intent_type: rosidl_runtime_rs::String,

    /// Specific action (move_forward, wave, etc.)
    pub action: rosidl_runtime_rs::String,

    /// Classification confidence (0.0-1.0)
    pub confidence: f32,

    /// Original user text
    pub raw_text: rosidl_runtime_rs::String,

    /// True if requires skill execution
    pub requires_skill: bool,

    /// Name of skill to execute
    pub skill_name: rosidl_runtime_rs::String,

    /// Action parameters as JSON string
    pub parameters_json: rosidl_runtime_rs::String,

    /// Context
    /// Conversation session ID
    pub session_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub timestamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for Intent {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__msg__Intent__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__msg__Intent__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Intent {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__Intent__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__Intent__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__Intent__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Intent {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Intent where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/msg/Intent";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__Intent() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__Transcription() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__msg__Transcription__init(msg: *mut Transcription) -> bool;
    fn aimee_msgs__msg__Transcription__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Transcription>, size: usize) -> bool;
    fn aimee_msgs__msg__Transcription__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Transcription>);
    fn aimee_msgs__msg__Transcription__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Transcription>, out_seq: *mut rosidl_runtime_rs::Sequence<Transcription>) -> bool;
}

// Corresponds to aimee_msgs__msg__Transcription
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Voice transcription message
/// Published by: Voice Manager (ASR)
/// Subscribed by: Intent Router

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Transcription {
    /// Transcribed text
    pub text: rosidl_runtime_rs::String,

    /// ASR confidence (0.0-1.0)
    pub confidence: f32,

    /// vosk | whisper | cloud
    pub source: rosidl_runtime_rs::String,

    /// True if this is a command (post-wake-word)
    pub is_command: bool,

    /// True if this is a partial result (streaming)
    pub is_partial: bool,

    /// Wake word info
    /// True if preceded by wake word
    pub wake_word_detected: bool,

    /// Which wake word was detected
    pub wake_word: rosidl_runtime_rs::String,

    /// Metadata
    pub timestamp: builtin_interfaces::msg::rmw::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub session_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub correlation_id: rosidl_runtime_rs::String,

}



impl Default for Transcription {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__msg__Transcription__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__msg__Transcription__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Transcription {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__Transcription__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__Transcription__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__Transcription__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Transcription {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Transcription where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/msg/Transcription";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__Transcription() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__RobotState() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__msg__RobotState__init(msg: *mut RobotState) -> bool;
    fn aimee_msgs__msg__RobotState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotState>, size: usize) -> bool;
    fn aimee_msgs__msg__RobotState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotState>);
    fn aimee_msgs__msg__RobotState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotState>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotState>) -> bool;
}

// Corresponds to aimee_msgs__msg__RobotState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Complete robot state message
/// Published by: State Manager (aggregates from all nodes)
/// Subscribed by: Skills, Cloud Bridge

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotState {
    /// Identity
    /// "ron" or "wren"
    pub robot_name: rosidl_runtime_rs::String,

    /// "ugv_arm" | "wave_rover"
    pub robot_type: rosidl_runtime_rs::String,

    /// Power
    /// 0.0 to 100.0
    pub battery_level: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub is_charging: bool,

    /// "normal" | "low" | "critical"
    pub power_status: rosidl_runtime_rs::String,

    /// Motion state
    /// "idle" | "moving" | "executing_skill"
    pub current_action: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub current_velocity: geometry_msgs::msg::rmw::Twist,


    // This member is not documented.
    #[allow(missing_docs)]
    pub odometry: nav_msgs::msg::rmw::Odometry,

    /// Arm state (if applicable)
    pub arm_state: sensor_msgs::msg::rmw::JointState,


    // This member is not documented.
    #[allow(missing_docs)]
    pub arm_is_moving: bool,

    /// "home" | "ready" | "custom"
    pub arm_pose_name: rosidl_runtime_rs::String,

    /// Gripper state
    /// 0.0 (closed) to 1.0 (open)
    pub gripper_position: f32,

    /// Camera state
    /// "idle" | "tracking" | "manual"
    pub camera_mode: rosidl_runtime_rs::String,

    /// "none" | "face" | "body" | "hand"
    pub tracking_target: rosidl_runtime_rs::String,

    /// Active skills
    pub active_skills: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub current_skill_id: rosidl_runtime_rs::String,

    /// System health
    /// List of active errors
    pub errors: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,

    /// List of active warnings
    pub warnings: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,

    /// Metadata
    pub timestamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for RobotState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__msg__RobotState__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__msg__RobotState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__RobotState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__RobotState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__RobotState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotState where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/msg/RobotState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__RobotState() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__FaceDetection() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__msg__FaceDetection__init(msg: *mut FaceDetection) -> bool;
    fn aimee_msgs__msg__FaceDetection__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<FaceDetection>, size: usize) -> bool;
    fn aimee_msgs__msg__FaceDetection__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<FaceDetection>);
    fn aimee_msgs__msg__FaceDetection__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<FaceDetection>, out_seq: *mut rosidl_runtime_rs::Sequence<FaceDetection>) -> bool;
}

// Corresponds to aimee_msgs__msg__FaceDetection
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Face detection message
/// Published by: Vision Manager
/// Subscribed by: Skills, OBSBOT Controller

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FaceDetection {
    /// Face identification
    /// Unique face identifier (or "unknown")
    pub face_id: rosidl_runtime_rs::String,

    /// Name if recognized, "unknown" otherwise
    pub person_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub recognition_confidence: f32,

    /// Face location (normalized coordinates 0.0-1.0)
    pub center_x: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub center_y: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub width: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub height: f32,

    /// Additional face data
    /// Total faces in frame
    pub num_faces_detected: i32,

    /// Optional: facial landmarks
    pub face_landmarks: rosidl_runtime_rs::Sequence<f32>,

    /// 3D position estimate (if available)
    pub position_3d: geometry_msgs::msg::rmw::Point,

    /// Metadata
    pub timestamp: builtin_interfaces::msg::rmw::Time,

    /// "obsbot_main" | "ov7670"
    pub camera_source: rosidl_runtime_rs::String,

}



impl Default for FaceDetection {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__msg__FaceDetection__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__msg__FaceDetection__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for FaceDetection {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__FaceDetection__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__FaceDetection__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__FaceDetection__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for FaceDetection {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for FaceDetection where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/msg/FaceDetection";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__FaceDetection() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__TrackingCommand() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__msg__TrackingCommand__init(msg: *mut TrackingCommand) -> bool;
    fn aimee_msgs__msg__TrackingCommand__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<TrackingCommand>, size: usize) -> bool;
    fn aimee_msgs__msg__TrackingCommand__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<TrackingCommand>);
    fn aimee_msgs__msg__TrackingCommand__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<TrackingCommand>, out_seq: *mut rosidl_runtime_rs::Sequence<TrackingCommand>) -> bool;
}

// Corresponds to aimee_msgs__msg__TrackingCommand
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Camera tracking command message
/// Published by: Skills, Face Recognition
/// Subscribed by: Vision Manager

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct TrackingCommand {
    /// "start" | "stop" | "preset" | "zoom" | "mode"
    pub command: rosidl_runtime_rs::String,

    /// "normal" | "upper_body" | "closeup" | "headless" | "desk" | "whiteboard" | "hand" | "group" | "off"
    pub mode: rosidl_runtime_rs::String,

    /// For "preset" command (1-3)
    pub preset_id: i32,

    /// For "zoom" command (0-100)
    pub zoom_level: i32,

    /// Target to track (for advanced tracking)
    /// "face" | "body" | "hand" | "object"
    pub target_type: rosidl_runtime_rs::String,

    /// Specific target identifier
    pub target_id: rosidl_runtime_rs::String,

    /// Last known position
    pub target_position: geometry_msgs::msg::rmw::Point,

    /// Metadata
    pub timestamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for TrackingCommand {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__msg__TrackingCommand__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__msg__TrackingCommand__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for TrackingCommand {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__TrackingCommand__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__TrackingCommand__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__TrackingCommand__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for TrackingCommand {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for TrackingCommand where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/msg/TrackingCommand";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__TrackingCommand() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__WakeWordDetection() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__msg__WakeWordDetection__init(msg: *mut WakeWordDetection) -> bool;
    fn aimee_msgs__msg__WakeWordDetection__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<WakeWordDetection>, size: usize) -> bool;
    fn aimee_msgs__msg__WakeWordDetection__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<WakeWordDetection>);
    fn aimee_msgs__msg__WakeWordDetection__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<WakeWordDetection>, out_seq: *mut rosidl_runtime_rs::Sequence<WakeWordDetection>) -> bool;
}

// Corresponds to aimee_msgs__msg__WakeWordDetection
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Wake word detection message
/// Published by: Wake Word Detection Brick (keyword spotting)
/// Subscribed by: Voice Manager, State Manager

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WakeWordDetection {
    /// Detected wake word (e.g., "aimee", "hey_aimee")
    pub wake_word: rosidl_runtime_rs::String,

    /// Detection confidence (0.0-1.0)
    pub confidence: f32,

    /// Detection source (e.g., "edge_impulse", "porcupine")
    pub source: rosidl_runtime_rs::String,

    /// Detection context
    /// Audio sample index at detection
    pub sample_index: u16,

    /// Audio signal energy level
    pub signal_energy: f32,

    /// System state
    /// true when wake word is active/triggered
    /// false when wake word session ends
    pub active: bool,

    /// Metadata
    pub timestamp: builtin_interfaces::msg::rmw::Time,

    /// Unique session identifier
    pub session_id: rosidl_runtime_rs::String,

}



impl Default for WakeWordDetection {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__msg__WakeWordDetection__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__msg__WakeWordDetection__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for WakeWordDetection {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__WakeWordDetection__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__WakeWordDetection__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__WakeWordDetection__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for WakeWordDetection {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for WakeWordDetection where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/msg/WakeWordDetection";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__WakeWordDetection() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__MotorAction() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__msg__MotorAction__init(msg: *mut MotorAction) -> bool;
    fn aimee_msgs__msg__MotorAction__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MotorAction>, size: usize) -> bool;
    fn aimee_msgs__msg__MotorAction__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MotorAction>);
    fn aimee_msgs__msg__MotorAction__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MotorAction>, out_seq: *mut rosidl_runtime_rs::Sequence<MotorAction>) -> bool;
}

// Corresponds to aimee_msgs__msg__MotorAction
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Motor action performed by a skill
/// Published in ExecuteSkill result

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MotorAction {
    /// Motor identifier (left_track, right_track, arm_base, etc.)
    pub motor_id: rosidl_runtime_rs::String,

    /// move, stop, rotate, position
    pub action_type: rosidl_runtime_rs::String,

    /// Action values (speed, position, angle)
    pub values: rosidl_runtime_rs::Sequence<f32>,

    /// How long the action took
    pub execution_time: builtin_interfaces::msg::rmw::Duration,

}



impl Default for MotorAction {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__msg__MotorAction__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__msg__MotorAction__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MotorAction {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__MotorAction__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__MotorAction__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__MotorAction__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MotorAction {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MotorAction where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/msg/MotorAction";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__MotorAction() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__CameraAction() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__msg__CameraAction__init(msg: *mut CameraAction) -> bool;
    fn aimee_msgs__msg__CameraAction__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<CameraAction>, size: usize) -> bool;
    fn aimee_msgs__msg__CameraAction__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<CameraAction>);
    fn aimee_msgs__msg__CameraAction__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<CameraAction>, out_seq: *mut rosidl_runtime_rs::Sequence<CameraAction>) -> bool;
}

// Corresponds to aimee_msgs__msg__CameraAction
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Camera action performed by a skill
/// Published in ExecuteSkill result

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CameraAction {
    /// track_face, stop_tracking, look_at_me, etc.
    pub action_type: rosidl_runtime_rs::String,

    /// Target object/person
    pub target: rosidl_runtime_rs::String,

    /// Detection confidence
    pub confidence: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub execution_time: builtin_interfaces::msg::rmw::Duration,

}



impl Default for CameraAction {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__msg__CameraAction__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__msg__CameraAction__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for CameraAction {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__CameraAction__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__CameraAction__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__CameraAction__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for CameraAction {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for CameraAction where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/msg/CameraAction";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__CameraAction() }
  }
}


#[link(name = "aimee_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__LEDAction() -> *const std::ffi::c_void;
}

#[link(name = "aimee_msgs__rosidl_generator_c")]
extern "C" {
    fn aimee_msgs__msg__LEDAction__init(msg: *mut LEDAction) -> bool;
    fn aimee_msgs__msg__LEDAction__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LEDAction>, size: usize) -> bool;
    fn aimee_msgs__msg__LEDAction__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LEDAction>);
    fn aimee_msgs__msg__LEDAction__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LEDAction>, out_seq: *mut rosidl_runtime_rs::Sequence<LEDAction>) -> bool;
}

// Corresponds to aimee_msgs__msg__LEDAction
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// LED action performed by a skill
/// Published in ExecuteSkill result

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LEDAction {
    /// Which LED (matrix, status, etc.)
    pub led_id: rosidl_runtime_rs::String,

    /// RGB color values
    pub color: rosidl_runtime_rs::Sequence<u8>,

    /// solid, blink, pulse, rainbow
    pub pattern: rosidl_runtime_rs::String,

    /// How long to display
    pub duration_sec: f32,

}



impl Default for LEDAction {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !aimee_msgs__msg__LEDAction__init(&mut msg as *mut _) {
        panic!("Call to aimee_msgs__msg__LEDAction__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LEDAction {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__LEDAction__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__LEDAction__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { aimee_msgs__msg__LEDAction__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LEDAction {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LEDAction where Self: Sized {
  const TYPE_NAME: &'static str = "aimee_msgs/msg/LEDAction";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__aimee_msgs__msg__LEDAction() }
  }
}


