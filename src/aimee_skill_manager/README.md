# Skill Manager Brick

ROS2 brick for Skill Management and Execution for the AIMEE Robot.

## Overview

This brick executes skills (movement, arm control, camera) with:
- **Action-based interface**: ExecuteSkill action server
- **Safety checks**: Validation before execution
- **Progress feedback**: Real-time execution status
- **Skill registry**: Pluggable skill system

## Built-in Skills

| Skill | Description | Actions |
|-------|-------------|---------|
| `movement` | UGV base control | move_forward, move_backward, turn_left, turn_right, stop |
| `arm_control` | RoArm-M3 control | wave, open_gripper, close_gripper, raise, lower |
| `camera` | OBSBOT control | track_face, follow, look_at_me, stop_tracking |
| `greeting` | Greeting responses | greet |

## Architecture

```
┌─────────────────┐      Intent       ┌──────────────────┐
│  Intent Router  │ ─────────────────→│  Skill Manager   │
│                 │                   │  (this brick)    │
└─────────────────┘                   └────────┬─────────┘
        │                                      │
        │                                      │ ExecuteSkill Action
        ↓                                      ↓
┌─────────────────┐                   ┌──────────────────┐
│  /tts/speak     │←──────────────────│  Skills          │
│  (response)     │   Response        │  - Movement      │
└─────────────────┘                   │  - Arm           │
                                      │  - Camera        │
                                      └──────────────────┘
```

## Installation

```bash
cd ~/aimee-robot-ws
source setup_env.sh
colcon build --packages-select aimee_skill_manager
source install/setup.bash
```

## Usage

### Start Skill Manager

```bash
ros2 run aimee_skill_manager skill_manager_node
```

### Test with Action Client

```python
import rclpy
from rclpy.action import ActionClient
from aimee_msgs.action import ExecuteSkill

rclpy.init()
node = rclpy.create_node('test_skill')
client = ActionClient(node, ExecuteSkill, '/skill/execute')

# Wait for server
client.wait_for_server()

# Create goal
goal = ExecuteSkill.Goal()
goal.skill_id = "movement"
goal.user_input = "move forward"
goal.session_id = "test"

# Send goal
future = client.send_goal_async(goal)
rclpy.spin_until_future_complete(node, future)

# Get result
goal_handle = future.result()
result_future = goal_handle.get_result_async()
rclpy.spin_until_future_complete(node, result_future)

result = result_future.result().result
print(f"Success: {result.success}")
print(f"Response: {result.response_text}")
```

## ROS2 Interface

### Action Server

| Action | Type | Description |
|--------|------|-------------|
| `/skill/execute` | `aimee_msgs/ExecuteSkill` | Execute a skill with feedback |

**Goal**: skill_id, user_input, robot_state, user_context, session_id
**Feedback**: status, current_action, progress, can_cancel
**Result**: success, response_text, error_message, actions_performed

### Subscribers

| Topic | Type | Description |
|-------|------|-------------|
| `/intent/classified` | `aimee_msgs/Intent` | Automatic skill execution |
| `/robot/state` | `aimee_msgs/RobotState` | Current robot state |

### Publishers

| Topic | Type | Description |
|-------|------|-------------|
| `/skill/status` | `std_msgs/String` | Execution status |
| `/tts/speak` | `std_msgs/String` | Response text |

## Creating Custom Skills

```python
from aimee_skill_manager.brick.skill_manager import Skill, SkillContext, SkillResult

class MySkill(Skill):
    def __init__(self):
        super().__init__(name="my_skill", description="My custom skill")
    
    async def execute(self, context: SkillContext) -> SkillResult:
        # Parse command
        command = context.user_input
        
        # Execute action
        # TODO: Publish to hardware controller
        
        return SkillResult(
            success=True,
            response_text="Done!",
            execution_time=1.0
        )
    
    def validate(self, context: SkillContext) -> bool:
        # Safety check
        return True
```

## Safety Features

- **Timeout protection**: Skills timeout after default 30s
- **Cancellation**: Skills can be cancelled mid-execution
- **Validation**: Pre-execution safety checks
- **Workspace bounds**: Arm movement constraints

## Configuration

```yaml
# config/brick_config.yaml
default_timeout: 30.0
enable_safety_checks: true

safety:
  max_linear_speed: 0.5
  max_angular_speed: 1.0
  workspace_bounds:
    x_min: -0.5
    x_max: 0.5
```

## Integration with Intent Router

The Skill Manager automatically executes skills when intents are classified:

```
User: "Move forward"
  ↓
Intent Router → intent=MOVEMENT, skill_name="movement"
  ↓
Skill Manager → Execute "movement" skill
  ↓
TTS: "Moving forward"
```

## Future Enhancements

1. **Hardware Integration**: Connect to actual UGV/arm/camera drivers
2. **More Skills**: Navigation, manipulation, vision tasks
3. **Skill Chaining**: "Pick up object and move to kitchen"
4. **Learning**: Learn new skills from demonstrations
5. **Recovery**: Automatic retry on failure

See `docs/FUTURE_ENHANCEMENTS.md` for details.

## License

MPL-2.0
