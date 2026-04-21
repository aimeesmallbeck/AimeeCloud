#!/usr/bin/env python3
"""Stub brick module for AIMEE testing."""
import logging

logger = logging.getLogger(__name__)


def brick(cls):
    """Stub brick decorator - registers and returns the class."""
    # In real implementation, this registers the brick
    logger.info(f"Registered brick: {cls.__name__}")
    return cls


class Brick:
    """Base brick class stub."""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def start(self):
        """Start the brick."""
        self.logger.info(f"{self.__class__.__name__} started")
    
    def stop(self):
        """Stop the brick."""
        self.logger.info(f"{self.__class__.__name__} stopped")


class BrickError(Exception):
    """Brick error."""
    pass
