# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
skill_manager Brick for Aimee Robot

Skill Manager and execution engine for AIMEE robot

Usage:
    from aimee_skill_manager.brick.skill_manager import (
        SkillManagerBrick, Skill, SkillContext, SkillResult
    )
    
    brick = SkillManagerBrick()
    await brick.initialize()
    
    # Execute a skill
    context = SkillContext(user_input="move forward")
    result = await brick.execute_skill("movement", context)
    print(f"Result: {result.response_text}")
    
    await brick.shutdown()
"""

from .skill_manager import (
    SkillManagerBrick,
    Skill,
    SkillContext,
    SkillResult,
    MoveSkill,
    ArmSkill,
    CameraSkill,
    GreetingSkill,
    SkillManagerBrickError
)

__all__ = [
    "SkillManagerBrick",
    "Skill",
    "SkillContext",
    "SkillResult",
    "MoveSkill",
    "ArmSkill",
    "CameraSkill",
    "GreetingSkill",
    "SkillManagerBrickError"
]
__version__ = "0.1.0"
