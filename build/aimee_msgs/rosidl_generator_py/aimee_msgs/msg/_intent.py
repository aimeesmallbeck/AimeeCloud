# generated from rosidl_generator_py/resource/_idl.py.em
# with input from aimee_msgs:msg/Intent.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Intent(type):
    """Metaclass of message 'Intent'."""

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
                'aimee_msgs.msg.Intent')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__intent
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__intent
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__intent
            cls._TYPE_SUPPORT = module.type_support_msg__msg__intent
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__intent

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


class Intent(metaclass=Metaclass_Intent):
    """Message class 'Intent'."""

    __slots__ = [
        '_intent_type',
        '_action',
        '_confidence',
        '_raw_text',
        '_requires_skill',
        '_skill_name',
        '_parameters_json',
        '_session_id',
        '_timestamp',
    ]

    _fields_and_field_types = {
        'intent_type': 'string',
        'action': 'string',
        'confidence': 'float',
        'raw_text': 'string',
        'requires_skill': 'boolean',
        'skill_name': 'string',
        'parameters_json': 'string',
        'session_id': 'string',
        'timestamp': 'builtin_interfaces/Time',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.intent_type = kwargs.get('intent_type', str())
        self.action = kwargs.get('action', str())
        self.confidence = kwargs.get('confidence', float())
        self.raw_text = kwargs.get('raw_text', str())
        self.requires_skill = kwargs.get('requires_skill', bool())
        self.skill_name = kwargs.get('skill_name', str())
        self.parameters_json = kwargs.get('parameters_json', str())
        self.session_id = kwargs.get('session_id', str())
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
        if self.intent_type != other.intent_type:
            return False
        if self.action != other.action:
            return False
        if self.confidence != other.confidence:
            return False
        if self.raw_text != other.raw_text:
            return False
        if self.requires_skill != other.requires_skill:
            return False
        if self.skill_name != other.skill_name:
            return False
        if self.parameters_json != other.parameters_json:
            return False
        if self.session_id != other.session_id:
            return False
        if self.timestamp != other.timestamp:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def intent_type(self):
        """Message field 'intent_type'."""
        return self._intent_type

    @intent_type.setter
    def intent_type(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'intent_type' field must be of type 'str'"
        self._intent_type = value

    @builtins.property
    def action(self):
        """Message field 'action'."""
        return self._action

    @action.setter
    def action(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'action' field must be of type 'str'"
        self._action = value

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
    def raw_text(self):
        """Message field 'raw_text'."""
        return self._raw_text

    @raw_text.setter
    def raw_text(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'raw_text' field must be of type 'str'"
        self._raw_text = value

    @builtins.property
    def requires_skill(self):
        """Message field 'requires_skill'."""
        return self._requires_skill

    @requires_skill.setter
    def requires_skill(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'requires_skill' field must be of type 'bool'"
        self._requires_skill = value

    @builtins.property
    def skill_name(self):
        """Message field 'skill_name'."""
        return self._skill_name

    @skill_name.setter
    def skill_name(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'skill_name' field must be of type 'str'"
        self._skill_name = value

    @builtins.property
    def parameters_json(self):
        """Message field 'parameters_json'."""
        return self._parameters_json

    @parameters_json.setter
    def parameters_json(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'parameters_json' field must be of type 'str'"
        self._parameters_json = value

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
