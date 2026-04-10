# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
llm_server Brick for Aimee Robot

LLM Action Server with streaming and preemption support

Usage:
    from aimee_llm_server.brick.llm_server import LLMServerBrick, LLMRequest
    
    brick = LLMServerBrick(
        backend="llama_cpp_server",
        server_url="http://localhost:8080"
    )
    await brick.initialize()
    
    # Generate with streaming
    request = LLMRequest(prompt="Hello, how are you?")
    async for feedback in brick.generate_stream(request):
        print(feedback.partial_response)
    
    await brick.shutdown()
"""

from .llm_server import (
    LLMServerBrick,
    LLMRequest,
    LLMFeedback,
    LLMResult,
    LLMBackend,
    LLMServerBrickError
)

__all__ = [
    "LLMServerBrick",
    "LLMRequest",
    "LLMFeedback",
    "LLMResult",
    "LLMBackend",
    "LLMServerBrickError"
]
__version__ = "0.1.0"
