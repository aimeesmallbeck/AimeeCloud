# Intent message for routing user commands
# Published by: Intent Router
# Subscribed by: Skill Manager

# Intent classification
string intent_type        # robot_control | identity_check | cloud_skill | emergency | unknown
string category           # movement | arm | system | entertainment | conversation
float32 confidence        # 0.0 to 1.0
string raw_text           # Original transcribed text
string source             # keyword | llm | cloud
string correlation_id     # Unique ID for tracking

# Metadata
builtin_interfaces/Time timestamp
string session_id
