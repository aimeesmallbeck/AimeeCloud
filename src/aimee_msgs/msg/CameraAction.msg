# Camera action performed by a skill
# Published in ExecuteSkill result

string action_type        # track_face, stop_tracking, look_at_me, etc.
string target             # Target object/person
float32 confidence        # Detection confidence
builtin_interfaces/Duration execution_time
