# generated from rosidl_generator_py/resource/_idl.py.em
# with input from aimee_msgs:msg/RobotState.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_RobotState(type):
    """Metaclass of message 'RobotState'."""

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
                'aimee_msgs.msg.RobotState')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__robot_state
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__robot_state
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__robot_state
            cls._TYPE_SUPPORT = module.type_support_msg__msg__robot_state
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__robot_state

            from builtin_interfaces.msg import Time
            if Time.__class__._TYPE_SUPPORT is None:
                Time.__class__.__import_type_support__()

            from geometry_msgs.msg import Twist
            if Twist.__class__._TYPE_SUPPORT is None:
                Twist.__class__.__import_type_support__()

            from nav_msgs.msg import Odometry
            if Odometry.__class__._TYPE_SUPPORT is None:
                Odometry.__class__.__import_type_support__()

            from sensor_msgs.msg import JointState
            if JointState.__class__._TYPE_SUPPORT is None:
                JointState.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class RobotState(metaclass=Metaclass_RobotState):
    """Message class 'RobotState'."""

    __slots__ = [
        '_robot_name',
        '_robot_type',
        '_battery_level',
        '_is_charging',
        '_power_status',
        '_current_action',
        '_current_velocity',
        '_odometry',
        '_arm_state',
        '_arm_is_moving',
        '_arm_pose_name',
        '_gripper_position',
        '_camera_mode',
        '_tracking_target',
        '_active_skills',
        '_current_skill_id',
        '_errors',
        '_warnings',
        '_timestamp',
    ]

    _fields_and_field_types = {
        'robot_name': 'string',
        'robot_type': 'string',
        'battery_level': 'float',
        'is_charging': 'boolean',
        'power_status': 'string',
        'current_action': 'string',
        'current_velocity': 'geometry_msgs/Twist',
        'odometry': 'nav_msgs/Odometry',
        'arm_state': 'sensor_msgs/JointState',
        'arm_is_moving': 'boolean',
        'arm_pose_name': 'string',
        'gripper_position': 'float',
        'camera_mode': 'string',
        'tracking_target': 'string',
        'active_skills': 'sequence<string>',
        'current_skill_id': 'string',
        'errors': 'sequence<string>',
        'warnings': 'sequence<string>',
        'timestamp': 'builtin_interfaces/Time',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Twist'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['nav_msgs', 'msg'], 'Odometry'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['sensor_msgs', 'msg'], 'JointState'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.robot_name = kwargs.get('robot_name', str())
        self.robot_type = kwargs.get('robot_type', str())
        self.battery_level = kwargs.get('battery_level', float())
        self.is_charging = kwargs.get('is_charging', bool())
        self.power_status = kwargs.get('power_status', str())
        self.current_action = kwargs.get('current_action', str())
        from geometry_msgs.msg import Twist
        self.current_velocity = kwargs.get('current_velocity', Twist())
        from nav_msgs.msg import Odometry
        self.odometry = kwargs.get('odometry', Odometry())
        from sensor_msgs.msg import JointState
        self.arm_state = kwargs.get('arm_state', JointState())
        self.arm_is_moving = kwargs.get('arm_is_moving', bool())
        self.arm_pose_name = kwargs.get('arm_pose_name', str())
        self.gripper_position = kwargs.get('gripper_position', float())
        self.camera_mode = kwargs.get('camera_mode', str())
        self.tracking_target = kwargs.get('tracking_target', str())
        self.active_skills = kwargs.get('active_skills', [])
        self.current_skill_id = kwargs.get('current_skill_id', str())
        self.errors = kwargs.get('errors', [])
        self.warnings = kwargs.get('warnings', [])
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
        if self.robot_name != other.robot_name:
            return False
        if self.robot_type != other.robot_type:
            return False
        if self.battery_level != other.battery_level:
            return False
        if self.is_charging != other.is_charging:
            return False
        if self.power_status != other.power_status:
            return False
        if self.current_action != other.current_action:
            return False
        if self.current_velocity != other.current_velocity:
            return False
        if self.odometry != other.odometry:
            return False
        if self.arm_state != other.arm_state:
            return False
        if self.arm_is_moving != other.arm_is_moving:
            return False
        if self.arm_pose_name != other.arm_pose_name:
            return False
        if self.gripper_position != other.gripper_position:
            return False
        if self.camera_mode != other.camera_mode:
            return False
        if self.tracking_target != other.tracking_target:
            return False
        if self.active_skills != other.active_skills:
            return False
        if self.current_skill_id != other.current_skill_id:
            return False
        if self.errors != other.errors:
            return False
        if self.warnings != other.warnings:
            return False
        if self.timestamp != other.timestamp:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def robot_name(self):
        """Message field 'robot_name'."""
        return self._robot_name

    @robot_name.setter
    def robot_name(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'robot_name' field must be of type 'str'"
        self._robot_name = value

    @builtins.property
    def robot_type(self):
        """Message field 'robot_type'."""
        return self._robot_type

    @robot_type.setter
    def robot_type(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'robot_type' field must be of type 'str'"
        self._robot_type = value

    @builtins.property
    def battery_level(self):
        """Message field 'battery_level'."""
        return self._battery_level

    @battery_level.setter
    def battery_level(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'battery_level' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'battery_level' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._battery_level = value

    @builtins.property
    def is_charging(self):
        """Message field 'is_charging'."""
        return self._is_charging

    @is_charging.setter
    def is_charging(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'is_charging' field must be of type 'bool'"
        self._is_charging = value

    @builtins.property
    def power_status(self):
        """Message field 'power_status'."""
        return self._power_status

    @power_status.setter
    def power_status(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'power_status' field must be of type 'str'"
        self._power_status = value

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
    def current_velocity(self):
        """Message field 'current_velocity'."""
        return self._current_velocity

    @current_velocity.setter
    def current_velocity(self, value):
        if __debug__:
            from geometry_msgs.msg import Twist
            assert \
                isinstance(value, Twist), \
                "The 'current_velocity' field must be a sub message of type 'Twist'"
        self._current_velocity = value

    @builtins.property
    def odometry(self):
        """Message field 'odometry'."""
        return self._odometry

    @odometry.setter
    def odometry(self, value):
        if __debug__:
            from nav_msgs.msg import Odometry
            assert \
                isinstance(value, Odometry), \
                "The 'odometry' field must be a sub message of type 'Odometry'"
        self._odometry = value

    @builtins.property
    def arm_state(self):
        """Message field 'arm_state'."""
        return self._arm_state

    @arm_state.setter
    def arm_state(self, value):
        if __debug__:
            from sensor_msgs.msg import JointState
            assert \
                isinstance(value, JointState), \
                "The 'arm_state' field must be a sub message of type 'JointState'"
        self._arm_state = value

    @builtins.property
    def arm_is_moving(self):
        """Message field 'arm_is_moving'."""
        return self._arm_is_moving

    @arm_is_moving.setter
    def arm_is_moving(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'arm_is_moving' field must be of type 'bool'"
        self._arm_is_moving = value

    @builtins.property
    def arm_pose_name(self):
        """Message field 'arm_pose_name'."""
        return self._arm_pose_name

    @arm_pose_name.setter
    def arm_pose_name(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'arm_pose_name' field must be of type 'str'"
        self._arm_pose_name = value

    @builtins.property
    def gripper_position(self):
        """Message field 'gripper_position'."""
        return self._gripper_position

    @gripper_position.setter
    def gripper_position(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'gripper_position' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'gripper_position' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._gripper_position = value

    @builtins.property
    def camera_mode(self):
        """Message field 'camera_mode'."""
        return self._camera_mode

    @camera_mode.setter
    def camera_mode(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'camera_mode' field must be of type 'str'"
        self._camera_mode = value

    @builtins.property
    def tracking_target(self):
        """Message field 'tracking_target'."""
        return self._tracking_target

    @tracking_target.setter
    def tracking_target(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'tracking_target' field must be of type 'str'"
        self._tracking_target = value

    @builtins.property
    def active_skills(self):
        """Message field 'active_skills'."""
        return self._active_skills

    @active_skills.setter
    def active_skills(self, value):
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
                 all(isinstance(v, str) for v in value) and
                 True), \
                "The 'active_skills' field must be a set or sequence and each value of type 'str'"
        self._active_skills = value

    @builtins.property
    def current_skill_id(self):
        """Message field 'current_skill_id'."""
        return self._current_skill_id

    @current_skill_id.setter
    def current_skill_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'current_skill_id' field must be of type 'str'"
        self._current_skill_id = value

    @builtins.property
    def errors(self):
        """Message field 'errors'."""
        return self._errors

    @errors.setter
    def errors(self, value):
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
                 all(isinstance(v, str) for v in value) and
                 True), \
                "The 'errors' field must be a set or sequence and each value of type 'str'"
        self._errors = value

    @builtins.property
    def warnings(self):
        """Message field 'warnings'."""
        return self._warnings

    @warnings.setter
    def warnings(self, value):
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
                 all(isinstance(v, str) for v in value) and
                 True), \
                "The 'warnings' field must be a set or sequence and each value of type 'str'"
        self._warnings = value

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
