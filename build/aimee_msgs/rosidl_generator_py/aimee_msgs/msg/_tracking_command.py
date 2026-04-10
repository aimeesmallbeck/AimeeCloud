# generated from rosidl_generator_py/resource/_idl.py.em
# with input from aimee_msgs:msg/TrackingCommand.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_TrackingCommand(type):
    """Metaclass of message 'TrackingCommand'."""

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
                'aimee_msgs.msg.TrackingCommand')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__tracking_command
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__tracking_command
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__tracking_command
            cls._TYPE_SUPPORT = module.type_support_msg__msg__tracking_command
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__tracking_command

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


class TrackingCommand(metaclass=Metaclass_TrackingCommand):
    """Message class 'TrackingCommand'."""

    __slots__ = [
        '_command',
        '_mode',
        '_preset_id',
        '_zoom_level',
        '_target_type',
        '_target_id',
        '_target_position',
        '_timestamp',
    ]

    _fields_and_field_types = {
        'command': 'string',
        'mode': 'string',
        'preset_id': 'int32',
        'zoom_level': 'int32',
        'target_type': 'string',
        'target_id': 'string',
        'target_position': 'geometry_msgs/Point',
        'timestamp': 'builtin_interfaces/Time',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Point'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.command = kwargs.get('command', str())
        self.mode = kwargs.get('mode', str())
        self.preset_id = kwargs.get('preset_id', int())
        self.zoom_level = kwargs.get('zoom_level', int())
        self.target_type = kwargs.get('target_type', str())
        self.target_id = kwargs.get('target_id', str())
        from geometry_msgs.msg import Point
        self.target_position = kwargs.get('target_position', Point())
        from builtin_interfaces.msg import Time
        self.timestamp = kwargs.get('timestamp', Time())

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
        if self.command != other.command:
            return False
        if self.mode != other.mode:
            return False
        if self.preset_id != other.preset_id:
            return False
        if self.zoom_level != other.zoom_level:
            return False
        if self.target_type != other.target_type:
            return False
        if self.target_id != other.target_id:
            return False
        if self.target_position != other.target_position:
            return False
        if self.timestamp != other.timestamp:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def command(self):
        """Message field 'command'."""
        return self._command

    @command.setter
    def command(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'command' field must be of type 'str'"
        self._command = value

    @builtins.property
    def mode(self):
        """Message field 'mode'."""
        return self._mode

    @mode.setter
    def mode(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'mode' field must be of type 'str'"
        self._mode = value

    @builtins.property
    def preset_id(self):
        """Message field 'preset_id'."""
        return self._preset_id

    @preset_id.setter
    def preset_id(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'preset_id' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'preset_id' field must be an integer in [-2147483648, 2147483647]"
        self._preset_id = value

    @builtins.property
    def zoom_level(self):
        """Message field 'zoom_level'."""
        return self._zoom_level

    @zoom_level.setter
    def zoom_level(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'zoom_level' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'zoom_level' field must be an integer in [-2147483648, 2147483647]"
        self._zoom_level = value

    @builtins.property
    def target_type(self):
        """Message field 'target_type'."""
        return self._target_type

    @target_type.setter
    def target_type(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'target_type' field must be of type 'str'"
        self._target_type = value

    @builtins.property
    def target_id(self):
        """Message field 'target_id'."""
        return self._target_id

    @target_id.setter
    def target_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'target_id' field must be of type 'str'"
        self._target_id = value

    @builtins.property
    def target_position(self):
        """Message field 'target_position'."""
        return self._target_position

    @target_position.setter
    def target_position(self, value):
        if __debug__:
            from geometry_msgs.msg import Point
            assert \
                isinstance(value, Point), \
                "The 'target_position' field must be a sub message of type 'Point'"
        self._target_position = value

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
