#!/usr/bin/env python3
import math
import numpy as np

from aimee_nav._core import GridMap, ScanMatcher, EKF2D, GlobalPlanner, RobotCentricGridMap

def test_robot_centric_grid():
    grid = RobotCentricGridMap(3.0, 0.15, 0.15)
    ranges = [1.0] * 360
    angles = [float(i) for i in range(360)]
    grid.update_from_scan(ranges, angles, 0.0, 0.0, 0.0, 8.0)
    arr = grid.grid_array()
    assert arr.shape == (21, 21), f"Expected (21,21), got {arr.shape}"
    assert arr[10, 10] < 100
    print("RobotCentricGridMap: PASS")

def test_global_grid_and_scan_matcher():
    gmap = GridMap(10.0, 10.0, 0.05, 0.15)
    gmap.set_origin(-5.0, -5.0)

    # Richer scan: box-like environment
    ranges = []
    for i in range(360):
        a = math.radians(i)
        # Box at +/- 1.5m in x and y
        if abs(math.cos(a)) > abs(math.sin(a)):
            r = 1.5 / abs(math.cos(a) + 1e-6)
        else:
            r = 1.5 / abs(math.sin(a) + 1e-6)
        ranges.append(min(r, 3.0))

    angle_min = 0.0
    angle_increment = 2.0 * math.pi / 360.0

    gmap.update_from_scan(0.0, 0.0, 0.0, ranges, angle_min, angle_increment, 0.01, 12.0)
    gmap.inflate_obstacles()

    sm = ScanMatcher(gmap)
    mx, my, mtheta, score = sm.match(ranges, angle_min, angle_increment, 0.01, 12.0, 0.0, 0.0, 0.0)
    assert score > 0, f"Match failed with score {score}"
    assert abs(mx) < 0.15, f"x error: {mx}"
    assert abs(my) < 0.15, f"y error: {my}"
    print(f"ScanMatcher: PASS (pose=({mx:.3f},{my:.3f},{mtheta:.3f}), score={score:.1f})")

def test_ekf():
    ekf = EKF2D()
    ekf.reset(0.0, 0.0, 0.0)
    ekf.predict(0.5, 0.0, 0.1)
    assert ekf.x() > 0.04, f"EKF x should increase, got {ekf.x()}"
    ekf.update_scan_pose(0.05, 0.0, 0.0, 0.01, 0.01)
    assert abs(ekf.x() - 0.05) < 0.02
    print("EKF2D: PASS")

def test_global_planner():
    gmap = GridMap(5.0, 5.0, 0.05, 0.15)
    gmap.set_origin(-2.5, -2.5)
    ranges = []
    for i in range(360):
        a = math.radians(i)
        ranges.append(2.0)
    gmap.update_from_scan(0.0, 0.0, 0.0, ranges, 0.0, 2.0*math.pi/360.0, 0.01, 12.0)
    gmap.inflate_obstacles()

    planner = GlobalPlanner()
    path = planner.plan(gmap, -1.0, 0.0, 1.0, 0.0)
    assert len(path) > 0, "Planner returned empty path"
    print(f"GlobalPlanner: PASS (path length={len(path)})")

if __name__ == '__main__':
    test_robot_centric_grid()
    test_global_grid_and_scan_matcher()
    test_ekf()
    test_global_planner()
    print("\nAll C++ component tests passed!")
