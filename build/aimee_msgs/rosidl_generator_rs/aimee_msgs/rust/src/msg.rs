#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to aimee_msgs__msg__Intent
/// Intent classification message
/// Published by: Intent Router
/// Subscribed by: Skills, State Manager

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Intent {
    /// Type of intent (greeting, movement, arm_control, etc.)
    pub intent_type: std::string::String,

    /// Specific action (move_forward, wave, etc.)
    pub action: std::string::String,

    /// Classification confidence (0.0-1.0)
    pub confidence: f32,

    /// Original user text
    pub raw_text: std::string::String,

    /// True if requires skill execution
    pub requires_skill: bool,

    /// Name of skill to execute
    pub skill_name: std::string::String,

    /// Action parameters as JSON string
    pub parameters_json: std::string::String,

    /// Context
    /// Conversation session ID
    pub session_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub timestamp: builtin_interfaces::msg::Time,

}



impl Default for Intent {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Intent::default())
  }
}

impl rosidl_runtime_rs::Message for Intent {
  type RmwMsg = super::msg::rmw::Intent;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        intent_type: msg.intent_type.as_str().into(),
        action: msg.action.as_str().into(),
        confidence: msg.confidence,
        raw_text: msg.raw_text.as_str().into(),
        requires_skill: msg.requires_skill,
        skill_name: msg.skill_name.as_str().into(),
        parameters_json: msg.parameters_json.as_str().into(),
        session_id: msg.session_id.as_str().into(),
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.timestamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        intent_type: msg.intent_type.as_str().into(),
        action: msg.action.as_str().into(),
      confidence: msg.confidence,
        raw_text: msg.raw_text.as_str().into(),
      requires_skill: msg.requires_skill,
        skill_name: msg.skill_name.as_str().into(),
        parameters_json: msg.parameters_json.as_str().into(),
        session_id: msg.session_id.as_str().into(),
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.timestamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      intent_type: msg.intent_type.to_string(),
      action: msg.action.to_string(),
      confidence: msg.confidence,
      raw_text: msg.raw_text.to_string(),
      requires_skill: msg.requires_skill,
      skill_name: msg.skill_name.to_string(),
      parameters_json: msg.parameters_json.to_string(),
      session_id: msg.session_id.to_string(),
      timestamp: builtin_interfaces::msg::Time::from_rmw_message(msg.timestamp),
    }
  }
}


// Corresponds to aimee_msgs__msg__Transcription
/// Voice transcription message
/// Published by: Voice Manager (ASR)
/// Subscribed by: Intent Router

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Transcription {
    /// Transcribed text
    pub text: std::string::String,

    /// ASR confidence (0.0-1.0)
    pub confidence: f32,

    /// vosk | whisper | cloud
    pub source: std::string::String,

    /// True if this is a command (post-wake-word)
    pub is_command: bool,

    /// True if this is a partial result (streaming)
    pub is_partial: bool,

    /// Wake word info
    /// True if preceded by wake word
    pub wake_word_detected: bool,

    /// Which wake word was detected
    pub wake_word: std::string::String,

    /// Metadata
    pub timestamp: builtin_interfaces::msg::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub session_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub correlation_id: std::string::String,

}



impl Default for Transcription {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Transcription::default())
  }
}

impl rosidl_runtime_rs::Message for Transcription {
  type RmwMsg = super::msg::rmw::Transcription;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        text: msg.text.as_str().into(),
        confidence: msg.confidence,
        source: msg.source.as_str().into(),
        is_command: msg.is_command,
        is_partial: msg.is_partial,
        wake_word_detected: msg.wake_word_detected,
        wake_word: msg.wake_word.as_str().into(),
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.timestamp)).into_owned(),
        session_id: msg.session_id.as_str().into(),
        correlation_id: msg.correlation_id.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        text: msg.text.as_str().into(),
      confidence: msg.confidence,
        source: msg.source.as_str().into(),
      is_command: msg.is_command,
      is_partial: msg.is_partial,
      wake_word_detected: msg.wake_word_detected,
        wake_word: msg.wake_word.as_str().into(),
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.timestamp)).into_owned(),
        session_id: msg.session_id.as_str().into(),
        correlation_id: msg.correlation_id.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      text: msg.text.to_string(),
      confidence: msg.confidence,
      source: msg.source.to_string(),
      is_command: msg.is_command,
      is_partial: msg.is_partial,
      wake_word_detected: msg.wake_word_detected,
      wake_word: msg.wake_word.to_string(),
      timestamp: builtin_interfaces::msg::Time::from_rmw_message(msg.timestamp),
      session_id: msg.session_id.to_string(),
      correlation_id: msg.correlation_id.to_string(),
    }
  }
}


