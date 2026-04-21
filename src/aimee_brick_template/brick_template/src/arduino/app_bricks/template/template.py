#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
{BRICK_NAME} Brick - {BRICK_DESCRIPTION}

This brick provides {BRICK_FUNCTIONALITY} for the Aimee robot.
"""

import asyncio
import logging
from typing import Optional, Any, Dict
from arduino.app_utils import brick

# Configure logging
logger = logging.getLogger(__name__)


class {BrickClassName}Error(Exception):
    """Custom exception for {BrickClassName} errors."""
    pass


@brick
class {BrickClassName}:
    """
    {BRICK_DESCRIPTION}
    
    Attributes:
        param1: Description of param1
        param2: Description of param2
        
    Example:
        >>> brick = {BrickClassName}(param1="value")
        >>> await brick.initialize()
        >>> result = await brick.do_something()
        >>> await brick.shutdown()
    """
    
    def __init__(
        self,
        param1: str = "default_value",
        param2: int = 42,
        debug: bool = False,
        **kwargs
    ):
        """
        Initialize the {BrickClassName}.
        
        Args:
            param1: Description of param1
            param2: Description of param2
            debug: Enable debug logging
            **kwargs: Additional arguments
        """
        self.param1 = param1
        self.param2 = param2
        self.debug = debug
        
        # Internal state
        self._initialized = False
        self._running = False
        self._lock = asyncio.Lock()
        
        if debug:
            logging.basicConfig(level=logging.DEBUG)
            
        logger.info(f"{BrickClassName} initialized with param1={param1}, param2={param2}")
        
    async def initialize(self) -> "{BrickClassName}":
        """
        Initialize hardware connections and resources.
        
        Returns:
            self for method chaining
            
        Raises:
            {BrickClassName}Error: If initialization fails
        """
        async with self._lock:
            if self._initialized:
                logger.warning("Already initialized, skipping")
                return self
                
            try:
                # Initialize hardware/resources here
                logger.info("Initializing hardware...")
                
                # Example: Connect to device, load models, etc.
                await self._connect()
                
                self._initialized = True
                logger.info("Initialization complete")
                
            except Exception as e:
                logger.error(f"Initialization failed: {e}")
                raise {BrickClassName}Error(f"Failed to initialize: {e}")
                
        return self
        
    async def _connect(self):
        """Internal method to establish connections."""
        # Implement connection logic here
        pass
        
    async def do_something(self, input_data: str) -> Dict[str, Any]:
        """
        Main functionality of the brick.
        
        Args:
            input_data: Input data to process
            
        Returns:
            Dictionary with results
            
        Raises:
            {BrickClassName}Error: If operation fails
        """
        if not self._initialized:
            raise {BrickClassName}Error("Brick not initialized. Call initialize() first.")
            
        async with self._lock:
            try:
                logger.debug(f"Processing: {input_data}")
                
                # Implement main functionality here
                result = await self._process(input_data)
                
                return {
                    "success": True,
                    "result": result,
                    "param1": self.param1,
                }
                
            except Exception as e:
                logger.error(f"Operation failed: {e}")
                return {
                    "success": False,
                    "error": str(e),
                }
                
    async def _process(self, input_data: str) -> Any:
        """Internal processing method."""
        # Implement processing logic here
        return f"Processed: {input_data}"
        
    async def shutdown(self):
        """
        Clean up resources and shutdown.
        
        This method should be called when the brick is no longer needed.
        """
        async with self._lock:
            if not self._initialized:
                return
                
            logger.info("Shutting down...")
            
            try:
                # Cleanup resources here
                self._running = False
                self._initialized = False
                
                logger.info("Shutdown complete")
                
            except Exception as e:
                logger.error(f"Error during shutdown: {e}")
                
    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of the brick.
        
        Returns:
            Dictionary with status information
        """
        return {
            "initialized": self._initialized,
            "running": self._running,
            "param1": self.param1,
            "param2": self.param2,
        }
        
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.shutdown()
