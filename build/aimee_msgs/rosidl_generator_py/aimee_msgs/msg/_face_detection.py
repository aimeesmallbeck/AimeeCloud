# generated from rosidl_generator_py/resource/_idl.py.em
# with input from aimee_msgs:msg/FaceDetection.idl
# generated code does not contain a copyright notice


# Import statements for member types

# Member 'face_landmarks'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_FaceDetection(type):
    """Metaclass of message 'FaceDetection'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('aimee_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'aimee_msgs.msg.FaceDetection')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__face_detection
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__face_detection
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__face_detection
            cls._TYPE_SUPPORT = module.type_support_msg__msg__face_detection
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__face_detection

            from builtin_interfaces.msg import Time
            if Time.__class__._TYPE_SUPPORT is None:
                Time.__class__.__import_type_support__()

            from geometry_msgs.msg import Point
            if Point.__class__._TYPE_SUPPORT is None:
                Point.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class FaceDetection(metaclass=Metaclass_FaceDetection):
    """Message class 'FaceDetection'."""

    __slots__ = [
        '_face_id',
        '_person_name',
        '_recognition_confidence',
        '_center_x',
        '_center_y',
        '_width',
        '_height',
        '_num_faces_detected',
        '_face_landmarks',
        '_position_3d',
        '_timestamp',
        '_camera_source',
    ]

    _fields_and_field_types = {
        'face_id': 'string',
        'person_name': 'string',
        'recognition_confidence': 'float',
        'center_x': 'float',
        'center_y': 'float',
        'width': 'float',
        'height': 'float',
        'num_faces_detected': 'int32',
        'face_landmarks': 'sequence<float>',
        'position_3d': 'geometry_msgs/Point',
        'timestamp': 'builtin_interfaces/Time',
        'camera_source': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('float')),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Point'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.face_id = kwargs.get('face_id', str())
        self.person_name = kwargs.get('person_name', str())
        self.recognition_confidence = kwargs.get('recognition_confidence', float())
        self.center_x = kwargs.get('center_x', float())
        self.center_y = kwargs.get('center_y', float())
        self.width = kwargs.get('width', float())
        self.height = kwargs.get('height', float())
        self.num_faces_detected = kwargs.get('num_faces_detected', int())
        self.face_landmarks = array.array('f', kwargs.get('face_landmarks', []))
        from geometry_msgs.msg import Point
        self.position_3d = kwargs.get('position_3d', Point())
        from builtin_interfaces.msg import Time
        self.timestamp = kwargs.get('timestamp', Time())
        self.camera_source = kwargs.get('camera_source', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.face_id != other.face_id:
            return False
        if self.person_name != other.person_name:
            return False
        if self.recognition_confidence != other.recognition_confidence:
            return False
        if self.center_x != other.center_x:
            return False
        if self.center_y != other.center_y:
            return False
        if self.width != other.width:
            return False
        if self.height != other.height:
            return False
        if self.num_faces_detected != other.num_faces_detected:
            return False
        if self.face_landmarks != other.face_landmarks:
            return False
        if self.position_3d != other.position_3d:
            return False
        if self.timestamp != other.timestamp:
            return False
        if self.camera_source != other.camera_source:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def face_id(self):
        """Message field 'face_id'."""
        return self._face_id

    @face_id.setter
    def face_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'face_id' field must be of type 'str'"
        self._face_id = value

    @builtins.property
    def person_name(self):
        """Message field 'person_name'."""
        return self._person_name

    @person_name.setter
    def person_name(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'person_name' field must be of type 'str'"
        self._person_name = value

    @builtins.property
    def recognition_confidence(self):
        """Message field 'recognition_confidence'."""
        return self._recognition_confidence

    @recognition_confidence.setter
    def recognition_confidence(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'recognition_confidence' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'recognition_confidence' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._recognition_confidence = value

    @builtins.property
    def center_x(self):
        """Message field 'center_x'."""
        return self._center_x

    @center_x.setter
    def center_x(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'center_x' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'center_x' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._center_x = value

    @builtins.property
    def center_y(self):
        """Message field 'center_y'."""
        return self._center_y

    @center_y.setter
    def center_y(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'center_y' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'center_y' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._center_y = value

    @builtins.property
    def width(self):
        """Message field 'width'."""
        return self._width

    @width.setter
    def width(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'width' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'width' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._width = value

    @builtins.property
    def height(self):
        """Message field 'height'."""
        return self._height

    @height.setter
    def height(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'height' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'height' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._height = value

    @builtins.property
    def num_faces_detected(self):
        """Message field 'num_faces_detected'."""
        return self._num_faces_detected

    @num_faces_detected.setter
    def num_faces_detected(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'num_faces_detected' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'num_faces_detected' field must be an integer in [-2147483648, 2147483647]"
        self._num_faces_detected = value

    @builtins.property
    def face_landmarks(self):
        """Message field 'face_landmarks'."""
        return self._face_landmarks

    @face_landmarks.setter
    def face_landmarks(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'f', \
                "The 'face_landmarks' array.array() must have the type code of 'f'"
            self._face_landmarks = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -3.402823466e+38 or val > 3.402823466e+38) or math.isinf(val) for val in value)), \
                "The 'face_landmarks' field must be a set or sequence and each value of type 'float' and each float in [-340282346600000016151267322115014000640.000000, 340282346600000016151267322115014000640.000000]"
        self._face_landmarks = array.array('f', value)

    @builtins.property
    def position_3d(self):
        """Message field 'position_3d'."""
        return self._position_3d

    @position_3d.setter
    def position_3d(self, value):
        if __debug__:
            from geometry_msgs.msg import Point
            assert \
                isinstance(value, Point), \
                "The 'position_3d' field must be a sub message of type 'Point'"
        self._position_3d = value

    @builtins.property
    def timestamp(self):
        """Message field 'timestamp'."""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        if __debug__:
            from builtin_interfaces.msg import Time
            assert \
                isinstance(value, Time), \
                "The 'timestamp' field must be a sub message of type 'Time'"
        self._timestamp = value

    @builtins.property
    def camera_source(self):
        """Message field 'camera_source'."""
        return self._camera_source

    @camera_source.setter
    def camera_source(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'camera_source' field must be of type 'str'"
        self._camera_source = value
