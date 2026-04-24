#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Lightweight 2D occupancy grid using NumPy.

RAM-efficient local map centered on the robot. Obstacles are inserted
via ray-casting from the robot pose. Cells decay over time to handle
dynamic obstacles.

Grid values:
    0   = unknown / unobserved
    1-99 = free space (higher = more recently observed)
    100-127 = occupied (100 + occupancy confidence)
    -1 = out of bounds (treated as unknown)
"""

import math
import time
from typing import List, Tuple, Optional
import numpy as np


class LocalGridMap:
    """
    A robot-centric occupancy grid that moves with the robot.
    """

    def __init__(
        self,
        size_m: float = 5.0,
        resolution_m: float = 0.05,
        inflation_m: float = 0.15,
        decay_time_s: float = 10.0,
        max_occupied: int = 127,
        min_free: int = 1,
    ) -> None:
        self.resolution = resolution_m
        self.size_m = size_m
        self.inflation_m = inflation_m
        self.decay_time_s = decay_time_s
        self.max_occupied = max_occupied
        self.min_free = min_free

        self.grid_size = int(round(size_m / resolution_m))
        if self.grid_size % 2 == 0:
            self.grid_size += 1  # Ensure odd size for center cell

        self.origin_x = 0.0
        self.origin_y = 0.0
        self.origin_theta = 0.0

        # Grid: 0 = unknown, 1-99 = free, 100-127 = occupied
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=np.int8)
        self._last_decay_time = 0.0

    # ------------------------------------------------------------------
    # Coordinate transforms
    # ------------------------------------------------------------------

    def _world_to_grid(self, wx: float, wy: float) -> Tuple[int, int]:
        """Convert world coordinates to grid indices."""
        # Rotate into grid frame
        dx = wx - self.origin_x
        dy = wy - self.origin_y
        cos_t = math.cos(-self.origin_theta)
        sin_t = math.sin(-self.origin_theta)
        gx = dx * cos_t - dy * sin_t
        gy = dx * sin_t + dy * cos_t

        # Convert to cell indices
        half = self.grid_size // 2
        col = int(round(gx / self.resolution)) + half
        row = int(round(gy / self.resolution)) + half
        return row, col

    def _grid_to_world(self, row: int, col: int) -> Tuple[float, float]:
        """Convert grid indices to world coordinates."""
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
        """Return grid value at world coordinates."""
        row, col = self._world_to_grid(wx, wy)
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            return int(self.grid[row, col])
        return -1

    def is_occupied(self, wx: float, wy: float) -> bool:
        """Check if a world position is occupied."""
        val = self.get_cell(wx, wy)
        return val >= 100

    def is_free(self, wx: float, wy: float) -> bool:
        """Check if a world position is known free."""
        val = self.get_cell(wx, wy)
        return 0 < val < 100

    def is_unknown(self, wx: float, wy: float) -> bool:
        """Check if a world position is unknown."""
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
        """
        Update the grid using a lidar scan.

        Args:
            ranges: distances in meters (inf for no return)
            angles_deg: angles in degrees, 0 = forward
            robot_x, robot_y: robot position in world frame
            robot_theta: robot heading in radians
            max_range_m: maximum usable range
        """
        self.origin_x = robot_x
        self.origin_y = robot_y
        self.origin_theta = robot_theta

        # Decay old cells
        self._decay()

        robot_row, robot_col = self._world_to_grid(robot_x, robot_y)
        if not (0 <= robot_row < self.grid_size and 0 <= robot_col < self.grid_size):
            return

        inflation_cells = int(round(self.inflation_m / self.resolution))

        for dist, angle_deg in zip(ranges, angles_deg):
            if dist <= 0 or math.isinf(dist) or math.isnan(dist):
                continue
            if dist > max_range_m:
                dist = max_range_m

            angle_rad = math.radians(angle_deg) + robot_theta
            end_x = robot_x + dist * math.cos(angle_rad)
            end_y = robot_y + dist * math.sin(angle_rad)

            end_row, end_col = self._world_to_grid(end_x, end_y)

            # Mark free cells along ray
            for r, c in self._bresenham(robot_row, robot_col, end_row, end_col):
                if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                    if self.grid[r, c] < 100:
                        self.grid[r, c] = min(99, max(self.min_free, self.grid[r, c] + 10))

            # Mark obstacle at end of ray (with inflation)
            if 0 <= end_row < self.grid_size and 0 <= end_col < self.grid_size:
                self._mark_obstacle(end_row, end_col, inflation_cells)

    def _mark_obstacle(self, row: int, col: int, inflation_cells: int) -> None:
        """Mark a cell and its neighbors as occupied."""
        for dr in range(-inflation_cells, inflation_cells + 1):
            for dc in range(-inflation_cells, inflation_cells + 1):
                if dr * dr + dc * dc > inflation_cells * inflation_cells:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                    self.grid[r, c] = self.max_occupied

    def _decay(self) -> None:
        """Gradually reduce cell confidence to handle dynamic obstacles."""
        now = time.time()
        if now - self._last_decay_time < 0.5:
            return
        self._last_decay_time = now

        # Free cells: reduce toward 0 (unknown)
        free_mask = (self.grid > 0) & (self.grid < 100)
        self.grid[free_mask] = np.maximum(0, self.grid[free_mask] - 2)

        # Occupied cells: reduce toward 0 (unknown) slowly
        occ_mask = self.grid >= 100
        self.grid[occ_mask] = np.maximum(0, self.grid[occ_mask] - 1)

    # ------------------------------------------------------------------
    # Path planning helpers
    # ------------------------------------------------------------------

    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int, float]]:
        """
        Return traversable 8-connected neighbors with costs.
        Diagonal cost = sqrt(2), straight = 1.
        """
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
        """Return traversal cost for a cell (higher = more expensive)."""
        if not (0 <= row < self.grid_size and 0 <= col < self.grid_size):
            return float('inf')
        val = self.grid[row, col]
        if val >= 100:
            return float('inf')
        # Unknown and free are both traversable; unknown treated as free
        # for local planning since we only know the current scan.
        return 1.0

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    @staticmethod
    def _bresenham(x0: int, y0: int, x1: int, y1: int) -> List[Tuple[int, int]]:
        """Integer Bresenham line algorithm. Returns list of (row, col)."""
        points: List[Tuple[int, int]] = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            points.append((y0, x0))  # (row, col)
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
        """
        Convert internal grid to ROS OccupancyGrid format (-1 to 100).
        Returns a new array suitable for nav_msgs/OccupancyGrid.data.
        """
        out = np.zeros_like(self.grid, dtype=np.int8)
        out[self.grid == 0] = -1           # Unknown
        out[(self.grid > 0) & (self.grid < 100)] = 0   # Free
        out[self.grid >= 100] = 100        # Occupied
        return out
