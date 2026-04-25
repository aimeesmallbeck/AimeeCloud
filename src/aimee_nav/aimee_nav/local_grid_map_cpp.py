#!/usr/bin/env python3
"""
Drop-in C++-accelerated replacement for LocalGridMap.
All heavy ray-casting and inflation runs in C++.
"""

import math
import time
from typing import List, Tuple
import numpy as np

try:
    from aimee_nav._core import RobotCentricGridMap as _RobotCentricGridMap
except ImportError:
    _RobotCentricGridMap = None


class LocalGridMapCpp:
    """API-compatible replacement for LocalGridMap using C++ core."""

    def __init__(
        self,
        size_m: float = 5.0,
        resolution_m: float = 0.05,
        inflation_m: float = 0.15,
        decay_time_s: float = 10.0,
        max_occupied: int = 127,
        min_free: int = 1,
    ) -> None:
        if _RobotCentricGridMap is None:
            raise RuntimeError("C++ extension _core is not available")

        self.resolution = resolution_m
        self.size_m = size_m
        self.inflation_m = inflation_m
        self.decay_time_s = decay_time_s
        self.max_occupied = max_occupied
        self.min_free = min_free

        self.grid_size = int(round(size_m / resolution_m))
        if self.grid_size % 2 == 0:
            self.grid_size += 1

        self.origin_x = 0.0
        self.origin_y = 0.0
        self.origin_theta = 0.0

        self._cpp = _RobotCentricGridMap(size_m, resolution_m, inflation_m, decay_time_s)
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=np.int8)
        self._last_decay_time = 0.0

    # ------------------------------------------------------------------
    # Coordinate transforms
    # ------------------------------------------------------------------

    def _world_to_grid(self, wx: float, wy: float) -> Tuple[int, int]:
        dx = wx - self.origin_x
        dy = wy - self.origin_y
        cos_t = math.cos(-self.origin_theta)
        sin_t = math.sin(-self.origin_theta)
        gx = dx * cos_t - dy * sin_t
        gy = dx * sin_t + dy * cos_t

        half = self.grid_size // 2
        col = int(round(gx / self.resolution)) + half
        row = int(round(gy / self.resolution)) + half
        return row, col

    def _grid_to_world(self, row: int, col: int) -> Tuple[float, float]:
        half = self.grid_size // 2
        gx = (col - half) * self.resolution
        gy = (row - half) * self.resolution

        cos_t = math.cos(self.origin_theta)
        sin_t = math.sin(self.origin_theta)
        wx = gx * cos_t - gy * sin_t + self.origin_x
        wy = gx * sin_t + gy * cos_t + self.origin_y
        return wx, wy

    # ------------------------------------------------------------------
    # Grid access
    # ------------------------------------------------------------------

    def get_cell(self, wx: float, wy: float) -> int:
        row, col = self._world_to_grid(wx, wy)
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            return int(self.grid[row, col])
        return -1

    def is_occupied(self, wx: float, wy: float) -> bool:
        return self.get_cell(wx, wy) >= 100

    def is_free(self, wx: float, wy: float) -> bool:
        val = self.get_cell(wx, wy)
        return 0 < val < 100

    def is_unknown(self, wx: float, wy: float) -> bool:
        val = self.get_cell(wx, wy)
        return val == 0 or val == -1

    # ------------------------------------------------------------------
    # Grid update from lidar
    # ------------------------------------------------------------------

    def update_from_scan(
        self,
        ranges: List[float],
        angles_deg: List[float],
        robot_x: float,
        robot_y: float,
        robot_theta: float,
        max_range_m: float = 8.0,
    ) -> None:
        self.origin_x = robot_x
        self.origin_y = robot_y
        self.origin_theta = robot_theta

        self._cpp.update_from_scan(ranges, angles_deg, robot_x, robot_y, robot_theta, max_range_m)
        # C++ returns a flat list; reshape to 2D numpy array
        self.grid = np.array(self._cpp.grid_array(), dtype=np.int8).reshape(
            (self.grid_size, self.grid_size)
        )

    # ------------------------------------------------------------------
    # Path planning helpers
    # ------------------------------------------------------------------

    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int, float]]:
        neighbors = []
        directions = [
            (-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
            (-1, -1, 1.414), (-1, 1, 1.414), (1, -1, 1.414), (1, 1, 1.414),
        ]
        for dr, dc, cost in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                if self.grid[r, c] < 100:
                    neighbors.append((r, c, cost))
        return neighbors

    def cell_cost(self, row: int, col: int) -> float:
        if not (0 <= row < self.grid_size and 0 <= col < self.grid_size):
            return float('inf')
        val = self.grid[row, col]
        if val >= 100:
            return float('inf')
        return 1.0

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    @staticmethod
    def _bresenham(x0: int, y0: int, x1: int, y1: int) -> List[Tuple[int, int]]:
        points: List[Tuple[int, int]] = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            points.append((y0, x0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

        return points

    def to_occupancy_grid_data(self) -> np.ndarray:
        # Use C++ helper which already does the conversion
        return self._cpp.to_occupancy_grid_data()
