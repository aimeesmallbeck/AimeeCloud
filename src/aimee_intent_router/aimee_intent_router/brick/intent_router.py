#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
intent_router Brick - Intent Router with LLM-based intent classification

This brick receives transcribed text, classifies intent using LLM,
and routes to appropriate skill for execution.

Features:
- LLM-based intent classification
- Skill routing and execution
- Conversation context management
- Response generation
- TTS integration for responses
"""

import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional, Any, Tuple

from arduino.app_utils import brick

# Configure logging
logger = logging.getLogger(__name__)


class IntentType(Enum):
    """Supported intent types."""
    GREETING = "greeting"
    MOVEMENT = "movement"
    ARM_CONTROL = "arm_control"
    CAMERA = "camera"
    SYSTEM = "system"
    CONVERSATION = "conversation"
    QUESTION = "question"
    CLOUD_SKILL = "cloud_skill"
    UNKNOWN = "unknown"


@dataclass
class Intent:
    """Classified intent."""
    intent_type: IntentType
    action: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    raw_text: str = ""
    requires_skill: bool = False
    skill_name: str = ""


@dataclass
class ConversationContext:
    """Conversation context for multi-turn interactions."""
    session_id: str
    history: List[Dict[str, str]] = field(default_factory=list)
    last_intent: Optional[Intent] = None
    entities: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass
class RouterResult:
    """Result of intent routing."""
    success: bool = False
    response: str = ""
    intent: Optional[Intent] = None
    skill_executed: bool = False
    error_message: str = ""
    processing_time: float = 0.0


class IntentRouterBrickError(Exception):
    """Custom exception for IntentRouterBrick errors."""
    pass


@brick
class IntentRouterBrick:
    """
    Intent Router with LLM-based intent classification.
    
    This brick processes transcribed text:
    1. Classifies intent using LLM
    2. Routes to appropriate skill
    3. Generates response
    4. Manages conversation context
    
    Attributes:
        system_prompt: System prompt for LLM intent classification
        max_context_length: Maximum conversation history length
        confidence_threshold: Minimum confidence for intent classification
        enable_conversation_mode: Enable multi-turn conversation support
        debug: Enable debug logging
        
    Example:
        >>> brick = IntentRouterBrick(
        ...     confidence_threshold=0.7,
        ...     enable_conversation_mode=True
        ... )
        >>> await brick.initialize()
        >>> 
        >>> result = await brick.process_text("move forward")
        >>> print(f"Intent: {result.intent.intent_type}")
        >>> 
        >>> await brick.shutdown()
    """
    
    DEFAULT_SYSTEM_PROMPT = """You are an intent classifier for a robot assistant named AIMEE.
Your task is to analyze user commands and classify them into intents.

Available intents:
- GREETING: "hello", "hi", "good morning"
- MOVEMENT: "move forward", "turn left", "go backward", "stop"
- ARM_CONTROL: "raise arm", "lower arm", "open gripper", "wave"
- CAMERA: "look at me", "track face", "stop tracking"
- SYSTEM: "what's your name", "who are you", "status"
- QUESTION: General questions
- CLOUD_SKILL: "weather", "news", "story", "game", "help", general chat
- CONVERSATION: Chat, not a command

