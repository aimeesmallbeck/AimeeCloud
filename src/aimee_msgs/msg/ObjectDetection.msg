# Object detection message
# Published by: Vision Pipeline
# Subscribed by: Perception, Skills

# Object identification
string object_class           # "ball", "cup", "block", etc.
string object_id              # Unique instance ID (e.g., "ball_001")
string color                  # "red", "blue", "green", etc.
float32 confidence            # Detection confidence (0.0-1.0)

# 2D bounding box (normalized coordinates 0.0-1.0)
float32 bbox_x                # Center X
float32 bbox_y                # Center Y
float32 bbox_width
float32 bbox_height

# 3D position in camera frame (if available)
geometry_msgs/Point position_camera  # meters from camera

# 3D position in robot base frame (transformed)
geometry_msgs/Point position_robot   # meters from robot base
geometry_msgs/Point position_map     # meters in map frame

# Object dimensions (estimated or known)
float32 object_width          # meters
float32 object_height         # meters
float32 object_depth          # meters

# Source information
string detection_method       # "color", "yolo", "template"
string camera_source          # "obsbot_main", "ov7670"
builtin_interfaces/Time timestamp
