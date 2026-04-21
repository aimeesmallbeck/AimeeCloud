# LLM Server Brick

ROS2 Action Server for LLM inference with streaming and preemption support for the AIMEE Robot.

## Overview

This brick provides non-blocking LLM inference:
- **ROS2 Action**: `LLMGenerate` with streaming feedback
- **Preemption**: Cancel ongoing generation for responsive interrupts
- **Backends**: llama.cpp server (OpenAI-compatible API)
- **Session Context**: Multi-turn conversation support

## Features

- **Streaming**: Token-by-token feedback during generation
- **Preemption**: Cancel requests for responsive interrupt handling
- **Session Context**: Maintains conversation history per session
- **Non-blocking**: Async/await for concurrent request handling
- **Memory Efficient**: Optimized for Arduino UNO Q (4GB RAM)

## Architecture

```
┌─────────────────┐      LLMGenerate Action       ┌─────────────────┐
│  Intent Router  │ ─────(Goal/Feedback/Result)──→│  LLM Server     │
│  or Skill       │                                │  (this brick)   │
└─────────────────┘                                └────────┬────────┘
                                                          │
                                                          │ HTTP API
                                                          ↓
                                                   ┌───────────────┐
                                                   │ llama.cpp     │
                                                   │ server        │
                                                   │ :8080         │
                                                   └───────┬───────┘
                                                           │
                                                           │ GGUF model
                                                           ↓
                                                   ┌───────────────┐
                                                   │ ~/models/*.gguf│
                                                   └───────────────┘
```

## Dependencies

### llama.cpp Server

Install llama.cpp server:

```bash
# Clone llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Build with server support
make LLAMA_CUDA=OFF  # For CPU-only build

# Or install via package manager
# sudo apt install llama-cpp-server  # if available
```

### Python Dependencies

```bash
pip3 install aiohttp
```

## Installation

```bash
cd ~/aimee-robot-ws
source setup_env.sh
colcon build --packages-select aimee_msgs aimee_llm_server
source install/setup.bash
```

## Usage

### Start llama.cpp Server

```bash
# Start server with a model
./llama-server \
  -m ~/models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf \
  -c 2048 \
  --host 127.0.0.1 \
  --port 8080

# Or with SmolLM2 for lower RAM usage
./llama-server \
  -m ~/models/SmolLM2-135M.Q4_K_M.gguf \
  -c 1024 \
  --port 8080
```

### Start LLM Server Node

```bash
ros2 run aimee_llm_server llm_server_node
```

### With Parameters

```bash
ros2 run aimee_llm_server llm_server_node \
  --ros-args \
  -p server_url:=http://localhost:8080 \
  -p default_max_tokens:=200 \
  -p default_temperature:=0.8 \
  -p debug:=true
```

## ROS2 Action Interface

### Action: `/llm/generate`

**Goal (LLMGenerate)**:
```python
string prompt              # User prompt
string system_context      # System prompt/persona
int32 max_tokens           # Max tokens (default: 150)
float32 temperature        # Temperature (default: 0.7)
bool stream                # Enable streaming (default: true)
string session_id          # Session for context
```

**Feedback (LLMGenerate)**:
```python
string partial_response    # Cumulative text
int32 tokens_generated     # Tokens so far
int32 tokens_total         # Estimated total
bool is_complete           # Generation finished
string current_word        # Current word
```

**Result (LLMGenerate)**:
```python
string response            # Complete text
bool success               # Success flag
string error_message       # Error if failed
float32 generation_time    # Time taken
int32 tokens_generated     # Total tokens
int32 tokens_input         # Input tokens
```

## Example Usage

### Test with Action Client

```python
import rclpy
from rclpy.action import ActionClient
from aimee_msgs.action import LLMGenerate

rclpy.init()
node = rclpy.create_node('test_llm_client')
client = ActionClient(node, LLMGenerate, '/llm/generate')

# Wait for server
client.wait_for_server()

# Create goal
goal = LLMGenerate.Goal()
goal.prompt = "What is the weather like?"
goal.system_context = "You are a helpful robot."
goal.max_tokens = 100
goal.temperature = 0.7
goal.stream = True
goal.session_id = "test_session"

# Send goal with feedback callback
def feedback_cb(feedback):
    print(f"Partial: {feedback.feedback.partial_response}")

future = client.send_goal_async(goal, feedback_cb)
rclpy.spin_until_future_complete(node, future)

goal_handle = future.result()
result_future = goal_handle.get_result_async()
rclpy.spin_until_future_complete(node, result_future)

result = result_future.result().result
print(f"Final: {result.response}")
```

### Cancel Ongoing Generation

```python
# To preempt/cancel an ongoing generation
goal_handle.cancel_goal_async()
```

## Available Models

| Model | Size | RAM | Speed | Quality |
|-------|------|-----|-------|---------|
| SmolLM2-135M | 135M | ~200MB | Fastest | Basic |
| Qwen2.5-0.5B | 0.5B | ~400MB | Fast | Good |
| TinyLlama-1.1B | 1.1B | ~700MB | Medium | Better |

Recommendation for Arduino UNO Q: **Qwen2.5-0.5B** for good balance.

## Session Context

The server maintains conversation context per session:

```python
# First message
goal.session_id = "user_123"
goal.prompt = "Hello, I'm Bob"

# Follow-up (context automatically included)
goal.prompt = "What's my name?"
# Server will remember "Bob" from previous exchange
```

Context is automatically managed (last 10 exchanges kept).

## Preemption Use Cases

1. **New Wake Word**: User says wake word during TTS → Cancel current LLM generation
2. **Stop Command**: User says "stop" → Preempt immediately
3. **Timeout**: Generation taking too long → Preempt and return partial result

## Performance Tuning

### For Low Latency (Arduino UNO Q)

```bash
# Use smaller model
./llama-server -m ~/models/SmolLM2-135M.Q4_K_M.gguf -c 1024

# Reduce max_tokens in requests
goal.max_tokens = 50  # Shorter responses

# Increase temperature for faster convergence
goal.temperature = 0.9
```

### For Better Quality

```bash
# Use larger model
./llama-server -m ~/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -c 2048

# Adjust temperature
goal.temperature = 0.5  # More focused
```

## Troubleshooting

### Connection Refused

```bash
# Check if llama.cpp server is running
curl http://localhost:8080/health

# Start server
./llama-server -m ~/models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf --port 8080
```

### Out of Memory

- Use smaller model (SmolLM2-135M)
- Reduce `-c` (context size): `-c 1024` instead of `-c 2048`
- Reduce `max_tokens` in requests
- Close other applications

### Slow Generation

- Check CPU usage: `htop`
- Use quantized models (Q4_K_M)
- Consider enabling GPU if available (CUDA/Metal)

## Future Enhancements

### Planned Features
1. **Direct llama.cpp bindings**: No HTTP server needed
2. **Ollama backend**: Support for Ollama API
3. **Model hot-swapping**: Switch models at runtime
4. **Batch processing**: Multiple prompts in parallel
5. **Caching**: Cache common responses

See `docs/FUTURE_ENHANCEMENTS.md` for more details.

## License

MPL-2.0
