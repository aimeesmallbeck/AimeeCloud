#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Simple A* path planner on the local occupancy grid.

Suitable for small grids (e.g., 100×100). Uses a binary heap for the
open set. Plans from robot center to goal in grid coordinates.
"""

import math
from typing import List, Tuple, Optional, Set
import heapq

from aimee_nav.local_grid_map import LocalGridMap


class SimplePlanner:
    """
    A* planner on a LocalGridMap.
    """

    def __init__(self, grid_map: LocalGridMap) -> None:
        self.grid = grid_map
        self._last_path: List[Tuple[float, float]] = []

    def plan(
        self,
        start_world: Tuple[float, float],
        goal_world: Tuple[float, float],
    ) -> Optional[List[Tuple[float, float]]]:
        """
        Plan a path from start to goal in world coordinates.

        Returns a list of (x, y) waypoints in world coordinates,
        or None if no path exists.
        """
        start_row, start_col = self.grid._world_to_grid(start_world[0], start_world[1])
        goal_row, goal_col = self.grid._world_to_grid(goal_world[0], goal_world[1])

        if not (0 <= start_row < self.grid.grid_size and 0 <= start_col < self.grid.grid_size):
            return None
        if not (0 <= goal_row < self.grid.grid_size and 0 <= goal_col < self.grid.grid_size):
            return None

        if self.grid.grid[goal_row, goal_col] >= 100:
            # Goal is occupied — try nearest free cell
            goal_row, goal_col = self._find_nearest_free(goal_row, goal_col)
            if goal_row is None:
                return None

        # A* search
        open_set: List[Tuple[float, int, int]] = []
        heapq.heappush(open_set, (0.0, start_row, start_col))

        came_from: dict = {}
        g_score = {(start_row, start_col): 0.0}
        f_score = {(start_row, start_col): self._heuristic(start_row, start_col, goal_row, goal_col)}

        closed_set: Set[Tuple[int, int]] = set()

        while open_set:
            _, current_row, current_col = heapq.heappop(open_set)
            current = (current_row, current_col)

            if current in closed_set:
                continue
            closed_set.add(current)

            if current == (goal_row, goal_col):
                path = self._reconstruct_path(came_from, current)
                path_world = [self.grid._grid_to_world(r, c) for r, c in path]
                self._last_path = path_world
                return path_world

            for nr, nc, step_cost in self.grid.get_neighbors(current_row, current_col):
                neighbor = (nr, nc)
                if neighbor in closed_set:
                    continue

                cell_cost = self.grid.cell_cost(nr, nc)
                if cell_cost == float('inf'):
                    continue

                tentative_g = g_score.get(current, float('inf')) + step_cost * cell_cost

                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self._heuristic(nr, nc, goal_row, goal_col)
                    f_score[neighbor] = f
                    heapq.heappush(open_set, (f, nr, nc))

        return None

    def _heuristic(self, r0: int, c0: int, r1: int, c1: int) -> float:
        """Euclidean heuristic scaled by grid resolution."""
        dx = c1 - c0
        dy = r1 - r0
        return math.hypot(dx, dy) * self.grid.resolution

    def _reconstruct_path(
        self,
        came_from: dict,
        current: Tuple[int, int],
    ) -> List[Tuple[int, int]]:
        """Reconstruct path from came_from map."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def _find_nearest_free(
        self,
        row: int,
        col: int,
        max_radius: int = 10,
    ) -> Tuple[Optional[int], Optional[int]]:
        """Search outward from (row, col) for the nearest free cell."""
        for radius in range(1, max_radius + 1):
            for dr in range(-radius, radius + 1):
                for dc in range(-radius, radius + 1):
                    if abs(dr) != radius and abs(dc) != radius:
                        continue
                    r, c = row + dr, col + dc
                    if 0 <= r < self.grid.grid_size and 0 <= c < self.grid.grid_size:
                        if self.grid.grid[r, c] < 100:
                            return r, c
        return None, None

    def smooth_path(
        self,
        path: List[Tuple[float, float]],
        tolerance: float = 0.05,
    ) -> List[Tuple[float, float]]:
        """
        Smooth a path using a simple line-of-sight shortcut algorithm.
        """
        if len(path) < 3:
            return path

        smoothed = [path[0]]
        i = 0
        while i < len(path) - 1:
            j = len(path) - 1
            while j > i + 1:
                if self._line_of_sight(path[i], path[j]):
                    break
                j -= 1
            smoothed.append(path[j])
            i = j

        return smoothed

    def _line_of_sight(
        self,
        p0: Tuple[float, float],
        p1: Tuple[float, float],
    ) -> bool:
        """Check if a straight line between two world points is obstacle-free."""
        r0, c0 = self.grid._world_to_grid(p0[0], p0[1])
        r1, c1 = self.grid._world_to_grid(p1[0], p1[1])
        for r, c in self.grid._bresenham(c0, r0, c1, r1):
            if not (0 <= r < self.grid.grid_size and 0 <= c < self.grid.grid_size):
                return False
            if self.grid.grid[r, c] >= 100:
                return False
        return True
