#!/usr/bin/env python3
import time
import math

from aimee_nav.local_grid_map import LocalGridMap
from aimee_nav.local_grid_map_cpp import LocalGridMapCpp

GRID_SIZE = 5.0
RES = 0.05
INFLATION = 0.15

ranges = []
angles_deg = []
for i in range(360):
    a = i
    if 80 <= i <= 100 or 170 <= i <= 190 or 260 <= i <= 280:
        r = 1.5
    else:
        r = 3.0 + math.sin(math.radians(i * 3)) * 0.5
    ranges.append(r)
    angles_deg.append(float(a))

robot_x, robot_y, robot_theta = 0.0, 0.0, 0.0

py_grid = LocalGridMap(size_m=GRID_SIZE, resolution_m=RES, inflation_m=INFLATION)
py_times = []
for _ in range(20):
    t0 = time.perf_counter()
    py_grid.update_from_scan(ranges, angles_deg, robot_x, robot_y, robot_theta, max_range_m=8.0)
    t1 = time.perf_counter()
    py_times.append((t1 - t0) * 1000.0)

cpp_grid = LocalGridMapCpp(size_m=GRID_SIZE, resolution_m=RES, inflation_m=INFLATION)
cpp_times = []
for _ in range(20):
    t0 = time.perf_counter()
    cpp_grid.update_from_scan(ranges, angles_deg, robot_x, robot_y, robot_theta, max_range_m=8.0)
    t1 = time.perf_counter()
    cpp_times.append((t1 - t0) * 1000.0)

py_avg = sum(py_times) / len(py_times)
cpp_avg = sum(cpp_times) / len(cpp_times)
py_max = max(py_times)
cpp_max = max(cpp_times)

print(f"Fine grid ({GRID_SIZE}m @ {RES}m)")
print(f"Python LocalGridMap:  avg={py_avg:.2f} ms  max={py_max:.2f} ms")
print(f"C++ LocalGridMapCpp:  avg={cpp_avg:.2f} ms  max={cpp_max:.2f} ms")
print(f"Speedup: {py_avg/cpp_avg:.1f}x")
