# Camera tracking command message
# Published by: Skills, Face Recognition
# Subscribed by: Vision Manager

string command            # "start" | "stop" | "preset" | "zoom" | "mode"
string mode               # "normal" | "upper_body" | "closeup" | "headless" | "desk" | "whiteboard" | "hand" | "group" | "off"
int32 preset_id           # For "preset" command (1-3)
int32 zoom_level          # For "zoom" command (0-100)

# Target to track (for advanced tracking)
string target_type        # "face" | "body" | "hand" | "object"
string target_id          # Specific target identifier
geometry_msgs/Point target_position  # Last known position

# Metadata
builtin_interfaces/Time timestamp
