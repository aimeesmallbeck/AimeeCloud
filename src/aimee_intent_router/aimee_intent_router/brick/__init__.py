# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
intent_router Brick for Aimee Robot

Intent Router with LLM-based intent classification

Usage:
    from aimee_intent_router.brick.intent_router import (
        IntentRouterBrick, Intent, IntentType, RouterResult
    )
    
    brick = IntentRouterBrick(
        confidence_threshold=0.7,
        enable_conversation_mode=True
    )
    await brick.initialize()
    
    # Register a skill handler
    def move_handler(intent, context):
        print(f"Moving: {intent.action}")
        return "Moved successfully"
    
    brick.register_skill_handler("movement", move_handler)
    
    # Process text
    result = await brick.process_text("move forward", llm_generate_func=my_llm_func)
    print(f"Response: {result.response}")
    
    await brick.shutdown()
"""

from .intent_router import (
    IntentRouterBrick,
    Intent,
    IntentType,
    RouterResult,
    ConversationContext,
    IntentRouterBrickError
)

__all__ = [
    "IntentRouterBrick",
    "Intent",
    "IntentType",
    "RouterResult",
    "ConversationContext",
    "IntentRouterBrickError"
]
__version__ = "0.1.0"
