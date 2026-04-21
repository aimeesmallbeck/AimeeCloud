# Face detection message
# Published by: Vision Manager
# Subscribed by: Skills, OBSBOT Controller

# Face identification
string face_id            # Unique face identifier (or "unknown")
string person_name        # Name if recognized, "unknown" otherwise
float32 recognition_confidence

# Face location (normalized coordinates 0.0-1.0)
float32 center_x
float32 center_y
float32 width
float32 height

# Additional face data
int32 num_faces_detected  # Total faces in frame
float32[] face_landmarks  # Optional: facial landmarks

# 3D position estimate (if available)
geometry_msgs/Point position_3d

# Metadata
builtin_interfaces/Time timestamp
string camera_source      # "obsbot_main" | "ov7670"
