try:
    from aimee_nav._core import GridMap, ScanMatcher, EKF2D, PoseGraph, Keyframe, Constraint, GlobalPlanner, DWALocalPlanner, DWAConfig
except ImportError as e:
    import warnings
    warnings.warn(f"C++ extension not available: {e}")
    GridMap = None
