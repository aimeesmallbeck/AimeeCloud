# Motor action performed by a skill
# Published in ExecuteSkill result

string motor_id           # Motor identifier (left_track, right_track, arm_base, etc.)
string action_type        # move, stop, rotate, position
float32[] values          # Action values (speed, position, angle)
builtin_interfaces/Duration execution_time   # How long the action took