// Corresponds to aimee_msgs__msg__RobotState
/// Complete robot state message
/// Published by: State Manager (aggregates from all nodes)
/// Subscribed by: Skills, Cloud Bridge

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotState {
    /// Identity
    /// "ron" or "wren"
    pub robot_name: std::string::String,

    /// "ugv_arm" | "wave_rover"
    pub robot_type: std::string::String,

    /// Power
    /// 0.0 to 100.0
    pub battery_level: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub is_charging: bool,

    /// "normal" | "low" | "critical"
    pub power_status: std::string::String,

    /// Motion state
    /// "idle" | "moving" | "executing_skill"
    pub current_action: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub current_velocity: geometry_msgs::msg::Twist,


    // This member is not documented.
    #[allow(missing_docs)]
    pub odometry: nav_msgs::msg::Odometry,

    /// Arm state (if applicable)
    pub arm_state: sensor_msgs::msg::JointState,


    // This member is not documented.
    #[allow(missing_docs)]
    pub arm_is_moving: bool,

    /// "home" | "ready" | "custom"
    pub arm_pose_name: std::string::String,

    /// Gripper state
    /// 0.0 (closed) to 1.0 (open)
    pub gripper_position: f32,

    /// Camera state
    /// "idle" | "tracking" | "manual"
    pub camera_mode: std::string::String,

    /// "none" | "face" | "body" | "hand"
    pub tracking_target: std::string::String,

    /// Active skills
    pub active_skills: Vec<std::string::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub current_skill_id: std::string::String,

    /// System health
    /// List of active errors
    pub errors: Vec<std::string::String>,

    /// List of active warnings
    pub warnings: Vec<std::string::String>,

    /// Metadata
    pub timestamp: builtin_interfaces::msg::Time,

}



impl Default for RobotState {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RobotState::default())
  }
}

impl rosidl_runtime_rs::Message for RobotState {
  type RmwMsg = super::msg::rmw::RobotState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        robot_name: msg.robot_name.as_str().into(),
        robot_type: msg.robot_type.as_str().into(),
        battery_level: msg.battery_level,
        is_charging: msg.is_charging,
        power_status: msg.power_status.as_str().into(),
        current_action: msg.current_action.as_str().into(),
        current_velocity: geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Owned(msg.current_velocity)).into_owned(),
        odometry: nav_msgs::msg::Odometry::into_rmw_message(std::borrow::Cow::Owned(msg.odometry)).into_owned(),
        arm_state: sensor_msgs::msg::JointState::into_rmw_message(std::borrow::Cow::Owned(msg.arm_state)).into_owned(),
        arm_is_moving: msg.arm_is_moving,
        arm_pose_name: msg.arm_pose_name.as_str().into(),
        gripper_position: msg.gripper_position,
        camera_mode: msg.camera_mode.as_str().into(),
        tracking_target: msg.tracking_target.as_str().into(),
        active_skills: msg.active_skills
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        current_skill_id: msg.current_skill_id.as_str().into(),
        errors: msg.errors
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        warnings: msg.warnings
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.timestamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        robot_name: msg.robot_name.as_str().into(),
        robot_type: msg.robot_type.as_str().into(),
      battery_level: msg.battery_level,
      is_charging: msg.is_charging,
        power_status: msg.power_status.as_str().into(),
        current_action: msg.current_action.as_str().into(),
        current_velocity: geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Borrowed(&msg.current_velocity)).into_owned(),
        odometry: nav_msgs::msg::Odometry::into_rmw_message(std::borrow::Cow::Borrowed(&msg.odometry)).into_owned(),
        arm_state: sensor_msgs::msg::JointState::into_rmw_message(std::borrow::Cow::Borrowed(&msg.arm_state)).into_owned(),
      arm_is_moving: msg.arm_is_moving,
        arm_pose_name: msg.arm_pose_name.as_str().into(),
      gripper_position: msg.gripper_position,
        camera_mode: msg.camera_mode.as_str().into(),
        tracking_target: msg.tracking_target.as_str().into(),
        active_skills: msg.active_skills
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        current_skill_id: msg.current_skill_id.as_str().into(),
        errors: msg.errors
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        warnings: msg.warnings
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.timestamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      robot_name: msg.robot_name.to_string(),
      robot_type: msg.robot_type.to_string(),
      battery_level: msg.battery_level,
      is_charging: msg.is_charging,
      power_status: msg.power_status.to_string(),
      current_action: msg.current_action.to_string(),
      current_velocity: geometry_msgs::msg::Twist::from_rmw_message(msg.current_velocity),
      odometry: nav_msgs::msg::Odometry::from_rmw_message(msg.odometry),
      arm_state: sensor_msgs::msg::JointState::from_rmw_message(msg.arm_state),
      arm_is_moving: msg.arm_is_moving,
      arm_pose_name: msg.arm_pose_name.to_string(),
      gripper_position: msg.gripper_position,
      camera_mode: msg.camera_mode.to_string(),
      tracking_target: msg.tracking_target.to_string(),
      active_skills: msg.active_skills
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      current_skill_id: msg.current_skill_id.to_string(),
      errors: msg.errors
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      warnings: msg.warnings
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      timestamp: builtin_interfaces::msg::Time::from_rmw_message(msg.timestamp),
    }
  }
}


