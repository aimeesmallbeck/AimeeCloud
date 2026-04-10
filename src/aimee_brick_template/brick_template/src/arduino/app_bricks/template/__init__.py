# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
{BRICK_NAME} Brick for Aimee Robot

{BRICK_DESCRIPTION}

Usage:
    from arduino.app_bricks.{BRICK_NAME} import {BrickClassName}
    
    brick = {BrickClassName}(
        param1="value1",
        param2="value2"
    )
    await brick.initialize()
    
    # Use brick functionality
    result = await brick.do_something()
    
    await brick.shutdown()
"""

from .{BRICK_NAME} import {BrickClassName}

__all__ = ["{BrickClassName}"]
__version__ = "0.1.0"
