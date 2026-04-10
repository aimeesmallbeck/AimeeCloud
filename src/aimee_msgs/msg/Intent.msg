# Intent classification message
# Published by: Intent Router
# Subscribed by: Skills, State Manager

string intent_type          # Type of intent (greeting, movement, arm_control, etc.)
string action               # Specific action (move_forward, wave, etc.)
float32 confidence          # Classification confidence (0.0-1.0)
string raw_text             # Original user text
bool requires_skill         # True if requires skill execution
string skill_name           # Name of skill to execute
string parameters_json      # Action parameters as JSON string

# Context
string session_id           # Conversation session ID
builtin_interfaces/Time timestamp
