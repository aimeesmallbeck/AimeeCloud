#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
llm_server Brick - LLM Action Server with streaming and preemption support

This brick provides non-blocking LLM inference with:
- Streaming responses (token-by-token feedback)
- Request preemption (cancel ongoing generation)
- Multiple backend support (llama.cpp server, direct bindings)
- Session context management
- Memory-efficient for Arduino UNO Q (4GB RAM)

Features:
- OpenAI-compatible API support (llama.cpp server)
- Async/await for non-blocking operation
- Preemption for responsive interrupt handling
- Configurable model parameters
"""

import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional, Any, AsyncIterator

import aiohttp
from arduino.app_utils import brick

# Configure logging
logger = logging.getLogger(__name__)


class LLMBackend(Enum):
    """Supported LLM backends."""
    LLAMA_CPP_SERVER = "llama_cpp_server"  # HTTP API
    LLAMA_CPP_DIRECT = "llama_cpp_direct"  # Python bindings (future)
    OLLAMA = "ollama"  # Ollama API (future)
    OPENAI = "openai"  # OpenAI API (future)


@dataclass
class LLMRequest:
    """LLM generation request."""
    prompt: str
    system_context: str = ""
    max_tokens: int = 150
    temperature: float = 0.7
    stream: bool = True
    session_id: str = ""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: float = field(default_factory=time.time)


@dataclass
class LLMFeedback:
    """Streaming feedback from LLM generation."""
    partial_response: str = ""
    tokens_generated: int = 0
    tokens_total: int = 0
    is_complete: bool = False
    current_word: str = ""
    timestamp: float = field(default_factory=time.time)


@dataclass
class LLMResult:
    """Final LLM generation result."""
    response: str = ""
    success: bool = False
    error_message: str = ""
    generation_time: float = 0.0
    tokens_generated: int = 0
    tokens_input: int = 0
    request_id: str = ""
    session_id: str = ""


class LLMServerBrickError(Exception):
    """Custom exception for LLMServerBrick errors."""
    pass


@brick
class LLMServerBrick:
    """
    LLM Action Server with streaming and preemption support.
    
    This brick provides non-blocking LLM inference using llama.cpp server
    or other backends. It supports streaming responses and request preemption.
    
    Attributes:
        backend: LLM backend type (default: llama_cpp_server)
        server_url: URL for llama.cpp server (default: http://localhost:8080)
        model_path: Path to GGUF model file (for direct backend)
        default_max_tokens: Default maximum tokens to generate
        default_temperature: Default sampling temperature
        timeout_seconds: Request timeout
        debug: Enable debug logging
        
    Example:
        >>> brick = LLMServerBrick(
        ...     backend="llama_cpp_server",
        ...     server_url="http://localhost:8080"
        ... )
        >>> await brick.initialize()
        >>> 
        >>> # Non-blocking generation with streaming
        >>> async for feedback in brick.generate_stream(request):
        ...     print(feedback.partial_response)
        >>> 
        >>> # Or get final result
        >>> result = await brick.generate(request)
        >>> print(result.response)
        >>> 
        >>> await brick.shutdown()
    """
    
    def __init__(
        self,
        backend: str = "llama_cpp_server",
        server_url: str = "http://localhost:8080",
        model_path: Optional[str] = None,
        default_max_tokens: int = 150,
        default_temperature: float = 0.7,
        timeout_seconds: float = 60.0,
        max_context_length: int = 2048,
        debug: bool = False,
        **kwargs
    ):
        """
        Initialize the LLMServerBrick.
        
        Args:
            backend: LLM backend (llama_cpp_server, llama_cpp_direct)
            server_url: URL for llama.cpp server API
            model_path: Path to GGUF model (for direct backend)
            default_max_tokens: Default max tokens
            default_temperature: Default temperature (0.0-1.0)
            timeout_seconds: Request timeout
            max_context_length: Maximum context window
            debug: Enable debug logging
            **kwargs: Additional arguments
        """
        self.backend = LLMBackend(backend)
        self.server_url = server_url.rstrip('/')
        self.model_path = model_path
        self.default_max_tokens = default_max_tokens
        self.default_temperature = default_temperature
        self.timeout_seconds = timeout_seconds
        self.max_context_length = max_context_length
        self.debug = debug
        
        # State
        self._initialized = False
        self._lock = asyncio.Lock()
        
        # HTTP session (for llama.cpp server)
        self._session: Optional[aiohttp.ClientSession] = None
        
        # Current generation (for preemption)
        self._current_request: Optional[LLMRequest] = None
        self._current_task: Optional[asyncio.Task] = None
        self._preempt_event = asyncio.Event()
        
        # Statistics
        self._generation_count = 0
        self._total_tokens_generated = 0
        
        # Session context storage (for multi-turn conversations)
        self._session_contexts: Dict[str, List[Dict[str, str]]] = {}
        self._max_session_history = 10
        
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        
        logger.info(
            f"LLMServerBrick initialized: backend={backend}, "
            f"server={server_url}, max_tokens={default_max_tokens}"
        )
    
    async def initialize(self) -> "LLMServerBrick":
        """
        Initialize the LLM server connection.
        
        Returns:
            self for method chaining
            
        Raises:
            LLMServerBrickError: If initialization fails
        """
        async with self._lock:
            if self._initialized:
                logger.warning("Already initialized, skipping")
                return self
            
            try:
                if self.backend == LLMBackend.LLAMA_CPP_SERVER:
                    await self._init_llama_cpp_server()
                elif self.backend == LLMBackend.LLAMA_CPP_DIRECT:
                    await self._init_llama_cpp_direct()
                else:
                    raise LLMServerBrickError(f"Unsupported backend: {self.backend}")
                
                self._initialized = True
                logger.info("LLMServerBrick initialization complete")
                
            except Exception as e:
                logger.error(f"Initialization failed: {e}")
                raise LLMServerBrickError(f"Failed to initialize: {e}")
        
        return self
    
    async def _init_llama_cpp_server(self):
        """Initialize connection to llama.cpp server."""
        # Create HTTP session
        timeout = aiohttp.ClientTimeout(total=self.timeout_seconds)
        self._session = aiohttp.ClientSession(timeout=timeout)
        
        # Test connection
        try:
            async with self._session.get(f"{self.server_url}/health") as resp:
                if resp.status == 200:
                    logger.info(f"Connected to llama.cpp server at {self.server_url}")
                else:
                    logger.warning(
                        f"llama.cpp server returned status {resp.status}"
                    )
        except aiohttp.ClientError as e:
            logger.warning(
                f"Could not connect to llama.cpp server: {e}. "
                "Will retry on first request."
            )
    
    async def _init_llama_cpp_direct(self):
        """Initialize llama.cpp Python bindings (future)."""
        raise LLMServerBrickError(
            "Direct llama.cpp backend not yet implemented. "
            "Use llama_cpp_server backend."
        )
    
    async def generate(self, request: LLMRequest) -> LLMResult:
        """
        Generate text with LLM (blocking, returns final result).
        
        Args:
            request: LLM generation request
            
        Returns:
            LLMResult with generated text and metadata
            
        Raises:
            LLMServerBrickError: If generation fails
        """
        if not self._initialized:
            raise LLMServerBrickError("Brick not initialized")
        
        start_time = time.time()
        
        try:
            if self.backend == LLMBackend.LLAMA_CPP_SERVER:
                return await self._generate_llama_cpp_server(request, start_time)
            else:
                raise LLMServerBrickError(f"Unsupported backend: {self.backend}")
                
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return LLMResult(
                success=False,
                error_message=str(e),
                generation_time=time.time() - start_time,
                request_id=request.request_id,
                session_id=request.session_id
            )
    
    async def generate_stream(
        self,
        request: LLMRequest,
        feedback_callback: Optional[Callable[[LLMFeedback], None]] = None
    ) -> AsyncIterator[LLMFeedback]:
        """
        Generate text with streaming feedback.
        
        Args:
            request: LLM generation request
            feedback_callback: Optional callback for each feedback chunk
            
        Yields:
            LLMFeedback with partial results
            
        Raises:
            LLMServerBrickError: If generation fails
        """
        if not self._initialized:
            raise LLMServerBrickError("Brick not initialized")
        
        if self.backend == LLMBackend.LLAMA_CPP_SERVER:
            async for feedback in self._generate_stream_llama_cpp_server(request):
                if feedback_callback:
                    feedback_callback(feedback)
                yield feedback
        else:
            raise LLMServerBrickError(f"Unsupported backend: {self.backend}")
    
    async def _generate_llama_cpp_server(
        self,
        request: LLMRequest,
        start_time: float
    ) -> LLMResult:
        """Generate using llama.cpp server (non-streaming)."""
        # Build messages with context
        messages = self._build_messages(request)
        
        # Build request payload
        payload = {
            "messages": messages,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "stream": False
        }
        
        try:
            async with self._session.post(
                f"{self.server_url}/v1/chat/completions",
                json=payload
            ) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    raise LLMServerBrickError(f"Server error {resp.status}: {error_text}")
                
                data = await resp.json()
                
                # Extract response
                choice = data.get("choices", [{}])[0]
                message = choice.get("message", {})
                content = message.get("content", "")
                
                # Update statistics
                self._generation_count += 1
                tokens_generated = data.get("usage", {}).get("completion_tokens", 0)
                tokens_input = data.get("usage", {}).get("prompt_tokens", 0)
                self._total_tokens_generated += tokens_generated
                
                # Store in session context
                self._update_session_context(request.session_id, request.prompt, content)
                
                return LLMResult(
                    response=content,
                    success=True,
                    generation_time=time.time() - start_time,
                    tokens_generated=tokens_generated,
                    tokens_input=tokens_input,
                    request_id=request.request_id,
                    session_id=request.session_id
                )
                
        except asyncio.TimeoutError:
            raise LLMServerBrickError("Request timed out")
        except aiohttp.ClientError as e:
            raise LLMServerBrickError(f"Connection error: {e}")
    
    async def _generate_stream_llama_cpp_server(
        self,
        request: LLMRequest
    ) -> AsyncIterator[LLMFeedback]:
        """Generate using llama.cpp server (streaming)."""
        # Build messages with context
        messages = self._build_messages(request)
        
        # Build request payload
        payload = {
            "messages": messages,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "stream": True
        }
        
        self._current_request = request
        accumulated_text = ""
        tokens_generated = 0
        
        try:
            async with self._session.post(
                f"{self.server_url}/v1/chat/completions",
                json=payload
            ) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    raise LLMServerBrickError(f"Server error {resp.status}: {error_text}")
                
                # Process SSE stream
                async for line in resp.content:
                    # Check for preemption
                    if self._preempt_event.is_set():
                        logger.info(f"Generation preempted: {request.request_id}")
                        self._preempt_event.clear()
                        yield LLMFeedback(
                            partial_response=accumulated_text,
                            tokens_generated=tokens_generated,
                            is_complete=True,
                            current_word="[PREEMPTED]"
                        )
                        return
                    
                    line = line.decode('utf-8').strip()
                    if not line or line.startswith(':'):
                        continue
                    
                    if line.startswith('data: '):
                        data_str = line[6:]  # Remove 'data: ' prefix
                        
                        if data_str == '[DONE]':
                            break
                        
                        try:
                            data = json.loads(data_str)
                            choice = data.get("choices", [{}])[0]
                            delta = choice.get("delta", {})
                            content = delta.get("content", "")
                            
                            if content:
                                accumulated_text += content
                                tokens_generated += 1
                                
                                # Extract current word (rough approximation)
                                words = accumulated_text.split()
                                current_word = words[-1] if words else ""
                                
                                yield LLMFeedback(
                                    partial_response=accumulated_text,
                                    tokens_generated=tokens_generated,
                                    current_word=current_word,
                                    is_complete=False
                                )
                                
                        except json.JSONDecodeError:
                            continue
                
                # Final feedback
                self._generation_count += 1
                self._total_tokens_generated += tokens_generated
                
                # Store in session context
                self._update_session_context(
                    request.session_id,
                    request.prompt,
                    accumulated_text
                )
                
                yield LLMFeedback(
                    partial_response=accumulated_text,
                    tokens_generated=tokens_generated,
                    is_complete=True
                )
                
        except asyncio.TimeoutError:
            raise LLMServerBrickError("Request timed out")
        except aiohttp.ClientError as e:
            raise LLMServerBrickError(f"Connection error: {e}")
        finally:
            self._current_request = None
    
    def _build_messages(self, request: LLMRequest) -> List[Dict[str, str]]:
        """Build message list with system prompt and context."""
        messages = []
        
        # System prompt
        if request.system_context:
            messages.append({
                "role": "system",
                "content": request.system_context
            })
        else:
            # Default system prompt
            messages.append({
                "role": "system",
                "content": (
                    "You are AIMEE, a helpful robot assistant. "
                    "Be concise and direct in your responses."
                )
            })
        
        # Add session context (conversation history)
        if request.session_id and request.session_id in self._session_contexts:
            messages.extend(self._session_contexts[request.session_id])
        
        # Add current prompt
        messages.append({"role": "user", "content": request.prompt})
        
        return messages
    
    def _update_session_context(
        self,
        session_id: str,
        user_message: str,
        assistant_response: str
    ):
        """Update conversation history for a session."""
        if not session_id:
            return
        
        if session_id not in self._session_contexts:
            self._session_contexts[session_id] = []
        
        context = self._session_contexts[session_id]
        
        # Add exchange
        context.append({"role": "user", "content": user_message})
        context.append({"role": "assistant", "content": assistant_response})
        
        # Trim to max history
        while len(context) > self._max_session_history * 2:
            context.pop(0)
            context.pop(0)
    
    async def preempt(self) -> bool:
        """
        Preempt (cancel) the current generation.
        
        Returns:
            True if there was a generation to preempt
        """
        if self._current_request and self._current_task:
            logger.info(f"Preempting generation: {self._current_request.request_id}")
            self._preempt_event.set()
            self._current_task.cancel()
            try:
                await self._current_task
            except asyncio.CancelledError:
                pass
            return True
        return False
    
    def clear_session(self, session_id: str):
        """Clear conversation context for a session."""
        if session_id in self._session_contexts:
            del self._session_contexts[session_id]
            logger.debug(f"Cleared session: {session_id}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the brick."""
        return {
            "initialized": self._initialized,
            "backend": self.backend.value,
            "server_url": self.server_url,
            "generation_count": self._generation_count,
            "total_tokens_generated": self._total_tokens_generated,
            "active_sessions": len(self._session_contexts),
            "current_request": self._current_request.request_id if self._current_request else None,
        }
    
    async def shutdown(self):
        """Clean up resources and shutdown."""
        async with self._lock:
            if not self._initialized:
                return
            
            logger.info("Shutting down LLMServerBrick...")
            
            try:
                # Preempt any ongoing generation
                await self.preempt()
                
                # Close HTTP session
                if self._session:
                    await self._session.close()
                    self._session = None
                
                # Clear contexts
                self._session_contexts.clear()
                
                self._initialized = False
                logger.info("Shutdown complete")
                
            except Exception as e:
                logger.error(f"Error during shutdown: {e}")
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.shutdown()