// Corresponds to aimee_msgs__msg__FaceDetection
/// Face detection message
/// Published by: Vision Manager
/// Subscribed by: Skills, OBSBOT Controller

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FaceDetection {
    /// Face identification
    /// Unique face identifier (or "unknown")
    pub face_id: std::string::String,

    /// Name if recognized, "unknown" otherwise
    pub person_name: std::string::String,


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
    pub face_landmarks: Vec<f32>,

    /// 3D position estimate (if available)
    pub position_3d: geometry_msgs::msg::Point,

    /// Metadata
    pub timestamp: builtin_interfaces::msg::Time,

    /// "obsbot_main" | "ov7670"
    pub camera_source: std::string::String,

}



impl Default for FaceDetection {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::FaceDetection::default())
  }
}

impl rosidl_runtime_rs::Message for FaceDetection {
  type RmwMsg = super::msg::rmw::FaceDetection;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        face_id: msg.face_id.as_str().into(),
        person_name: msg.person_name.as_str().into(),
        recognition_confidence: msg.recognition_confidence,
        center_x: msg.center_x,
        center_y: msg.center_y,
        width: msg.width,
        height: msg.height,
        num_faces_detected: msg.num_faces_detected,
        face_landmarks: msg.face_landmarks.into(),
        position_3d: geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Owned(msg.position_3d)).into_owned(),
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.timestamp)).into_owned(),
        camera_source: msg.camera_source.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        face_id: msg.face_id.as_str().into(),
        person_name: msg.person_name.as_str().into(),
      recognition_confidence: msg.recognition_confidence,
      center_x: msg.center_x,
      center_y: msg.center_y,
      width: msg.width,
      height: msg.height,
      num_faces_detected: msg.num_faces_detected,
        face_landmarks: msg.face_landmarks.as_slice().into(),
        position_3d: geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Borrowed(&msg.position_3d)).into_owned(),
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.timestamp)).into_owned(),
        camera_source: msg.camera_source.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      face_id: msg.face_id.to_string(),
      person_name: msg.person_name.to_string(),
      recognition_confidence: msg.recognition_confidence,
      center_x: msg.center_x,
      center_y: msg.center_y,
      width: msg.width,
      height: msg.height,
      num_faces_detected: msg.num_faces_detected,
      face_landmarks: msg.face_landmarks
          .into_iter()
          .collect(),
      position_3d: geometry_msgs::msg::Point::from_rmw_message(msg.position_3d),
      timestamp: builtin_interfaces::msg::Time::from_rmw_message(msg.timestamp),
      camera_source: msg.camera_source.to_string(),
    }
  }
}


// Corresponds to aimee_msgs__msg__TrackingCommand
/// Camera tracking command message
/// Published by: Skills, Face Recognition
/// Subscribed by: Vision Manager

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct TrackingCommand {
    /// "start" | "stop" | "preset" | "zoom" | "mode"
    pub command: std::string::String,

    /// "normal" | "upper_body" | "closeup" | "headless" | "desk" | "whiteboard" | "hand" | "group" | "off"
    pub mode: std::string::String,

    /// For "preset" command (1-3)
    pub preset_id: i32,

    /// For "zoom" command (0-100)
    pub zoom_level: i32,

    /// Target to track (for advanced tracking)
    /// "face" | "body" | "hand" | "object"
    pub target_type: std::string::String,

    /// Specific target identifier
    pub target_id: std::string::String,

    /// Last known position
    pub target_position: geometry_msgs::msg::Point,

    /// Metadata
    pub timestamp: builtin_interfaces::msg::Time,

}



impl Default for TrackingCommand {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::TrackingCommand::default())
  }
}

