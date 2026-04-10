# Complete robot state message
# Published by: State Manager (aggregates from all nodes)
# Subscribed by: Skills, Cloud Bridge

# Identity
string robot_name         # "ron" or "wren"
string robot_type         # "ugv_arm" | "wave_rover"

# Power
float32 battery_level     # 0.0 to 100.0
bool is_charging
string power_status       # "normal" | "low" | "critical"

# Motion state
string current_action     # "idle" | "moving" | "executing_skill"
geometry_msgs/Twist current_velocity
nav_msgs/Odometry odometry

# Arm state (if applicable)
sensor_msgs/JointState arm_state
bool arm_is_moving
string arm_pose_name      # "home" | "ready" | "custom"

# Gripper state
float32 gripper_position  # 0.0 (closed) to 1.0 (open)

# Camera state
string camera_mode        # "idle" | "tracking" | "manual"
string tracking_target    # "none" | "face" | "body" | "hand"

# Active skills
string[] active_skills
string current_skill_id

# System health
string[] errors           # List of active errors
string[] warnings         # List of active warnings

# Metadata
builtin_interfaces/Time timestamp