Respond in JSON format:
{
    "intent": "MOVEMENT",
    "action": "move_forward",
    "parameters": {"speed": 0.5},
    "confidence": 0.95,
    "requires_skill": true,
    "response": "Moving forward"
}
"""
    
    def __init__(
        self,
        system_prompt: Optional[str] = None,
        max_context_length: int = 10,
        confidence_threshold: float = 0.6,
        enable_conversation_mode: bool = True,
        conversation_timeout: float = 60.0,
        fallback_to_chat: bool = True,
        chat_routing: str = "cloud",
        debug: bool = False,
        **kwargs
    ):
        """
        Initialize the IntentRouterBrick.
        
        Args:
            system_prompt: System prompt for LLM classification
            max_context_length: Max conversation history exchanges
            confidence_threshold: Minimum confidence for classification
            enable_conversation_mode: Enable multi-turn conversations
            conversation_timeout: Seconds before conversation expires
            fallback_to_chat: Fallback to chat response if no skill match
            chat_routing: "cloud" or "local_llm" — where chat/question intents go
            debug: Enable debug logging
            **kwargs: Additional arguments
        """
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.max_context_length = max_context_length
        self.confidence_threshold = confidence_threshold
        self.enable_conversation_mode = enable_conversation_mode
        self.conversation_timeout = conversation_timeout
        self.fallback_to_chat = fallback_to_chat
        self.chat_routing = chat_routing
        self.debug = debug
        
        # State
        self._initialized = False
        self._lock = asyncio.Lock()
        
        # Conversation contexts (session_id -> ConversationContext)
        self._contexts: Dict[str, ConversationContext] = {}
        
        # Intent handlers
        self._skill_handlers: Dict[str, Callable[[Intent, ConversationContext], Any]] = {}
        self._response_handlers: List[Callable[[str, Intent], None]] = []
        
        # Noise words — second line of defense for ASR hallucinations
        self.noise_words: set[str] = {
            "huh", "who", "um", "mm", "mhm", "uh", "eh", "hm", "hmm",
            "ah", "oh", "er", "ha", "uhh", "ahh", "mmm", "uhuh", "huhuh"
        }
        
        # Statistics
        self._processed_count = 0
        self._skill_execution_count = 0
        
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        
        logger.info(
            f"IntentRouterBrick initialized: confidence={confidence_threshold}, "
            f"conversation_mode={enable_conversation_mode}"
        )
    
    async def initialize(self) -> "IntentRouterBrick":
        """
        Initialize the intent router.
        
        Returns:
            self for method chaining
        """
        async with self._lock:
            if self._initialized:
                return self
            
            self._initialized = True
            logger.info("IntentRouterBrick initialization complete")
        
        return self
    
    def register_skill_handler(
        self,
        skill_name: str,
        handler: Callable[[Intent, ConversationContext], Any]
    ):
        """
        Register a handler for a skill.
        
        Args:
            skill_name: Name of the skill
            handler: Callback function(intent, context) -> result
        """
        self._skill_handlers[skill_name] = handler
        logger.debug(f"Registered skill handler: {skill_name}")
    
    def on_response(self, handler: Callable[[str, Intent], None]):
        """
        Register a handler for responses.
        
        Args:
            handler: Callback function(response_text, intent)
        """
        self._response_handlers.append(handler)
    
    async def process_text(
        self,
        text: str,
        session_id: Optional[str] = None,
        llm_generate_func: Optional[Callable] = None
    ) -> RouterResult:
        """
        Process transcribed text and route to appropriate handler.
        
        Args:
            text: Transcribed user text
            session_id: Conversation session ID
            llm_generate_func: Async function for LLM generation
            
        Returns:
            RouterResult with classification and execution results
        """
        if not self._initialized:
            raise IntentRouterBrickError("Brick not initialized")
        
        start_time = time.time()
        
        # Get or create session
        if not session_id:
            session_id = str(uuid.uuid4())[:8]
        
        context = self._get_or_create_context(session_id)
        
        # Noise gate: drop obvious ASR garbage before spending LLM tokens
        cleaned = text.strip().lower().rstrip('.').rstrip('?').rstrip('!')
        if len(cleaned) < 2 or cleaned in self.noise_words:
            logger.debug(f"Ignored noise/too short: '{text}'")
            return RouterResult(
                success=True,
                intent=Intent(
                    intent_type=IntentType.UNKNOWN,
                    action="noise",
                    confidence=0.0,
                    raw_text=text,
                    requires_skill=False
                ),
                response="",
                processing_time=time.time() - start_time
            )
        
        try:
            # Step 1: Classify intent using LLM
            intent = await self._classify_intent(text, context, llm_generate_func)
            
            # Step 2: Execute skill if required
            skill_result = None
            if intent.requires_skill and intent.skill_name:
                skill_result = await self._execute_skill(intent, context)
            
            # Step 3: Generate response
            response = await self._generate_response(
                text, intent, skill_result, context, llm_generate_func
            )
            
            # Step 4: Update context
            self._update_context(context, text, response, intent)
            
            # Step 5: Notify handlers
            for handler in self._response_handlers:
                try:
                    handler(response, intent)
                except Exception as e:
                    logger.error(f"Response handler error: {e}")
            
            # Update statistics
            self._processed_count += 1
            if intent.requires_skill:
                self._skill_execution_count += 1
            
            processing_time = time.time() - start_time
            
            return RouterResult(
                success=True,
                response=response,
                intent=intent,
                skill_executed=intent.requires_skill and skill_result is not None,
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Intent routing failed: {e}")
            processing_time = time.time() - start_time
            
            return RouterResult(
                success=False,
                error_message=str(e),
                processing_time=processing_time
            )
    
    async def _classify_intent(
        self,
        text: str,
        context: ConversationContext,
        llm_generate_func: Optional[Callable]
    ) -> Intent:
        """
        Classify intent using LLM.
        
        Args:
            text: User text to classify
            context: Conversation context
            llm_generate_func: LLM generation function
            
        Returns:
            Classified Intent
        """
        if not llm_generate_func:
            # Fallback: simple keyword-based classification
            return self._fallback_classify(text)
        
        # Build prompt with context
        prompt = self._build_classification_prompt(text, context)
        
        try:
            # Call LLM for classification
            llm_response = await llm_generate_func(
                prompt=prompt,
                system_context=self.system_prompt,
                max_tokens=60,
                temperature=0.3  # Low temperature for consistent classification
            )
            
            # Parse JSON response
            result_text = llm_response.get('response', '')
            
            # Extract JSON from response (handle markdown code blocks)
            json_str = self._extract_json(result_text)
            
            if json_str:
                result = json.loads(json_str)
                
                intent_type = IntentType(result.get('intent', 'UNKNOWN').lower())
                
                return Intent(
                    intent_type=intent_type,
                    action=result.get('action', ''),
                    parameters=result.get('parameters', {}),
                    confidence=result.get('confidence', 0.0),
                    raw_text=text,
                    requires_skill=result.get('requires_skill', False),
                    skill_name=result.get('skill_name', result.get('action', ''))
                )
            else:
                # No valid JSON, fallback
                return self._fallback_classify(text)
                
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse LLM response as JSON: {e}")
            return self._fallback_classify(text)
        except Exception as e:
            logger.error(f"Intent classification error: {e}")
            return self._fallback_classify(text)
    
    def _fallback_classify(self, text: str) -> Intent:
        """
        Fallback keyword-based classification.
        
        Used when LLM classification fails or unavailable.
        """
        text_lower = text.lower()
        
        # Simple keyword matching
        if any(word in text_lower for word in ['hello', 'hi', 'hey', 'good morning']):
            return Intent(
                intent_type=IntentType.GREETING,
                action="greet",
                confidence=0.8,
                raw_text=text,
                requires_skill=False
            )
        
        elif any(word in text_lower for word in ['forward', 'backward', 'left', 'right', 'move', 'go', 'turn']):
            action = "move_forward" if "forward" in text_lower else "move"
            if "backward" in text_lower or "back" in text_lower:
                action = "move_backward"
            elif "left" in text_lower:
                action = "turn_left"
            elif "right" in text_lower:
                action = "turn_right"
            elif "stop" in text_lower:
                action = "stop"
            
            return Intent(
                intent_type=IntentType.MOVEMENT,
                action=action,
                confidence=0.7,
                raw_text=text,
                requires_skill=True,
                skill_name="movement"
            )
        
        elif any(word in text_lower for word in ['arm', 'gripper', 'hand', 'wave']):
            return Intent(
                intent_type=IntentType.ARM_CONTROL,
                action="arm_control",
                confidence=0.7,
                raw_text=text,
                requires_skill=True,
                skill_name="arm_control"
            )
        
        elif any(word in text_lower for word in ['camera', 'look', 'track', 'see']):
            return Intent(
                intent_type=IntentType.CAMERA,
                action="camera_control",
                confidence=0.7,
                raw_text=text,
                requires_skill=True,
                skill_name="camera"
            )
        
        elif "?" in text or any(word in text_lower for word in [
            'what', 'when', 'where', 'why', 'who', 'how',
            'is ', 'are ', 'can ', 'could ', 'do ', 'does ', 'did ',
            'will ', 'would ', 'should ', 'have ', 'has ', 'was ', 'were '
        ]):
            return Intent(
                intent_type=IntentType.QUESTION,
                action="answer_question",
                confidence=0.6,
                raw_text=text,
                requires_skill=False
            )
        
        else:
            return Intent(
                intent_type=IntentType.CONVERSATION,
                action="chat",
                confidence=0.5,
                raw_text=text,
                requires_skill=False
            )
    
    async def _execute_skill(
        self,
        intent: Intent,
        context: ConversationContext
    ) -> Any:
        """
        Execute skill handler for intent.
        
        Args:
            intent: Classified intent
            context: Conversation context
            
        Returns:
            Skill execution result
        """
        handler = self._skill_handlers.get(intent.skill_name)
        
        if not handler:
            logger.warning(f"No handler registered for skill: {intent.skill_name}")
            return None
        
        try:
            # Call handler
            if asyncio.iscoroutinefunction(handler):
                result = await handler(intent, context)
            else:
                result = handler(intent, context)
            
            logger.info(f"Executed skill: {intent.skill_name}")
            return result
            
        except Exception as e:
            logger.error(f"Skill execution failed: {e}")
            return None
    
    async def _generate_response(
        self,
        text: str,
        intent: Intent,
        skill_result: Any,
        context: ConversationContext,
        llm_generate_func: Optional[Callable]
    ) -> str:
        """
        Generate response for user.
        
        Args:
            text: Original user text
            intent: Classified intent
            skill_result: Result from skill execution
            context: Conversation context
            llm_generate_func: LLM generation function
            
        Returns:
            Response text
        """
        # Use LLM to generate response if available
        if llm_generate_func and (intent.intent_type == IntentType.CONVERSATION or 
                                   intent.intent_type == IntentType.QUESTION):
            
            prompt = f"User: {text}\nIntent: {intent.intent_type.value}\n"
            if skill_result:
                prompt += f"Skill result: {skill_result}\n"
            prompt += "Respond naturally:"
            
            try:
                llm_response = await llm_generate_func(
                    prompt=prompt,
                    system_context="You are AIMEE, a helpful robot. Be concise.",
                    max_tokens=80,
                    temperature=0.7
                )
                return llm_response.get('response', 'I understand.')
            except Exception as e:
                logger.warning(f"LLM response generation failed: {e}")
        
        # Cloud-routed intents do not generate local TTS responses
        if self.chat_routing == "cloud" and intent.intent_type in (
            IntentType.QUESTION, IntentType.CONVERSATION, IntentType.CLOUD_SKILL
        ):
            return ""
        
        # Predefined responses for specific intents (used when LLM unavailable)
        response_map = {
            IntentType.GREETING: "Hello! I'm AIMEE. How can I help you?",
            IntentType.MOVEMENT: f"{intent.action.replace('_', ' ').title()}." if intent.action else "Moving.",
            IntentType.ARM_CONTROL: f"Controlling arm: {intent.action}." if intent.action else "Arm control.",
            IntentType.CAMERA: "Camera adjusted.",
            IntentType.SYSTEM: "I'm AIMEE, your robot assistant.",
            IntentType.QUESTION: "That's an interesting question.",
            IntentType.CONVERSATION: "I'm listening.",
            IntentType.CLOUD_SKILL: "Let me check that for you.",
            IntentType.UNKNOWN: "",
        }
        
        return response_map.get(
            intent.intent_type,
            "I understand." if not self.fallback_to_chat else "I'm listening."
        )
    
    def _build_classification_prompt(
        self,
        text: str,
        context: ConversationContext
    ) -> str:
        """Build classification prompt with context."""
        prompt = f"Classify this command: \"{text}\"\n\n"
        
        # Add conversation history if available
        if context.history and self.enable_conversation_mode:
            prompt += "Context:\n"
            for i, exchange in enumerate(context.history[-3:]):  # Last 3 exchanges
                prompt += f"  User: {exchange.get('user', '')}\n"
                prompt += f"  Assistant: {exchange.get('assistant', '')}\n"
            prompt += "\n"
        
        prompt += "Respond with JSON only."
        
        return prompt
    
    def _extract_json(self, text: str) -> Optional[str]:
        """Extract JSON from text (handles markdown code blocks)."""
        # Try to find JSON in code block
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            if end > start:
                return text[start:end].strip()
        
        # Try to find JSON between braces
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            return text[start:end+1]
        
        return None
    
    def _get_or_create_context(self, session_id: str) -> ConversationContext:
        """Get or create conversation context."""
        if session_id not in self._contexts:
            self._contexts[session_id] = ConversationContext(session_id=session_id)
        
        context = self._contexts[session_id]
        
        # Check if context expired
        if time.time() - context.timestamp > self.conversation_timeout:
            # Reset context but keep session ID
            self._contexts[session_id] = ConversationContext(session_id=session_id)
            return self._contexts[session_id]
        
        return context
    
    def _update_context(
        self,
        context: ConversationContext,
        user_text: str,
        assistant_response: str,
        intent: Intent
    ):
        """Update conversation context."""
        context.history.append({
            'user': user_text,
            'assistant': assistant_response,
            'intent': intent.intent_type.value,
            'timestamp': time.time()
        })
        
        context.last_intent = intent
        context.timestamp = time.time()
        
        # Trim history
        while len(context.history) > self.max_context_length:
            context.history.pop(0)
    
    def clear_context(self, session_id: str):
        """Clear conversation context for a session."""
        if session_id in self._contexts:
            del self._contexts[session_id]
            logger.debug(f"Cleared context: {session_id}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status."""
        return {
            "initialized": self._initialized,
            "processed_count": self._processed_count,
            "skill_execution_count": self._skill_execution_count,
            "active_sessions": len(self._contexts),
            "registered_skills": list(self._skill_handlers.keys()),
            "conversation_mode": self.enable_conversation_mode,
        }
    
    async def shutdown(self):
        """Clean up resources."""
        async with self._lock:
            if not self._initialized:
                return
            
            logger.info("Shutting down IntentRouterBrick...")
            
            # Clear contexts
            self._contexts.clear()
            
            # Clear handlers
            self._skill_handlers.clear()
            self._response_handlers.clear()
            
            self._initialized = False
            logger.info("Shutdown complete")
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.shutdown()
