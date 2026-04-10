// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aimee_msgs:msg/FaceDetection.idl
// generated code does not contain a copyright notice

#ifndef AIMEE_MSGS__MSG__DETAIL__FACE_DETECTION__STRUCT_HPP_
#define AIMEE_MSGS__MSG__DETAIL__FACE_DETECTION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'position_3d'
#include "geometry_msgs/msg/detail/point__struct.hpp"
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aimee_msgs__msg__FaceDetection __attribute__((deprecated))
#else
# define DEPRECATED__aimee_msgs__msg__FaceDetection __declspec(deprecated)
#endif

namespace aimee_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct FaceDetection_
{
  using Type = FaceDetection_<ContainerAllocator>;

  explicit FaceDetection_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : position_3d(_init),
    timestamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->face_id = "";
      this->person_name = "";
      this->recognition_confidence = 0.0f;
      this->center_x = 0.0f;
      this->center_y = 0.0f;
      this->width = 0.0f;
      this->height = 0.0f;
      this->num_faces_detected = 0l;
      this->camera_source = "";
    }
  }

  explicit FaceDetection_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : face_id(_alloc),
    person_name(_alloc),
    position_3d(_alloc, _init),
    timestamp(_alloc, _init),
    camera_source(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->face_id = "";
      this->person_name = "";
      this->recognition_confidence = 0.0f;
      this->center_x = 0.0f;
      this->center_y = 0.0f;
      this->width = 0.0f;
      this->height = 0.0f;
      this->num_faces_detected = 0l;
      this->camera_source = "";
    }
  }

  // field types and members
  using _face_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _face_id_type face_id;
  using _person_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _person_name_type person_name;
  using _recognition_confidence_type =
    float;
  _recognition_confidence_type recognition_confidence;
  using _center_x_type =
    float;
  _center_x_type center_x;
  using _center_y_type =
    float;
  _center_y_type center_y;
  using _width_type =
    float;
  _width_type width;
  using _height_type =
    float;
  _height_type height;
  using _num_faces_detected_type =
    int32_t;
  _num_faces_detected_type num_faces_detected;
  using _face_landmarks_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _face_landmarks_type face_landmarks;
  using _position_3d_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _position_3d_type position_3d;
  using _timestamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _timestamp_type timestamp;
  using _camera_source_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _camera_source_type camera_source;

  // setters for named parameter idiom
  Type & set__face_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->face_id = _arg;
    return *this;
  }
  Type & set__person_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->person_name = _arg;
    return *this;
  }
  Type & set__recognition_confidence(
    const float & _arg)
  {
    this->recognition_confidence = _arg;
    return *this;
  }
  Type & set__center_x(
    const float & _arg)
  {
    this->center_x = _arg;
    return *this;
  }
  Type & set__center_y(
    const float & _arg)
  {
    this->center_y = _arg;
    return *this;
  }
  Type & set__width(
    const float & _arg)
  {
    this->width = _arg;
    return *this;
  }
  Type & set__height(
    const float & _arg)
  {
    this->height = _arg;
    return *this;
  }
  Type & set__num_faces_detected(
    const int32_t & _arg)
  {
    this->num_faces_detected = _arg;
    return *this;
  }
  Type & set__face_landmarks(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->face_landmarks = _arg;
    return *this;
  }
  Type & set__position_3d(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->position_3d = _arg;
    return *this;
  }
  Type & set__timestamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->timestamp = _arg;
    return *this;
  }
  Type & set__camera_source(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->camera_source = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aimee_msgs::msg::FaceDetection_<ContainerAllocator> *;
  using ConstRawPtr =
    const aimee_msgs::msg::FaceDetection_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aimee_msgs::msg::FaceDetection_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aimee_msgs::msg::FaceDetection_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::FaceDetection_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::FaceDetection_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aimee_msgs::msg::FaceDetection_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aimee_msgs::msg::FaceDetection_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aimee_msgs::msg::FaceDetection_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aimee_msgs::msg::FaceDetection_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aimee_msgs__msg__FaceDetection
    std::shared_ptr<aimee_msgs::msg::FaceDetection_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aimee_msgs__msg__FaceDetection
    std::shared_ptr<aimee_msgs::msg::FaceDetection_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FaceDetection_ & other) const
  {
    if (this->face_id != other.face_id) {
      return false;
    }
    if (this->person_name != other.person_name) {
      return false;
    }
    if (this->recognition_confidence != other.recognition_confidence) {
      return false;
    }
    if (this->center_x != other.center_x) {
      return false;
    }
    if (this->center_y != other.center_y) {
      return false;
    }
    if (this->width != other.width) {
      return false;
    }
    if (this->height != other.height) {
      return false;
    }
    if (this->num_faces_detected != other.num_faces_detected) {
      return false;
    }
    if (this->face_landmarks != other.face_landmarks) {
      return false;
    }
    if (this->position_3d != other.position_3d) {
      return false;
    }
    if (this->timestamp != other.timestamp) {
      return false;
    }
    if (this->camera_source != other.camera_source) {
      return false;
    }
    return true;
  }
  bool operator!=(const FaceDetection_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FaceDetection_

// alias to use template instance with default allocator
using FaceDetection =
  aimee_msgs::msg::FaceDetection_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aimee_msgs

#endif  // AIMEE_MSGS__MSG__DETAIL__FACE_DETECTION__STRUCT_HPP_
