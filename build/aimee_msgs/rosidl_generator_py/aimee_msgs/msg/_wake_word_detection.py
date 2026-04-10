# generated from rosidl_generator_py/resource/_idl.py.em
# with input from aimee_msgs:msg/WakeWordDetection.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_WakeWordDetection(type):
    """Metaclass of message 'WakeWordDetection'."""

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
                'aimee_msgs.msg.WakeWordDetection')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__wake_word_detection
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__wake_word_detection
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__wake_word_detection
            cls._TYPE_SUPPORT = module.type_support_msg__msg__wake_word_detection
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__wake_word_detection

            from builtin_interfaces.msg import Time
            if Time.__class__._TYPE_SUPPORT is None:
                Time.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class WakeWordDetection(metaclass=Metaclass_WakeWordDetection):
    """Message class 'WakeWordDetection'."""

    __slots__ = [
        '_wake_word',
        '_confidence',
        '_source',
        '_sample_index',
        '_signal_energy',
        '_active',
        '_timestamp',
        '_session_id',
    ]

    _fields_and_field_types = {
        'wake_word': 'string',
        'confidence': 'float',
        'source': 'string',
        'sample_index': 'uint16',
        'signal_energy': 'float',
        'active': 'boolean',
        'timestamp': 'builtin_interfaces/Time',
        'session_id': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint16'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.wake_word = kwargs.get('wake_word', str())
        self.confidence = kwargs.get('confidence', float())
        self.source = kwargs.get('source', str())
        self.sample_index = kwargs.get('sample_index', int())
        self.signal_energy = kwargs.get('signal_energy', float())
        self.active = kwargs.get('active', bool())
        from builtin_interfaces.msg import Time
        self.timestamp = kwargs.get('timestamp', Time())
        self.session_id = kwargs.get('session_id', str())

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
        if self.wake_word != other.wake_word:
            return False
        if self.confidence != other.confidence:
            return False
        if self.source != other.source:
            return False
        if self.sample_index != other.sample_index:
            return False
        if self.signal_energy != other.signal_energy:
            return False
        if self.active != other.active:
            return False
        if self.timestamp != other.timestamp:
            return False
        if self.session_id != other.session_id:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def wake_word(self):
        """Message field 'wake_word'."""
        return self._wake_word

    @wake_word.setter
    def wake_word(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'wake_word' field must be of type 'str'"
        self._wake_word = value

    @builtins.property
    def confidence(self):
        """Message field 'confidence'."""
        return self._confidence

    @confidence.setter
    def confidence(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'confidence' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'confidence' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._confidence = value

    @builtins.property
    def source(self):
        """Message field 'source'."""
        return self._source

    @source.setter
    def source(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'source' field must be of type 'str'"
        self._source = value

    @builtins.property
    def sample_index(self):
        """Message field 'sample_index'."""
        return self._sample_index

    @sample_index.setter
    def sample_index(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'sample_index' field must be of type 'int'"
            assert value >= 0 and value < 65536, \
                "The 'sample_index' field must be an unsigned integer in [0, 65535]"
        self._sample_index = value

    @builtins.property
    def signal_energy(self):
        """Message field 'signal_energy'."""
        return self._signal_energy

    @signal_energy.setter
    def signal_energy(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'signal_energy' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'signal_energy' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._signal_energy = value

    @builtins.property
    def active(self):
        """Message field 'active'."""
        return self._active

    @active.setter
    def active(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'active' field must be of type 'bool'"
        self._active = value

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
    def session_id(self):
        """Message field 'session_id'."""
        return self._session_id

    @session_id.setter
    def session_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'session_id' field must be of type 'str'"
        self._session_id = value
