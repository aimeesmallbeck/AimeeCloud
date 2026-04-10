# generated from rosidl_generator_py/resource/_idl.py.em
# with input from aimee_msgs:action/LLMGenerate.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_LLMGenerate_Goal(type):
    """Metaclass of message 'LLMGenerate_Goal'."""

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
                'aimee_msgs.action.LLMGenerate_Goal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__llm_generate__goal
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__llm_generate__goal
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__llm_generate__goal
            cls._TYPE_SUPPORT = module.type_support_msg__action__llm_generate__goal
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__llm_generate__goal

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class LLMGenerate_Goal(metaclass=Metaclass_LLMGenerate_Goal):
    """Message class 'LLMGenerate_Goal'."""

    __slots__ = [
        '_prompt',
        '_system_context',
        '_max_tokens',
        '_temperature',
        '_stream',
        '_session_id',
    ]

    _fields_and_field_types = {
        'prompt': 'string',
        'system_context': 'string',
        'max_tokens': 'int32',
        'temperature': 'float',
        'stream': 'boolean',
        'session_id': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.prompt = kwargs.get('prompt', str())
        self.system_context = kwargs.get('system_context', str())
        self.max_tokens = kwargs.get('max_tokens', int())
        self.temperature = kwargs.get('temperature', float())
        self.stream = kwargs.get('stream', bool())
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
        if self.prompt != other.prompt:
            return False
        if self.system_context != other.system_context:
            return False
        if self.max_tokens != other.max_tokens:
            return False
        if self.temperature != other.temperature:
            return False
        if self.stream != other.stream:
            return False
        if self.session_id != other.session_id:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def prompt(self):
        """Message field 'prompt'."""
        return self._prompt

    @prompt.setter
    def prompt(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'prompt' field must be of type 'str'"
        self._prompt = value

    @builtins.property
    def system_context(self):
        """Message field 'system_context'."""
        return self._system_context

    @system_context.setter
    def system_context(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'system_context' field must be of type 'str'"
        self._system_context = value

    @builtins.property
    def max_tokens(self):
        """Message field 'max_tokens'."""
        return self._max_tokens

    @max_tokens.setter
    def max_tokens(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'max_tokens' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'max_tokens' field must be an integer in [-2147483648, 2147483647]"
        self._max_tokens = value

    @builtins.property
    def temperature(self):
        """Message field 'temperature'."""
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'temperature' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'temperature' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._temperature = value

    @builtins.property
    def stream(self):
        """Message field 'stream'."""
        return self._stream

    @stream.setter
    def stream(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'stream' field must be of type 'bool'"
        self._stream = value

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


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import math

# already imported above
# import rosidl_parser.definition


class Metaclass_LLMGenerate_Result(type):
    """Metaclass of message 'LLMGenerate_Result'."""

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
                'aimee_msgs.action.LLMGenerate_Result')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__llm_generate__result
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__llm_generate__result
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__llm_generate__result
            cls._TYPE_SUPPORT = module.type_support_msg__action__llm_generate__result
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__llm_generate__result

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class LLMGenerate_Result(metaclass=Metaclass_LLMGenerate_Result):
    """Message class 'LLMGenerate_Result'."""

    __slots__ = [
        '_response',
        '_success',
        '_error_message',
        '_generation_time',
        '_tokens_generated',
        '_tokens_input',
    ]

    _fields_and_field_types = {
        'response': 'string',
        'success': 'boolean',
        'error_message': 'string',
        'generation_time': 'float',
        'tokens_generated': 'int32',
        'tokens_input': 'int32',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.response = kwargs.get('response', str())
        self.success = kwargs.get('success', bool())
        self.error_message = kwargs.get('error_message', str())
        self.generation_time = kwargs.get('generation_time', float())
        self.tokens_generated = kwargs.get('tokens_generated', int())
        self.tokens_input = kwargs.get('tokens_input', int())

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
        if self.response != other.response:
            return False
        if self.success != other.success:
            return False
        if self.error_message != other.error_message:
            return False
        if self.generation_time != other.generation_time:
            return False
        if self.tokens_generated != other.tokens_generated:
            return False
        if self.tokens_input != other.tokens_input:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def response(self):
        """Message field 'response'."""
        return self._response

    @response.setter
    def response(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'response' field must be of type 'str'"
        self._response = value

    @builtins.property
    def success(self):
        """Message field 'success'."""
        return self._success

    @success.setter
    def success(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'success' field must be of type 'bool'"
        self._success = value

    @builtins.property
    def error_message(self):
        """Message field 'error_message'."""
        return self._error_message

    @error_message.setter
    def error_message(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'error_message' field must be of type 'str'"
        self._error_message = value

    @builtins.property
    def generation_time(self):
        """Message field 'generation_time'."""
        return self._generation_time

    @generation_time.setter
    def generation_time(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'generation_time' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'generation_time' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._generation_time = value

    @builtins.property
    def tokens_generated(self):
        """Message field 'tokens_generated'."""
        return self._tokens_generated

    @tokens_generated.setter
    def tokens_generated(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'tokens_generated' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'tokens_generated' field must be an integer in [-2147483648, 2147483647]"
        self._tokens_generated = value

    @builtins.property
    def tokens_input(self):
        """Message field 'tokens_input'."""
        return self._tokens_input

    @tokens_input.setter
    def tokens_input(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'tokens_input' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'tokens_input' field must be an integer in [-2147483648, 2147483647]"
        self._tokens_input = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_LLMGenerate_Feedback(type):
    """Metaclass of message 'LLMGenerate_Feedback'."""

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
                'aimee_msgs.action.LLMGenerate_Feedback')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__llm_generate__feedback
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__llm_generate__feedback
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__llm_generate__feedback
            cls._TYPE_SUPPORT = module.type_support_msg__action__llm_generate__feedback
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__llm_generate__feedback

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class LLMGenerate_Feedback(metaclass=Metaclass_LLMGenerate_Feedback):
    """Message class 'LLMGenerate_Feedback'."""

    __slots__ = [
        '_partial_response',
        '_tokens_generated',
        '_tokens_total',
        '_is_complete',
        '_current_word',
    ]

    _fields_and_field_types = {
        'partial_response': 'string',
        'tokens_generated': 'int32',
        'tokens_total': 'int32',
        'is_complete': 'boolean',
        'current_word': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.partial_response = kwargs.get('partial_response', str())
        self.tokens_generated = kwargs.get('tokens_generated', int())
        self.tokens_total = kwargs.get('tokens_total', int())
        self.is_complete = kwargs.get('is_complete', bool())
        self.current_word = kwargs.get('current_word', str())

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
        if self.partial_response != other.partial_response:
            return False
        if self.tokens_generated != other.tokens_generated:
            return False
        if self.tokens_total != other.tokens_total:
            return False
        if self.is_complete != other.is_complete:
            return False
        if self.current_word != other.current_word:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def partial_response(self):
        """Message field 'partial_response'."""
        return self._partial_response

    @partial_response.setter
    def partial_response(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'partial_response' field must be of type 'str'"
        self._partial_response = value

    @builtins.property
    def tokens_generated(self):
        """Message field 'tokens_generated'."""
        return self._tokens_generated

    @tokens_generated.setter
    def tokens_generated(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'tokens_generated' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'tokens_generated' field must be an integer in [-2147483648, 2147483647]"
        self._tokens_generated = value

    @builtins.property
    def tokens_total(self):
        """Message field 'tokens_total'."""
        return self._tokens_total

    @tokens_total.setter
    def tokens_total(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'tokens_total' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'tokens_total' field must be an integer in [-2147483648, 2147483647]"
        self._tokens_total = value

    @builtins.property
    def is_complete(self):
        """Message field 'is_complete'."""
        return self._is_complete

    @is_complete.setter
    def is_complete(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'is_complete' field must be of type 'bool'"
        self._is_complete = value

    @builtins.property
    def current_word(self):
        """Message field 'current_word'."""
        return self._current_word

    @current_word.setter
    def current_word(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'current_word' field must be of type 'str'"
        self._current_word = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_LLMGenerate_SendGoal_Request(type):
    """Metaclass of message 'LLMGenerate_SendGoal_Request'."""

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
                'aimee_msgs.action.LLMGenerate_SendGoal_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__llm_generate__send_goal__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__llm_generate__send_goal__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__llm_generate__send_goal__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__llm_generate__send_goal__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__llm_generate__send_goal__request

            from aimee_msgs.action import LLMGenerate
            if LLMGenerate.Goal.__class__._TYPE_SUPPORT is None:
                LLMGenerate.Goal.__class__.__import_type_support__()

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class LLMGenerate_SendGoal_Request(metaclass=Metaclass_LLMGenerate_SendGoal_Request):
    """Message class 'LLMGenerate_SendGoal_Request'."""

    __slots__ = [
        '_goal_id',
        '_goal',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'goal': 'aimee_msgs/LLMGenerate_Goal',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['aimee_msgs', 'action'], 'LLMGenerate_Goal'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from aimee_msgs.action._llm_generate import LLMGenerate_Goal
        self.goal = kwargs.get('goal', LLMGenerate_Goal())

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
        if self.goal_id != other.goal_id:
            return False
        if self.goal != other.goal:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if __debug__:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value

    @builtins.property
    def goal(self):
        """Message field 'goal'."""
        return self._goal

    @goal.setter
    def goal(self, value):
        if __debug__:
            from aimee_msgs.action._llm_generate import LLMGenerate_Goal
            assert \
                isinstance(value, LLMGenerate_Goal), \
                "The 'goal' field must be a sub message of type 'LLMGenerate_Goal'"
        self._goal = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_LLMGenerate_SendGoal_Response(type):
    """Metaclass of message 'LLMGenerate_SendGoal_Response'."""

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
                'aimee_msgs.action.LLMGenerate_SendGoal_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__llm_generate__send_goal__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__llm_generate__send_goal__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__llm_generate__send_goal__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__llm_generate__send_goal__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__llm_generate__send_goal__response

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


class LLMGenerate_SendGoal_Response(metaclass=Metaclass_LLMGenerate_SendGoal_Response):
    """Message class 'LLMGenerate_SendGoal_Response'."""

    __slots__ = [
        '_accepted',
        '_stamp',
    ]

    _fields_and_field_types = {
        'accepted': 'boolean',
        'stamp': 'builtin_interfaces/Time',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.accepted = kwargs.get('accepted', bool())
        from builtin_interfaces.msg import Time
        self.stamp = kwargs.get('stamp', Time())

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
        if self.accepted != other.accepted:
            return False
        if self.stamp != other.stamp:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def accepted(self):
        """Message field 'accepted'."""
        return self._accepted

    @accepted.setter
    def accepted(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'accepted' field must be of type 'bool'"
        self._accepted = value

    @builtins.property
    def stamp(self):
        """Message field 'stamp'."""
        return self._stamp

    @stamp.setter
    def stamp(self, value):
        if __debug__:
            from builtin_interfaces.msg import Time
            assert \
                isinstance(value, Time), \
                "The 'stamp' field must be a sub message of type 'Time'"
        self._stamp = value


class Metaclass_LLMGenerate_SendGoal(type):
    """Metaclass of service 'LLMGenerate_SendGoal'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('aimee_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'aimee_msgs.action.LLMGenerate_SendGoal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__llm_generate__send_goal

            from aimee_msgs.action import _llm_generate
            if _llm_generate.Metaclass_LLMGenerate_SendGoal_Request._TYPE_SUPPORT is None:
                _llm_generate.Metaclass_LLMGenerate_SendGoal_Request.__import_type_support__()
            if _llm_generate.Metaclass_LLMGenerate_SendGoal_Response._TYPE_SUPPORT is None:
                _llm_generate.Metaclass_LLMGenerate_SendGoal_Response.__import_type_support__()


class LLMGenerate_SendGoal(metaclass=Metaclass_LLMGenerate_SendGoal):
    from aimee_msgs.action._llm_generate import LLMGenerate_SendGoal_Request as Request
    from aimee_msgs.action._llm_generate import LLMGenerate_SendGoal_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_LLMGenerate_GetResult_Request(type):
    """Metaclass of message 'LLMGenerate_GetResult_Request'."""

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
                'aimee_msgs.action.LLMGenerate_GetResult_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__llm_generate__get_result__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__llm_generate__get_result__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__llm_generate__get_result__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__llm_generate__get_result__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__llm_generate__get_result__request

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class LLMGenerate_GetResult_Request(metaclass=Metaclass_LLMGenerate_GetResult_Request):
    """Message class 'LLMGenerate_GetResult_Request'."""

    __slots__ = [
        '_goal_id',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())

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
        if self.goal_id != other.goal_id:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if __debug__:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_LLMGenerate_GetResult_Response(type):
    """Metaclass of message 'LLMGenerate_GetResult_Response'."""

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
                'aimee_msgs.action.LLMGenerate_GetResult_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__llm_generate__get_result__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__llm_generate__get_result__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__llm_generate__get_result__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__llm_generate__get_result__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__llm_generate__get_result__response

            from aimee_msgs.action import LLMGenerate
            if LLMGenerate.Result.__class__._TYPE_SUPPORT is None:
                LLMGenerate.Result.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class LLMGenerate_GetResult_Response(metaclass=Metaclass_LLMGenerate_GetResult_Response):
    """Message class 'LLMGenerate_GetResult_Response'."""

    __slots__ = [
        '_status',
        '_result',
    ]

    _fields_and_field_types = {
        'status': 'int8',
        'result': 'aimee_msgs/LLMGenerate_Result',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['aimee_msgs', 'action'], 'LLMGenerate_Result'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.status = kwargs.get('status', int())
        from aimee_msgs.action._llm_generate import LLMGenerate_Result
        self.result = kwargs.get('result', LLMGenerate_Result())

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
        if self.status != other.status:
            return False
        if self.result != other.result:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def status(self):
        """Message field 'status'."""
        return self._status

    @status.setter
    def status(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'status' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'status' field must be an integer in [-128, 127]"
        self._status = value

    @builtins.property
    def result(self):
        """Message field 'result'."""
        return self._result

    @result.setter
    def result(self, value):
        if __debug__:
            from aimee_msgs.action._llm_generate import LLMGenerate_Result
            assert \
                isinstance(value, LLMGenerate_Result), \
                "The 'result' field must be a sub message of type 'LLMGenerate_Result'"
        self._result = value


class Metaclass_LLMGenerate_GetResult(type):
    """Metaclass of service 'LLMGenerate_GetResult'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('aimee_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'aimee_msgs.action.LLMGenerate_GetResult')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__llm_generate__get_result

            from aimee_msgs.action import _llm_generate
            if _llm_generate.Metaclass_LLMGenerate_GetResult_Request._TYPE_SUPPORT is None:
                _llm_generate.Metaclass_LLMGenerate_GetResult_Request.__import_type_support__()
            if _llm_generate.Metaclass_LLMGenerate_GetResult_Response._TYPE_SUPPORT is None:
                _llm_generate.Metaclass_LLMGenerate_GetResult_Response.__import_type_support__()


class LLMGenerate_GetResult(metaclass=Metaclass_LLMGenerate_GetResult):
    from aimee_msgs.action._llm_generate import LLMGenerate_GetResult_Request as Request
    from aimee_msgs.action._llm_generate import LLMGenerate_GetResult_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_LLMGenerate_FeedbackMessage(type):
    """Metaclass of message 'LLMGenerate_FeedbackMessage'."""

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
                'aimee_msgs.action.LLMGenerate_FeedbackMessage')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__llm_generate__feedback_message
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__llm_generate__feedback_message
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__llm_generate__feedback_message
            cls._TYPE_SUPPORT = module.type_support_msg__action__llm_generate__feedback_message
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__llm_generate__feedback_message

            from aimee_msgs.action import LLMGenerate
            if LLMGenerate.Feedback.__class__._TYPE_SUPPORT is None:
                LLMGenerate.Feedback.__class__.__import_type_support__()

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class LLMGenerate_FeedbackMessage(metaclass=Metaclass_LLMGenerate_FeedbackMessage):
    """Message class 'LLMGenerate_FeedbackMessage'."""

    __slots__ = [
        '_goal_id',
        '_feedback',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'feedback': 'aimee_msgs/LLMGenerate_Feedback',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['aimee_msgs', 'action'], 'LLMGenerate_Feedback'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from aimee_msgs.action._llm_generate import LLMGenerate_Feedback
        self.feedback = kwargs.get('feedback', LLMGenerate_Feedback())

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
        if self.goal_id != other.goal_id:
            return False
        if self.feedback != other.feedback:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if __debug__:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value

    @builtins.property
    def feedback(self):
        """Message field 'feedback'."""
        return self._feedback

    @feedback.setter
    def feedback(self, value):
        if __debug__:
            from aimee_msgs.action._llm_generate import LLMGenerate_Feedback
            assert \
                isinstance(value, LLMGenerate_Feedback), \
                "The 'feedback' field must be a sub message of type 'LLMGenerate_Feedback'"
        self._feedback = value


class Metaclass_LLMGenerate(type):
    """Metaclass of action 'LLMGenerate'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('aimee_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'aimee_msgs.action.LLMGenerate')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_action__action__llm_generate

            from action_msgs.msg import _goal_status_array
            if _goal_status_array.Metaclass_GoalStatusArray._TYPE_SUPPORT is None:
                _goal_status_array.Metaclass_GoalStatusArray.__import_type_support__()
            from action_msgs.srv import _cancel_goal
            if _cancel_goal.Metaclass_CancelGoal._TYPE_SUPPORT is None:
                _cancel_goal.Metaclass_CancelGoal.__import_type_support__()

            from aimee_msgs.action import _llm_generate
            if _llm_generate.Metaclass_LLMGenerate_SendGoal._TYPE_SUPPORT is None:
                _llm_generate.Metaclass_LLMGenerate_SendGoal.__import_type_support__()
            if _llm_generate.Metaclass_LLMGenerate_GetResult._TYPE_SUPPORT is None:
                _llm_generate.Metaclass_LLMGenerate_GetResult.__import_type_support__()
            if _llm_generate.Metaclass_LLMGenerate_FeedbackMessage._TYPE_SUPPORT is None:
                _llm_generate.Metaclass_LLMGenerate_FeedbackMessage.__import_type_support__()


class LLMGenerate(metaclass=Metaclass_LLMGenerate):

    # The goal message defined in the action definition.
    from aimee_msgs.action._llm_generate import LLMGenerate_Goal as Goal
    # The result message defined in the action definition.
    from aimee_msgs.action._llm_generate import LLMGenerate_Result as Result
    # The feedback message defined in the action definition.
    from aimee_msgs.action._llm_generate import LLMGenerate_Feedback as Feedback

    class Impl:

        # The send_goal service using a wrapped version of the goal message as a request.
        from aimee_msgs.action._llm_generate import LLMGenerate_SendGoal as SendGoalService
        # The get_result service using a wrapped version of the result message as a response.
        from aimee_msgs.action._llm_generate import LLMGenerate_GetResult as GetResultService
        # The feedback message with generic fields which wraps the feedback message.
        from aimee_msgs.action._llm_generate import LLMGenerate_FeedbackMessage as FeedbackMessage

        # The generic service to cancel a goal.
        from action_msgs.srv._cancel_goal import CancelGoal as CancelGoalService
        # The generic message for get the status of a goal.
        from action_msgs.msg._goal_status_array import GoalStatusArray as GoalStatusMessage

    def __init__(self):
        raise NotImplementedError('Action classes can not be instantiated')
