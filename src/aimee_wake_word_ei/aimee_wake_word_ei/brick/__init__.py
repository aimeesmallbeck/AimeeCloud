# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
wake_word_ei Brick for Aimee Robot

Wake word detection using Edge Impulse keyword spotting model

Usage:
    from arduino.app_bricks.wake_word_ei import WakeWordEIBrick
    
    brick = WakeWordEIBrick(
        param1="value1",
        param2="value2"
    )
    await brick.initialize()
    
    # Use brick functionality
    result = await brick.do_something()
    
    await brick.shutdown()
"""

from .wake_word_ei import WakeWordEIBrick

__all__ = ["WakeWordEIBrick"]
__version__ = "0.1.0"