impl rosidl_runtime_rs::Message for TrackingCommand {
  type RmwMsg = super::msg::rmw::TrackingCommand;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        command: msg.command.as_str().into(),
        mode: msg.mode.as_str().into(),
        preset_id: msg.preset_id,
        zoom_level: msg.zoom_level,
        target_type: msg.target_type.as_str().into(),
        target_id: msg.target_id.as_str().into(),
        target_position: geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Owned(msg.target_position)).into_owned(),
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.timestamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        command: msg.command.as_str().into(),
        mode: msg.mode.as_str().into(),
      preset_id: msg.preset_id,
      zoom_level: msg.zoom_level,
        target_type: msg.target_type.as_str().into(),
        target_id: msg.target_id.as_str().into(),
        target_position: geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Borrowed(&msg.target_position)).into_owned(),
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.timestamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      command: msg.command.to_string(),
      mode: msg.mode.to_string(),
      preset_id: msg.preset_id,
      zoom_level: msg.zoom_level,
      target_type: msg.target_type.to_string(),
      target_id: msg.target_id.to_string(),
      target_position: geometry_msgs::msg::Point::from_rmw_message(msg.target_position),
      timestamp: builtin_interfaces::msg::Time::from_rmw_message(msg.timestamp),
    }
  }
}


// Corresponds to aimee_msgs__msg__WakeWordDetection
/// Wake word detection message
/// Published by: Wake Word Detection Brick (keyword spotting)
/// Subscribed by: Voice Manager, State Manager

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WakeWordDetection {
    /// Detected wake word (e.g., "aimee", "hey_aimee")
    pub wake_word: std::string::String,

    /// Detection confidence (0.0-1.0)
    pub confidence: f32,

    /// Detection source (e.g., "edge_impulse", "porcupine")
    pub source: std::string::String,

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
    pub timestamp: builtin_interfaces::msg::Time,

    /// Unique session identifier
    pub session_id: std::string::String,

}



impl Default for WakeWordDetection {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::WakeWordDetection::default())
  }
}

impl rosidl_runtime_rs::Message for WakeWordDetection {
  type RmwMsg = super::msg::rmw::WakeWordDetection;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        wake_word: msg.wake_word.as_str().into(),
        confidence: msg.confidence,
        source: msg.source.as_str().into(),
        sample_index: msg.sample_index,
        signal_energy: msg.signal_energy,
        active: msg.active,
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.timestamp)).into_owned(),
        session_id: msg.session_id.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        wake_word: msg.wake_word.as_str().into(),
      confidence: msg.confidence,
        source: msg.source.as_str().into(),
      sample_index: msg.sample_index,
      signal_energy: msg.signal_energy,
      active: msg.active,
        timestamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.timestamp)).into_owned(),
        session_id: msg.session_id.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      wake_word: msg.wake_word.to_string(),
      confidence: msg.confidence,
      source: msg.source.to_string(),
      sample_index: msg.sample_index,
      signal_energy: msg.signal_energy,
      active: msg.active,
      timestamp: builtin_interfaces::msg::Time::from_rmw_message(msg.timestamp),
      session_id: msg.session_id.to_string(),
    }
  }
}


// Corresponds to aimee_msgs__msg__MotorAction
/// Motor action performed by a skill
/// Published in ExecuteSkill result

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MotorAction {
    /// Motor identifier (left_track, right_track, arm_base, etc.)
    pub motor_id: std::string::String,

    /// move, stop, rotate, position
    pub action_type: std::string::String,

    /// Action values (speed, position, angle)
    pub values: Vec<f32>,

    /// How long the action took
    pub execution_time: builtin_interfaces::msg::Duration,

}



impl Default for MotorAction {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::MotorAction::default())
  }
}

impl rosidl_runtime_rs::Message for MotorAction {
  type RmwMsg = super::msg::rmw::MotorAction;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        motor_id: msg.motor_id.as_str().into(),
        action_type: msg.action_type.as_str().into(),
        values: msg.values.into(),
        execution_time: builtin_interfaces::msg::Duration::into_rmw_message(std::borrow::Cow::Owned(msg.execution_time)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        motor_id: msg.motor_id.as_str().into(),
        action_type: msg.action_type.as_str().into(),
        values: msg.values.as_slice().into(),
        execution_time: builtin_interfaces::msg::Duration::into_rmw_message(std::borrow::Cow::Borrowed(&msg.execution_time)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      motor_id: msg.motor_id.to_string(),
      action_type: msg.action_type.to_string(),
      values: msg.values
          .into_iter()
          .collect(),
      execution_time: builtin_interfaces::msg::Duration::from_rmw_message(msg.execution_time),
    }
  }
}


