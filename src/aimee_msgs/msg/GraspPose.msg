# Grasp pose for manipulation
# Published by: Grasp Planner
# Subscribed by: Arm Controller

# Target object reference
string object_id              # Which object to grasp
string object_class           # For verification

# Pre-grasp position (approach pose)
geometry_msgs/Pose pre_grasp_pose    # Position before grasping
float32 pre_grasp_offset      # Distance to keep before grasp (meters)

# Grasp position (final gripper pose)
geometry_msgs/Pose grasp_pose        # Final grasp position

# Post-grasp position (lift pose)
geometry_msgs/Pose lift_pose         # Position after grasping
float32 lift_height           # How high to lift (meters)

# Gripper settings
float32 gripper_open_width   # meters
float32 gripper_close_width  # meters (0 for full close)

# Grasp quality metrics
float32 grasp_quality         # 0.0-1.0 confidence in this grasp
string grasp_type             # "top_down", "side", "pinch"

# Approach direction (for visualization/debugging)
geometry_msgs/Vector3 approach_vector

# Metadata
builtin_interfaces/Time timestamp
string frame_id               # "base_link", "gripper_frame", etc.
