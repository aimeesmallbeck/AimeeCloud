#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
skill_manager Brick - Skill Manager and execution engine for AIMEE robot

This brick executes skills (movement, arm, camera) with:
- Action-based interface (ExecuteSkill)
- Safety checks and validation
- Progress feedback
- Skill registry and management
"""

import asyncio
import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional, Any, Type

from arduino.app_utils import brick

# Configure logging
logger = logging.getLogger(__name__)


class SkillStatus(Enum):
    """Skill execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class SkillResult:
    """Result of skill execution."""
    success: bool = False
    response_text: str = ""
    error_message: str = ""
    execution_time: float = 0.0
    actions_performed: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SkillContext:
    """Context for skill execution."""
    user_input: str = ""
    user_context: Dict[str, Any] = field(default_factory=dict)
    robot_state: Optional[Any] = None
    session_id: str = ""
    skill_id: str = ""


class Skill(ABC):
    """Abstract base class for skills."""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self._cancelled = False
    
    @abstractmethod
    async def execute(self, context: SkillContext) -> SkillResult:
        """
        Execute the skill.
        
        Args:
            context: Execution context
            
        Returns:
            SkillResult
        """
        pass
    
    def cancel(self):
        """Cancel skill execution."""
        self._cancelled = True
        logger.info(f"Skill {self.name} cancelled")
    
    def is_cancelled(self) -> bool:
        """Check if skill was cancelled."""
        return self._cancelled
    
    def validate(self, context: SkillContext) -> bool:
        """
        Validate if skill can be executed.
        
        Args:
            context: Execution context
            
        Returns:
            True if valid
        """
        return True


class MoveSkill(Skill):
    """Movement skill for UGV base."""
    
    def __init__(self):
        super().__init__(
            name="movement",
            description="Control robot movement (forward, backward, turn, stop)"
        )
    
    async def execute(self, context: SkillContext) -> SkillResult:
        """Execute movement command."""
        start_time = time.time()
        
        # Parse command from user input
        command = self._parse_command(context.user_input)
        
        logger.info(f"Executing movement: {command}")
        
        # TODO: Publish to movement controller topic
        # For now, simulate execution
        await asyncio.sleep(0.5)
        
        if self.is_cancelled():
            return SkillResult(
                success=False,
                error_message="Cancelled"
            )
        
        execution_time = time.time() - start_time
        
        return SkillResult(
            success=True,
            response_text=f"Moving {command['direction']}",
            execution_time=execution_time,
            actions_performed=[{
                "type": "movement",
                "direction": command['direction'],
                "speed": command.get('speed', 0.5)
            }]
        )
    
    def _parse_command(self, text: str) -> Dict[str, Any]:
        """Parse movement command from text."""
        text_lower = text.lower()
        
        if "forward" in text_lower or "ahead" in text_lower:
            return {"direction": "forward", "speed": 0.5}
        elif "backward" in text_lower or "back" in text_lower:
            return {"direction": "backward", "speed": 0.5}
        elif "left" in text_lower:
            return {"direction": "left", "speed": 0.3}
        elif "right" in text_lower:
            return {"direction": "right", "speed": 0.3}
        elif "stop" in text_lower:
            return {"direction": "stop", "speed": 0.0}
        else:
            return {"direction": "forward", "speed": 0.5}


class ArmSkill(Skill):
    """Arm control skill for RoArm-M3."""
    
    def __init__(self):
        super().__init__(
            name="arm_control",
            description="Control robotic arm (move, gripper, wave)"
        )
    
    async def execute(self, context: SkillContext) -> SkillResult:
        """Execute arm command."""
        start_time = time.time()
        
        command = self._parse_command(context.user_input)
        
        logger.info(f"Executing arm control: {command}")
        
        # TODO: Publish to arm controller
        await asyncio.sleep(0.5)
        
        if self.is_cancelled():
            return SkillResult(
                success=False,
                error_message="Cancelled"
            )
        
        execution_time = time.time() - start_time
        
        return SkillResult(
            success=True,
            response_text=f"Arm {command['action']}",
            execution_time=execution_time,
            actions_performed=[{
                "type": "arm",
                "action": command['action']
            }]
        )
    
    def _parse_command(self, text: str) -> Dict[str, Any]:
        """Parse arm command from text."""
        text_lower = text.lower()
        
        if "wave" in text_lower:
            return {"action": "wave"}
        elif "open" in text_lower:
            return {"action": "open_gripper"}
        elif "close" in text_lower:
            return {"action": "close_gripper"}
        elif "raise" in text_lower or "up" in text_lower:
            return {"action": "raise"}
        elif "lower" in text_lower or "down" in text_lower:
            return {"action": "lower"}
        else:
            return {"action": "move"}


