# Arm control command
# Published by: Skills, Grasp Planner
# Subscribed by: Arm Controller

# Command type
string command_type           # "joint", "cartesian", "grasp", "home", "gripper"

# For "joint" command - joint angles in degrees
float32[] joint_angles        # [base, shoulder, elbow, wrist1, wrist2, gripper]
float32 joint_speed           # 0-100 percent

# For "cartesian" command - end-effector pose
geometry_msgs/Pose target_pose
float32 cartesian_speed       # mm/s

# For "grasp" command
string grasp_object_id        # Reference to ObjectDetection
GraspPose grasp_pose          # Full grasp specification

# For "gripper" command
float32 gripper_position      # 0-100 (0=closed, 100=open)
float32 gripper_force         # 0-100 (gripping force)

# Motion planning
bool use_planning             # Use path planning (true) or direct motion (false)
float32 planning_time         # Max time for planning (seconds)

# Safety
float32 max_velocity          # Global velocity limit
bool stop_on_collision        # Emergency stop if collision detected

# Metadata
builtin_interfaces/Time timestamp
string skill_id               # Which skill requested this
