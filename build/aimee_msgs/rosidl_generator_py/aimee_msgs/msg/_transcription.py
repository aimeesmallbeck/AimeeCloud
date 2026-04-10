# generated from rosidl_generator_py/resource/_idl.py.em
# with input from aimee_msgs:msg/Transcription.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Transcription(type):
    """Metaclass of message 'Transcription'."""

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
                'aimee_msgs.msg.Transcription')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__transcription
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__transcription
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__transcription
            cls._TYPE_SUPPORT = module.type_support_msg__msg__transcription
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__transcription

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


class Transcription(metaclass=Metaclass_Transcription):
    """Message class 'Transcription'."""

    __slots__ = [
        '_text',
        '_confidence',
        '_source',
        '_is_command',
        '_is_partial',
        '_wake_word_detected',
        '_wake_word',
        '_timestamp',
        '_session_id',
        '_correlation_id',
    ]

    _fields_and_field_types = {
        'text': 'string',
        'confidence': 'float',
        'source': 'string',
        'is_command': 'boolean',
        'is_partial': 'boolean',
        'wake_word_detected': 'boolean',
        'wake_word': 'string',
        'timestamp': 'builtin_interfaces/Time',
        'session_id': 'string',
        'correlation_id': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.text = kwargs.get('text', str())
        self.confidence = kwargs.get('confidence', float())
        self.source = kwargs.get('source', str())
        self.is_command = kwargs.get('is_command', bool())
        self.is_partial = kwargs.get('is_partial', bool())
        self.wake_word_detected = kwargs.get('wake_word_detected', bool())
        self.wake_word = kwargs.get('wake_word', str())
        from builtin_interfaces.msg import Time
        self.timestamp = kwargs.get('timestamp', Time())
        self.session_id = kwargs.get('session_id', str())
        self.correlation_id = kwargs.get('correlation_id', str())

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
        if self.text != other.text:
            return False
        if self.confidence != other.confidence:
            return False
        if self.source != other.source:
            return False
        if self.is_command != other.is_command:
            return False
        if self.is_partial != other.is_partial:
            return False
        if self.wake_word_detected != other.wake_word_detected:
            return False
        if self.wake_word != other.wake_word:
            return False
        if self.timestamp != other.timestamp:
            return False
        if self.session_id != other.session_id:
            return False
        if self.correlation_id != other.correlation_id:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def text(self):
        """Message field 'text'."""
        return self._text

    @text.setter
    def text(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'text' field must be of type 'str'"
        self._text = value

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
    def is_command(self):
        """Message field 'is_command'."""
        return self._is_command

    @is_command.setter
    def is_command(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'is_command' field must be of type 'bool'"
        self._is_command = value

    @builtins.property
    def is_partial(self):
        """Message field 'is_partial'."""
        return self._is_partial

    @is_partial.setter
    def is_partial(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'is_partial' field must be of type 'bool'"
        self._is_partial = value

    @builtins.property
    def wake_word_detected(self):
        """Message field 'wake_word_detected'."""
        return self._wake_word_detected

    @wake_word_detected.setter
    def wake_word_detected(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'wake_word_detected' field must be of type 'bool'"
        self._wake_word_detected = value

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

    @builtins.property
    def correlation_id(self):
        """Message field 'correlation_id'."""
        return self._correlation_id

    @correlation_id.setter
    def correlation_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'correlation_id' field must be of type 'str'"
        self._correlation_id = value