class CameraSkill(Skill):
    """Camera control skill for OBSBOT."""
    
    def __init__(self):
        super().__init__(
            name="camera",
            description="Control camera (track, look, follow)"
        )
    
    async def execute(self, context: SkillContext) -> SkillResult:
        """Execute camera command."""
        start_time = time.time()
        
        command = self._parse_command(context.user_input)
        
        logger.info(f"Executing camera control: {command}")
        
        # TODO: Publish to camera controller
        await asyncio.sleep(0.3)
        
        if self.is_cancelled():
            return SkillResult(
                success=False,
                error_message="Cancelled"
            )
        
        execution_time = time.time() - start_time
        
        return SkillResult(
            success=True,
            response_text=f"Camera {command['action']}",
            execution_time=execution_time,
            actions_performed=[{
                "type": "camera",
                "action": command['action']
            }]
        )
    
    def _parse_command(self, text: str) -> Dict[str, Any]:
        """Parse camera command from text."""
        text_lower = text.lower()
        
        if "track" in text_lower:
            return {"action": "track_face"}
        elif "follow" in text_lower:
            return {"action": "follow"}
        elif "look" in text_lower:
            return {"action": "look_at_me"}
        elif "stop" in text_lower:
            return {"action": "stop_tracking"}
        else:
            return {"action": "look_at_me"}


class GreetingSkill(Skill):
    """Greeting skill."""
    
    def __init__(self):
        super().__init__(
            name="greeting",
            description="Respond to greetings"
        )
    
    async def execute(self, context: SkillContext) -> SkillResult:
        """Execute greeting."""
        responses = [
            "Hello! I'm AIMEE. How can I help you?",
            "Hi there! Ready to assist.",
            "Greetings! What would you like me to do?"
        ]
        
        import random
        response = random.choice(responses)
        
        return SkillResult(
            success=True,
            response_text=response,
            execution_time=0.0
        )


class SkillManagerBrickError(Exception):
    """Custom exception for SkillManagerBrick."""
    pass


