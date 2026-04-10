// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aimee_msgs:msg/FaceDetection.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__FACE_DETECTION__TRAITS_HPP_
#define AIMEE_MSGS__MSG__DETAIL__FACE_DETECTION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aimee_msgs/msg/detail/face_detection__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'position_3d'
#include "geometry_msgs/msg/detail/point__traits.hpp"
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace aimee_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const FaceDetection & msg,
  std::ostream & out)
{
  out << "{";
  // member: face_id
  {
    out << "face_id: ";
    rosidl_generator_traits::value_to_yaml(msg.face_id, out);
    out << ", ";
  }

  // member: person_name
  {
    out << "person_name: ";
    rosidl_generator_traits::value_to_yaml(msg.person_name, out);
    out << ", ";
  }

  // member: recognition_confidence
  {
    out << "recognition_confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.recognition_confidence, out);
    out << ", ";
  }

  // member: center_x
  {
    out << "center_x: ";
    rosidl_generator_traits::value_to_yaml(msg.center_x, out);
    out << ", ";
  }

  // member: center_y
  {
    out << "center_y: ";
    rosidl_generator_traits::value_to_yaml(msg.center_y, out);
    out << ", ";
  }

  // member: width
  {
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << ", ";
  }

  // member: height
  {
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
    out << ", ";
  }

  // member: num_faces_detected
  {
    out << "num_faces_detected: ";
    rosidl_generator_traits::value_to_yaml(msg.num_faces_detected, out);
    out << ", ";
  }

  // member: face_landmarks
  {
    if (msg.face_landmarks.size() == 0) {
      out << "face_landmarks: []";
    } else {
      out << "face_landmarks: [";
      size_t pending_items = msg.face_landmarks.size();
      for (auto item : msg.face_landmarks) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: position_3d
  {
    out << "position_3d: ";
    to_flow_style_yaml(msg.position_3d, out);
    out << ", ";
  }

  // member: timestamp
  {
    out << "timestamp: ";
    to_flow_style_yaml(msg.timestamp, out);
    out << ", ";
  }

  // member: camera_source
  {
    out << "camera_source: ";
    rosidl_generator_traits::value_to_yaml(msg.camera_source, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const FaceDetection & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: face_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "face_id: ";
    rosidl_generator_traits::value_to_yaml(msg.face_id, out);
    out << "\n";
  }

  // member: person_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "person_name: ";
    rosidl_generator_traits::value_to_yaml(msg.person_name, out);
    out << "\n";
  }

  // member: recognition_confidence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "recognition_confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.recognition_confidence, out);
    out << "\n";
  }

  // member: center_x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "center_x: ";
    rosidl_generator_traits::value_to_yaml(msg.center_x, out);
    out << "\n";
  }

  // member: center_y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "center_y: ";
    rosidl_generator_traits::value_to_yaml(msg.center_y, out);
    out << "\n";
  }

  // member: width
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << "\n";
  }

  // member: height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
    out << "\n";
  }

  // member: num_faces_detected
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "num_faces_detected: ";
    rosidl_generator_traits::value_to_yaml(msg.num_faces_detected, out);
    out << "\n";
  }

  // member: face_landmarks
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.face_landmarks.size() == 0) {
      out << "face_landmarks: []\n";
    } else {
      out << "face_landmarks:\n";
      for (auto item : msg.face_landmarks) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: position_3d
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "position_3d:\n";
    to_block_style_yaml(msg.position_3d, out, indentation + 2);
  }

  // member: timestamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "timestamp:\n";
    to_block_style_yaml(msg.timestamp, out, indentation + 2);
  }

  // member: camera_source
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "camera_source: ";
    rosidl_generator_traits::value_to_yaml(msg.camera_source, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const FaceDetection & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace aimee_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aimee_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aimee_msgs::msg::FaceDetection & msg,
  std::ostream & out, size_t indentation = 0)
{
  aimee_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aimee_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const aimee_msgs::msg::FaceDetection & msg)
{
  return aimee_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aimee_msgs::msg::FaceDetection>()
{
  return "aimee_msgs::msg::FaceDetection";
}

template<>
inline const char * name<aimee_msgs::msg::FaceDetection>()
{
  return "aimee_msgs/msg/FaceDetection";
}

template<>
struct has_fixed_size<aimee_msgs::msg::FaceDetection>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aimee_msgs::msg::FaceDetection>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aimee_msgs::msg::FaceDetection>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AIMEE_MSGS__MSG__DETAIL__FACE_DETECTION__TRAITS_HPP_
