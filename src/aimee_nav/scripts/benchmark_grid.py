#!/usr/bin/env python3
import time
import math
import numpy as np

# Old Python implementation
from aimee_nav.local_grid_map import LocalGridMap

# New C++-backed implementation
from aimee_nav.local_grid_map_cpp import LocalGridMapCpp

GRID_SIZE = 3.0
RES = 0.15
INFLATION = 0.15

# Simulate a 360-point LD19 scan
ranges = []
angles_deg = []
for i in range(360):
    a = i
    # Simulate a room with some walls
    if 80 <= i <= 100 or 170 <= i <= 190 or 260 <= i <= 280:
        r = 1.5
    else:
        r = 3.0 + math.sin(math.radians(i * 3)) * 0.5
    ranges.append(r)
    angles_deg.append(float(a))

robot_x, robot_y, robot_theta = 0.0, 0.0, 0.0

# Benchmark Python
py_grid = LocalGridMap(size_m=GRID_SIZE, resolution_m=RES, inflation_m=INFLATION)
py_times = []
for _ in range(50):
    t0 = time.perf_counter()
    py_grid.update_from_scan(ranges, angles_deg, robot_x, robot_y, robot_theta, max_range_m=8.0)
    t1 = time.perf_counter()
    py_times.append((t1 - t0) * 1000.0)

# Benchmark C++ backed
cpp_grid = LocalGridMapCpp(size_m=GRID_SIZE, resolution_m=RES, inflation_m=INFLATION)
cpp_times = []
for _ in range(50):
    t0 = time.perf_counter()
    cpp_grid.update_from_scan(ranges, angles_deg, robot_x, robot_y, robot_theta, max_range_m=8.0)
    t1 = time.perf_counter()
    cpp_times.append((t1 - t0) * 1000.0)

py_avg = sum(py_times) / len(py_times)
cpp_avg = sum(cpp_times) / len(cpp_times)
py_max = max(py_times)
cpp_max = max(cpp_times)

print(f"Python LocalGridMap:  avg={py_avg:.2f} ms  max={py_max:.2f} ms")
print(f"C++ LocalGridMapCpp:  avg={cpp_avg:.2f} ms  max={cpp_max:.2f} ms")
print(f"Speedup: {py_avg/cpp_avg:.1f}x")