@brick
class SkillManagerBrick:
    """
    Skill Manager and execution engine for AIMEE robot.
    
    This brick manages skill registration and execution:
    - Register skills by name
    - Execute skills with context
    - Handle skill cancellation
    - Provide execution feedback
    
    Attributes:
        default_timeout: Default skill execution timeout
        enable_safety_checks: Enable safety validation
        debug: Enable debug logging
        
    Example:
        >>> brick = SkillManagerBrick()
        >>> await brick.initialize()
        >>> 
        >>> # Register built-in skills
        >>> brick.register_skill(MoveSkill())
        >>> brick.register_skill(ArmSkill())
        >>> 
        >>> # Execute skill
        >>> context = SkillContext(user_input="move forward")
        >>> result = await brick.execute_skill("movement", context)
        >>> 
        >>> await brick.shutdown()
    """
    
    def __init__(
        self,
        default_timeout: float = 30.0,
        enable_safety_checks: bool = True,
        debug: bool = False,
        **kwargs
    ):
        """
        Initialize the SkillManagerBrick.
        
        Args:
            default_timeout: Default execution timeout (seconds)
            enable_safety_checks: Enable safety validation
            debug: Enable debug logging
            **kwargs: Additional arguments
        """
        self.default_timeout = default_timeout
        self.enable_safety_checks = enable_safety_checks
        self.debug = debug
        
        # State
        self._initialized = False
        self._lock = asyncio.Lock()
        
        # Skill registry
        self._skills: Dict[str, Skill] = {}
        self._current_skill: Optional[Skill] = None
        
        # Statistics
        self._execution_count = 0
        self._success_count = 0
        
        # Feedback callbacks
        self._feedback_callbacks: List[Callable[[str, str, float], None]] = []
        
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        
        logger.info(
            f"SkillManagerBrick initialized: timeout={default_timeout}s, "
            f"safety={enable_safety_checks}"
        )
    
    async def initialize(self) -> "SkillManagerBrick":
        """
        Initialize the skill manager and register built-in skills.
        
        Returns:
            self for method chaining
        """
        async with self._lock:
            if self._initialized:
                return self
            
            # Register built-in skills
            self._register_builtin_skills()
            
            self._initialized = True
            logger.info(f"SkillManagerBrick initialized with {len(self._skills)} skills")
        
        return self
    
    def _register_builtin_skills(self):
        """Register built-in skills."""
        builtin_skills = [
            MoveSkill(),
            ArmSkill(),
            CameraSkill(),
            GreetingSkill(),
        ]
        
        for skill in builtin_skills:
            self.register_skill(skill)
    
    def register_skill(self, skill: Skill):
        """
        Register a skill.
        
        Args:
            skill: Skill instance
        """
        self._skills[skill.name] = skill
        logger.debug(f"Registered skill: {skill.name}")
    
    def get_skill(self, name: str) -> Optional[Skill]:
        """
        Get a skill by name.
        
        Args:
            name: Skill name
            
        Returns:
            Skill or None
        """
        return self._skills.get(name)
    
    def list_skills(self) -> List[str]:
        """
        List all registered skill names.
        
        Returns:
            List of skill names
        """
        return list(self._skills.keys())
    
    async def execute_skill(
        self,
        skill_name: str,
        context: SkillContext,
        timeout: Optional[float] = None
    ) -> SkillResult:
        """
        Execute a skill.
        
        Args:
            skill_name: Name of skill to execute
            context: Execution context
            timeout: Execution timeout (None for default)
            
        Returns:
            SkillResult
        """
        if not self._initialized:
            raise SkillManagerBrickError("Brick not initialized")
        
        if timeout is None:
            timeout = self.default_timeout
        
        # Get skill
        skill = self._skills.get(skill_name)
        if not skill:
            return SkillResult(
                success=False,
                error_message=f"Unknown skill: {skill_name}"
            )
        
        # Validate
        if self.enable_safety_checks:
            if not skill.validate(context):
                return SkillResult(
                    success=False,
                    error_message="Safety validation failed"
                )
        
        # Execute with timeout
        self._current_skill = skill
        self._execution_count += 1
        
        try:
            # Report starting
            self._report_feedback(skill_name, "starting", 0.0)
            
            # Execute skill with timeout
            result = await asyncio.wait_for(
                skill.execute(context),
                timeout=timeout
            )
            
            # Report completion
            self._report_feedback(skill_name, "completed", 1.0)
            
            if result.success:
                self._success_count += 1
            
            return result
            
        except asyncio.TimeoutError:
            logger.error(f"Skill {skill_name} timed out after {timeout}s")
            self._report_feedback(skill_name, "timeout", 0.0)
            return SkillResult(
                success=False,
                error_message=f"Timeout after {timeout}s"
            )
            
        except Exception as e:
            logger.error(f"Skill {skill_name} execution failed: {e}")
            self._report_feedback(skill_name, "error", 0.0)
            return SkillResult(
                success=False,
                error_message=str(e)
            )
            
        finally:
            self._current_skill = None
    
    async def cancel_current_skill(self) -> bool:
        """
        Cancel the currently executing skill.
        
        Returns:
            True if a skill was cancelled
        """
        if self._current_skill:
            self._current_skill.cancel()
            return True
        return False
    
    def on_feedback(self, callback: Callable[[str, str, float], None]):
        """
        Register feedback callback.
        
        Args:
            callback: Function(skill_name, status, progress)
        """
        self._feedback_callbacks.append(callback)
    
    def _report_feedback(self, skill_name: str, status: str, progress: float):
        """Report execution feedback."""
        for callback in self._feedback_callbacks:
            try:
                callback(skill_name, status, progress)
            except Exception as e:
                logger.error(f"Feedback callback error: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status."""
        return {
            "initialized": self._initialized,
            "registered_skills": self.list_skills(),
            "execution_count": self._execution_count,
            "success_count": self._success_count,
            "current_skill": self._current_skill.name if self._current_skill else None,
        }
    
    async def shutdown(self):
        """Clean up resources."""
        async with self._lock:
            if not self._initialized:
                return
            
            logger.info("Shutting down SkillManagerBrick...")
            
            # Cancel current skill
            if self._current_skill:
                self._current_skill.cancel()
            
            # Clear skills
            self._skills.clear()
            self._feedback_callbacks.clear()
            
            self._initialized = False
            logger.info("Shutdown complete")
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.shutdown()
