# generated from rosidl_generator_py/resource/_idl.py.em
# with input from aimee_msgs:msg/LEDAction.idl
# generated code does not contain a copyright notice


# Import statements for member types

# Member 'color'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_LEDAction(type):
    """Metaclass of message 'LEDAction'."""

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
                'aimee_msgs.msg.LEDAction')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__led_action
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__led_action
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__led_action
            cls._TYPE_SUPPORT = module.type_support_msg__msg__led_action
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__led_action

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class LEDAction(metaclass=Metaclass_LEDAction):
    """Message class 'LEDAction'."""

    __slots__ = [
        '_led_id',
        '_color',
        '_pattern',
        '_duration_sec',
    ]

    _fields_and_field_types = {
        'led_id': 'string',
        'color': 'sequence<uint8>',
        'pattern': 'string',
        'duration_sec': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('uint8')),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.led_id = kwargs.get('led_id', str())
        self.color = array.array('B', kwargs.get('color', []))
        self.pattern = kwargs.get('pattern', str())
        self.duration_sec = kwargs.get('duration_sec', float())

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
        if self.led_id != other.led_id:
            return False
        if self.color != other.color:
            return False
        if self.pattern != other.pattern:
            return False
        if self.duration_sec != other.duration_sec:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def led_id(self):
        """Message field 'led_id'."""
        return self._led_id

    @led_id.setter
    def led_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'led_id' field must be of type 'str'"
        self._led_id = value

    @builtins.property
    def color(self):
        """Message field 'color'."""
        return self._color

    @color.setter
    def color(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'B', \
                "The 'color' array.array() must have the type code of 'B'"
            self._color = value
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
                 all(isinstance(v, int) for v in value) and
                 all(val >= 0 and val < 256 for val in value)), \
                "The 'color' field must be a set or sequence and each value of type 'int' and each unsigned integer in [0, 255]"
        self._color = array.array('B', value)

    @builtins.property
    def pattern(self):
        """Message field 'pattern'."""
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'pattern' field must be of type 'str'"
        self._pattern = value

    @builtins.property
    def duration_sec(self):
        """Message field 'duration_sec'."""
        return self._duration_sec

    @duration_sec.setter
    def duration_sec(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'duration_sec' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'duration_sec' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._duration_sec = value
