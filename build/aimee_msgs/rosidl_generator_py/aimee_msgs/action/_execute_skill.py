# generated from rosidl_generator_py/resource/_idl.py.em
# with input from aimee_msgs:action/ExecuteSkill.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ExecuteSkill_Goal(type):
    """Metaclass of message 'ExecuteSkill_Goal'."""

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
                'aimee_msgs.action.ExecuteSkill_Goal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_skill__goal
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_skill__goal
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_skill__goal
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_skill__goal
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_skill__goal

            from aimee_msgs.msg import RobotState
            if RobotState.__class__._TYPE_SUPPORT is None:
                RobotState.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExecuteSkill_Goal(metaclass=Metaclass_ExecuteSkill_Goal):
    """Message class 'ExecuteSkill_Goal'."""

    __slots__ = [
        '_skill_id',
        '_user_input',
        '_robot_state',
        '_user_context',
        '_session_id',
    ]

    _fields_and_field_types = {
        'skill_id': 'string',
        'user_input': 'string',
        'robot_state': 'aimee_msgs/RobotState',
        'user_context': 'string',
        'session_id': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['aimee_msgs', 'msg'], 'RobotState'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.skill_id = kwargs.get('skill_id', str())
        self.user_input = kwargs.get('user_input', str())
        from aimee_msgs.msg import RobotState
        self.robot_state = kwargs.get('robot_state', RobotState())
        self.user_context = kwargs.get('user_context', str())
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
        if self.skill_id != other.skill_id:
            return False
        if self.user_input != other.user_input:
            return False
        if self.robot_state != other.robot_state:
            return False
        if self.user_context != other.user_context:
            return False
        if self.session_id != other.session_id:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def skill_id(self):
        """Message field 'skill_id'."""
        return self._skill_id

    @skill_id.setter
    def skill_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'skill_id' field must be of type 'str'"
        self._skill_id = value

    @builtins.property
    def user_input(self):
        """Message field 'user_input'."""
        return self._user_input

    @user_input.setter
    def user_input(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'user_input' field must be of type 'str'"
        self._user_input = value

    @builtins.property
    def robot_state(self):
        """Message field 'robot_state'."""
        return self._robot_state

    @robot_state.setter
    def robot_state(self, value):
        if __debug__:
            from aimee_msgs.msg import RobotState
            assert \
                isinstance(value, RobotState), \
                "The 'robot_state' field must be a sub message of type 'RobotState'"
        self._robot_state = value

    @builtins.property
    def user_context(self):
        """Message field 'user_context'."""
        return self._user_context

    @user_context.setter
    def user_context(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'user_context' field must be of type 'str'"
        self._user_context = value

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
# import rosidl_parser.definition


class Metaclass_ExecuteSkill_Result(type):
    """Metaclass of message 'ExecuteSkill_Result'."""

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
                'aimee_msgs.action.ExecuteSkill_Result')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_skill__result
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_skill__result
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_skill__result
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_skill__result
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_skill__result

            from aimee_msgs.msg import CameraAction
            if CameraAction.__class__._TYPE_SUPPORT is None:
                CameraAction.__class__.__import_type_support__()

            from aimee_msgs.msg import LEDAction
            if LEDAction.__class__._TYPE_SUPPORT is None:
                LEDAction.__class__.__import_type_support__()

            from aimee_msgs.msg import MotorAction
            if MotorAction.__class__._TYPE_SUPPORT is None:
                MotorAction.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExecuteSkill_Result(metaclass=Metaclass_ExecuteSkill_Result):
    """Message class 'ExecuteSkill_Result'."""

    __slots__ = [
        '_success',
        '_response_text',
        '_tts_audio_path',
        '_error_message',
        '_motor_actions',
        '_camera_actions',
        '_led_actions',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'response_text': 'string',
        'tts_audio_path': 'string',
        'error_message': 'string',
        'motor_actions': 'sequence<aimee_msgs/MotorAction>',
        'camera_actions': 'sequence<aimee_msgs/CameraAction>',
        'led_actions': 'sequence<aimee_msgs/LEDAction>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['aimee_msgs', 'msg'], 'MotorAction')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['aimee_msgs', 'msg'], 'CameraAction')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['aimee_msgs', 'msg'], 'LEDAction')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.response_text = kwargs.get('response_text', str())
        self.tts_audio_path = kwargs.get('tts_audio_path', str())
        self.error_message = kwargs.get('error_message', str())
        self.motor_actions = kwargs.get('motor_actions', [])
        self.camera_actions = kwargs.get('camera_actions', [])
        self.led_actions = kwargs.get('led_actions', [])

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
        if self.success != other.success:
            return False
        if self.response_text != other.response_text:
            return False
        if self.tts_audio_path != other.tts_audio_path:
            return False
        if self.error_message != other.error_message:
            return False
        if self.motor_actions != other.motor_actions:
            return False
        if self.camera_actions != other.camera_actions:
            return False
        if self.led_actions != other.led_actions:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

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
    def response_text(self):
        """Message field 'response_text'."""
        return self._response_text

    @response_text.setter
    def response_text(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'response_text' field must be of type 'str'"
        self._response_text = value

    @builtins.property
    def tts_audio_path(self):
        """Message field 'tts_audio_path'."""
        return self._tts_audio_path

    @tts_audio_path.setter
    def tts_audio_path(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'tts_audio_path' field must be of type 'str'"
        self._tts_audio_path = value

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
    def motor_actions(self):
        """Message field 'motor_actions'."""
        return self._motor_actions

    @motor_actions.setter
    def motor_actions(self, value):
        if __debug__:
            from aimee_msgs.msg import MotorAction
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
                 all(isinstance(v, MotorAction) for v in value) and
                 True), \
                "The 'motor_actions' field must be a set or sequence and each value of type 'MotorAction'"
        self._motor_actions = value

    @builtins.property
    def camera_actions(self):
        """Message field 'camera_actions'."""
        return self._camera_actions

    @camera_actions.setter
    def camera_actions(self, value):
        if __debug__:
            from aimee_msgs.msg import CameraAction
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
                 all(isinstance(v, CameraAction) for v in value) and
                 True), \
                "The 'camera_actions' field must be a set or sequence and each value of type 'CameraAction'"
        self._camera_actions = value

    @builtins.property
    def led_actions(self):
        """Message field 'led_actions'."""
        return self._led_actions

    @led_actions.setter
    def led_actions(self, value):
        if __debug__:
            from aimee_msgs.msg import LEDAction
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
                 all(isinstance(v, LEDAction) for v in value) and
                 True), \
                "The 'led_actions' field must be a set or sequence and each value of type 'LEDAction'"
        self._led_actions = value


# Import statements for member types

# already imported above
# import builtins

import math  # noqa: E402, I100

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteSkill_Feedback(type):
    """Metaclass of message 'ExecuteSkill_Feedback'."""

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
                'aimee_msgs.action.ExecuteSkill_Feedback')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_skill__feedback
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_skill__feedback
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_skill__feedback
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_skill__feedback
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_skill__feedback

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExecuteSkill_Feedback(metaclass=Metaclass_ExecuteSkill_Feedback):
    """Message class 'ExecuteSkill_Feedback'."""

    __slots__ = [
        '_status',
        '_current_action',
        '_progress',
        '_can_cancel',
    ]

    _fields_and_field_types = {
        'status': 'string',
        'current_action': 'string',
        'progress': 'float',
        'can_cancel': 'boolean',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.status = kwargs.get('status', str())
        self.current_action = kwargs.get('current_action', str())
        self.progress = kwargs.get('progress', float())
        self.can_cancel = kwargs.get('can_cancel', bool())

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
        if self.current_action != other.current_action:
            return False
        if self.progress != other.progress:
            return False
        if self.can_cancel != other.can_cancel:
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
                isinstance(value, str), \
                "The 'status' field must be of type 'str'"
        self._status = value

    @builtins.property
    def current_action(self):
        """Message field 'current_action'."""
        return self._current_action

    @current_action.setter
    def current_action(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'current_action' field must be of type 'str'"
        self._current_action = value

    @builtins.property
    def progress(self):
        """Message field 'progress'."""
        return self._progress

    @progress.setter
    def progress(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'progress' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'progress' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._progress = value

    @builtins.property
    def can_cancel(self):
        """Message field 'can_cancel'."""
        return self._can_cancel

    @can_cancel.setter
    def can_cancel(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'can_cancel' field must be of type 'bool'"
        self._can_cancel = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteSkill_SendGoal_Request(type):
    """Metaclass of message 'ExecuteSkill_SendGoal_Request'."""

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
                'aimee_msgs.action.ExecuteSkill_SendGoal_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_skill__send_goal__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_skill__send_goal__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_skill__send_goal__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_skill__send_goal__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_skill__send_goal__request

            from aimee_msgs.action import ExecuteSkill
            if ExecuteSkill.Goal.__class__._TYPE_SUPPORT is None:
                ExecuteSkill.Goal.__class__.__import_type_support__()

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


class ExecuteSkill_SendGoal_Request(metaclass=Metaclass_ExecuteSkill_SendGoal_Request):
    """Message class 'ExecuteSkill_SendGoal_Request'."""

    __slots__ = [
        '_goal_id',
        '_goal',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'goal': 'aimee_msgs/ExecuteSkill_Goal',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['aimee_msgs', 'action'], 'ExecuteSkill_Goal'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from aimee_msgs.action._execute_skill import ExecuteSkill_Goal
        self.goal = kwargs.get('goal', ExecuteSkill_Goal())

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
            from aimee_msgs.action._execute_skill import ExecuteSkill_Goal
            assert \
                isinstance(value, ExecuteSkill_Goal), \
                "The 'goal' field must be a sub message of type 'ExecuteSkill_Goal'"
        self._goal = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteSkill_SendGoal_Response(type):
    """Metaclass of message 'ExecuteSkill_SendGoal_Response'."""

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
                'aimee_msgs.action.ExecuteSkill_SendGoal_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_skill__send_goal__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_skill__send_goal__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_skill__send_goal__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_skill__send_goal__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_skill__send_goal__response

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


class ExecuteSkill_SendGoal_Response(metaclass=Metaclass_ExecuteSkill_SendGoal_Response):
    """Message class 'ExecuteSkill_SendGoal_Response'."""

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


class Metaclass_ExecuteSkill_SendGoal(type):
    """Metaclass of service 'ExecuteSkill_SendGoal'."""

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
                'aimee_msgs.action.ExecuteSkill_SendGoal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__execute_skill__send_goal

            from aimee_msgs.action import _execute_skill
            if _execute_skill.Metaclass_ExecuteSkill_SendGoal_Request._TYPE_SUPPORT is None:
                _execute_skill.Metaclass_ExecuteSkill_SendGoal_Request.__import_type_support__()
            if _execute_skill.Metaclass_ExecuteSkill_SendGoal_Response._TYPE_SUPPORT is None:
                _execute_skill.Metaclass_ExecuteSkill_SendGoal_Response.__import_type_support__()


class ExecuteSkill_SendGoal(metaclass=Metaclass_ExecuteSkill_SendGoal):
    from aimee_msgs.action._execute_skill import ExecuteSkill_SendGoal_Request as Request
    from aimee_msgs.action._execute_skill import ExecuteSkill_SendGoal_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteSkill_GetResult_Request(type):
    """Metaclass of message 'ExecuteSkill_GetResult_Request'."""

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
                'aimee_msgs.action.ExecuteSkill_GetResult_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_skill__get_result__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_skill__get_result__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_skill__get_result__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_skill__get_result__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_skill__get_result__request

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


class ExecuteSkill_GetResult_Request(metaclass=Metaclass_ExecuteSkill_GetResult_Request):
    """Message class 'ExecuteSkill_GetResult_Request'."""

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


class Metaclass_ExecuteSkill_GetResult_Response(type):
    """Metaclass of message 'ExecuteSkill_GetResult_Response'."""

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
                'aimee_msgs.action.ExecuteSkill_GetResult_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_skill__get_result__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_skill__get_result__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_skill__get_result__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_skill__get_result__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_skill__get_result__response

            from aimee_msgs.action import ExecuteSkill
            if ExecuteSkill.Result.__class__._TYPE_SUPPORT is None:
                ExecuteSkill.Result.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExecuteSkill_GetResult_Response(metaclass=Metaclass_ExecuteSkill_GetResult_Response):
    """Message class 'ExecuteSkill_GetResult_Response'."""

    __slots__ = [
        '_status',
        '_result',
    ]

    _fields_and_field_types = {
        'status': 'int8',
        'result': 'aimee_msgs/ExecuteSkill_Result',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['aimee_msgs', 'action'], 'ExecuteSkill_Result'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.status = kwargs.get('status', int())
        from aimee_msgs.action._execute_skill import ExecuteSkill_Result
        self.result = kwargs.get('result', ExecuteSkill_Result())

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
            from aimee_msgs.action._execute_skill import ExecuteSkill_Result
            assert \
                isinstance(value, ExecuteSkill_Result), \
                "The 'result' field must be a sub message of type 'ExecuteSkill_Result'"
        self._result = value


class Metaclass_ExecuteSkill_GetResult(type):
    """Metaclass of service 'ExecuteSkill_GetResult'."""

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
                'aimee_msgs.action.ExecuteSkill_GetResult')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__execute_skill__get_result

            from aimee_msgs.action import _execute_skill
            if _execute_skill.Metaclass_ExecuteSkill_GetResult_Request._TYPE_SUPPORT is None:
                _execute_skill.Metaclass_ExecuteSkill_GetResult_Request.__import_type_support__()
            if _execute_skill.Metaclass_ExecuteSkill_GetResult_Response._TYPE_SUPPORT is None:
                _execute_skill.Metaclass_ExecuteSkill_GetResult_Response.__import_type_support__()


class ExecuteSkill_GetResult(metaclass=Metaclass_ExecuteSkill_GetResult):
    from aimee_msgs.action._execute_skill import ExecuteSkill_GetResult_Request as Request
    from aimee_msgs.action._execute_skill import ExecuteSkill_GetResult_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteSkill_FeedbackMessage(type):
    """Metaclass of message 'ExecuteSkill_FeedbackMessage'."""

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
                'aimee_msgs.action.ExecuteSkill_FeedbackMessage')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_skill__feedback_message
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_skill__feedback_message
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_skill__feedback_message
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_skill__feedback_message
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_skill__feedback_message

            from aimee_msgs.action import ExecuteSkill
            if ExecuteSkill.Feedback.__class__._TYPE_SUPPORT is None:
                ExecuteSkill.Feedback.__class__.__import_type_support__()

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


class ExecuteSkill_FeedbackMessage(metaclass=Metaclass_ExecuteSkill_FeedbackMessage):
    """Message class 'ExecuteSkill_FeedbackMessage'."""

    __slots__ = [
        '_goal_id',
        '_feedback',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'feedback': 'aimee_msgs/ExecuteSkill_Feedback',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['aimee_msgs', 'action'], 'ExecuteSkill_Feedback'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from aimee_msgs.action._execute_skill import ExecuteSkill_Feedback
        self.feedback = kwargs.get('feedback', ExecuteSkill_Feedback())

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
            from aimee_msgs.action._execute_skill import ExecuteSkill_Feedback
            assert \
                isinstance(value, ExecuteSkill_Feedback), \
                "The 'feedback' field must be a sub message of type 'ExecuteSkill_Feedback'"
        self._feedback = value


class Metaclass_ExecuteSkill(type):
    """Metaclass of action 'ExecuteSkill'."""

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
                'aimee_msgs.action.ExecuteSkill')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_action__action__execute_skill

            from action_msgs.msg import _goal_status_array
            if _goal_status_array.Metaclass_GoalStatusArray._TYPE_SUPPORT is None:
                _goal_status_array.Metaclass_GoalStatusArray.__import_type_support__()
            from action_msgs.srv import _cancel_goal
            if _cancel_goal.Metaclass_CancelGoal._TYPE_SUPPORT is None:
                _cancel_goal.Metaclass_CancelGoal.__import_type_support__()

            from aimee_msgs.action import _execute_skill
            if _execute_skill.Metaclass_ExecuteSkill_SendGoal._TYPE_SUPPORT is None:
                _execute_skill.Metaclass_ExecuteSkill_SendGoal.__import_type_support__()
            if _execute_skill.Metaclass_ExecuteSkill_GetResult._TYPE_SUPPORT is None:
                _execute_skill.Metaclass_ExecuteSkill_GetResult.__import_type_support__()
            if _execute_skill.Metaclass_ExecuteSkill_FeedbackMessage._TYPE_SUPPORT is None:
                _execute_skill.Metaclass_ExecuteSkill_FeedbackMessage.__import_type_support__()


class ExecuteSkill(metaclass=Metaclass_ExecuteSkill):

    # The goal message defined in the action definition.
    from aimee_msgs.action._execute_skill import ExecuteSkill_Goal as Goal
    # The result message defined in the action definition.
    from aimee_msgs.action._execute_skill import ExecuteSkill_Result as Result
    # The feedback message defined in the action definition.
    from aimee_msgs.action._execute_skill import ExecuteSkill_Feedback as Feedback

    class Impl:

        # The send_goal service using a wrapped version of the goal message as a request.
        from aimee_msgs.action._execute_skill import ExecuteSkill_SendGoal as SendGoalService
        # The get_result service using a wrapped version of the result message as a response.
        from aimee_msgs.action._execute_skill import ExecuteSkill_GetResult as GetResultService
        # The feedback message with generic fields which wraps the feedback message.
        from aimee_msgs.action._execute_skill import ExecuteSkill_FeedbackMessage as FeedbackMessage

        # The generic service to cancel a goal.
        from action_msgs.srv._cancel_goal import CancelGoal as CancelGoalService
        # The generic message for get the status of a goal.
        from action_msgs.msg._goal_status_array import GoalStatusArray as GoalStatusMessage

    def __init__(self):
        raise NotImplementedError('Action classes can not be instantiated')
