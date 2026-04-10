# Wake word detection message
# Published by: Wake Word Detection Brick (keyword spotting)
# Subscribed by: Voice Manager, State Manager

string wake_word          # Detected wake word (e.g., "aimee", "hey_aimee")
float32 confidence        # Detection confidence (0.0-1.0)
string source             # Detection source (e.g., "edge_impulse", "porcupine")

# Detection context
uint16 sample_index       # Audio sample index at detection
float32 signal_energy     # Audio signal energy level

# System state
bool active               # true when wake word is active/triggered
                          # false when wake word session ends

# Metadata
builtin_interfaces/Time timestamp
string session_id         # Unique session identifier
