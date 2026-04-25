#!/usr/bin/env python3
"""Quick validation of DWA + local costmap extraction."""
import math
from aimee_nav._core import GridMap, DWALocalPlanner, DWAConfig, GlobalPlanner

# Build a simple global map with a corridor
gmap = GridMap(10.0, 10.0, 0.05, 0.15)
gmap.set_origin(-5.0, -5.0)
ranges = []
for i in range(360):
    a = math.radians(i)
    # Corridor: walls at y = +/- 1.0
    if abs(math.sin(a)) > 0.1:
        r = abs(1.0 / math.sin(a))
    else:
        r = 10.0
    ranges.append(min(r, 5.0))

gmap.update_from_scan(0.0, 0.0, 0.0, ranges, 0.0, 2.0*math.pi/360.0, 0.01, 12.0)
gmap.inflate_obstacles()

# Extract local costmap
local = gmap.extract_local_grid_map(0.0, 0.0, 3.0, 3.0)
print(f"Local map: {local.width_cells()}x{local.height_cells()}")

# Plan a global path through the corridor
planner = GlobalPlanner()
path = planner.plan(gmap, -2.0, 0.0, 2.0, 0.0)
print(f"Global path length: {len(path)}")

# Run DWA
cfg = DWAConfig()
cfg.max_vel_x = 0.5
cfg.vx_samples = 10
cfg.vtheta_samples = 10

dwa = DWALocalPlanner(cfg)
v, w, traj_x, traj_y = dwa.compute_velocity(
    local, 0.0, 0.0, 0.0, 0.0, 0.0,
    path, 2.0, 0.0
)
print(f"DWA command: v={v:.3f}, w={w:.3f}")
assert abs(v) > 0.01, "DWA should produce forward velocity in clear corridor"
print("DWA integration: PASS")
