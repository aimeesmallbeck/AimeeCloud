# AimeeNav Audit Report — Ron (UGV02) Integration
**Date:** 2026-04-25  
**Context:** Post turn-fix audit (controller now uses T=1 wheel_speed mode, max_speed=1.0, max_angular=1.0, accel limiting enabled)

---

## CRITICAL ISSUES — Fix before SLAM/Nav testing on Ron

### 1. Duplicate `/odom` Publishers
**Severity: HIGH**
- Both `ugv02_controller_node` and `aimee_nav_node` publish `/odom` on the same topic
- In ROS mode, AimeeNav skips `odom→base_link` TF (good), but still publishes `/odom` messages
- Interleaved messages from raw encoder odometry + EKF-fused odometry confuse downstream nodes
- **Fix:** Disable `/odom` publishing in AimeeNav when `base_interface: "ros"` (controller owns odometry)

### 2. Hardcoded Reactive/Recovery Speeds Ignore max_speed/max_angular
**Severity: HIGH**
- Recovery spin: `angular_z = 0.5` rad/s (ignores `max_angular`)
- Recovery backup: `linear_x = -0.15` m/s (ignores `max_speed`)
- Reactive panic turn: `angular_z = ±0.5` rad/s (ignores `max_angular`)
- Reactive caution turn: `angular_z = ±0.5` rad/s
- Exploration random bias: `angular_z = random.choice([-0.3, 0.3])`
- For Ron, 0.5 rad/s ≈ 130°/s — above our calibrated "appropriate max" of 90°/s
- **Fix:** Replace hardcoded constants with `self._max_speed` / `self._max_angular` references

### 3. Global Map Fixed at 10 m × 10 m
**Severity: HIGH**
- Global grid origin fixed at (-5, -5); does NOT scroll or expand
- Once Ron drives beyond ±5 m, mapping stops (`update_from_scan` returns early)
- **Fix:** Increase `global_map_size_m` to 50–100 m, or implement scrolling map

### 4. EKF Covariance Propagation Bug
**Severity: HIGH**
- `ekf_2d.cpp` predict uses `P = F*P + Q` instead of `P = F*P*F^T + Q`
- Not valid Kalman filter algebra; covariance loses symmetry/positive-definiteness
- **Fix:** Implement full `F*P*F^T + Q` propagation (or at least symmetric approximation)

### 5. scan_match_pos_std / scan_match_yaw_std Naming Ambiguity
**Severity: HIGH**
- Parameter names end in `_std` (standard deviation)
- YAML comment says "VARIANCE (sigma²)"
- C++ EKF treats them directly as variance
- If they ARE std devs (5 cm, 3°), the EKF is wrong (should square them)
- If they ARE variances (σ ≈ 22 cm, σ ≈ 10°), scan matcher is trusted less than intended
- **Fix:** Rename to `_variance` or `_std` and make code match semantics consistently

---

## MEDIUM ISSUES

### 6. Local Grid Too Coarse for Navigation
- `grid_size_m: 3.0` with `grid_resolution_m: 0.15` = 21×21 cells
- With `safety_distance_m: 0.35` + `obstacle_inflation_m: 0.15`, only 1–2 cells lookahead
- Doorway (~0.8 m) = ~5 cells; may be blocked by inflation
- **Fix:** `grid_size_m: 5.0`, `grid_resolution_m: 0.05` (100×100 cells)

### 7. Hardcoded Scan-Match Thresholds
- `search_radius_m = 0.5`, `search_angle_rad = 0.2`, `score_threshold = 10.0`
- Not exposed in YAML; wastes CPU on UNO Q
- **Fix:** Expose in `aimee_nav_params.yaml`

### 8. Process Noise Q Not Scaled by dt
- `Q` added directly regardless of `nav_rate_hz`
- If rate changes from 5→10 Hz, noise per second doubles
- **Fix:** Multiply `Q` by `dt` in `predict()`

### 9. Missing Parameter Forwarding to AimeeNav
- `robot.launch.py` does not forward `max_speed`, `max_angular`, `angular_scale`, `control_mode`, `accel_limit_*`, `track_width_multiplier`, `ticks_per_meter` to `aimee_nav_node`
- AimeeNav uses hardcoded YAML defaults instead of robot config
- Currently OK because AimeeNav YAML has sensible defaults (0.3 m/s, 0.3 rad/s)
- **Fix:** Forward all relevant params, or document that YAML values are authoritative

### 10. ugv02_bringup.launch.py Missing control_mode
- Does not pass `control_mode` → node defaults to `'velocity'` (T=13)
- Also hardcodes `wheel_separation: 0.23` (wrong for Ron/Minnie 0.172)
- **Fix:** Add `control_mode` parameter and accept `wheel_separation` as launch arg

---

## LOW / INFO

### 11. WaveRoverDriver angular_scale Never Applied
- Stores `self._angular_scale` but formula `diff = angular_z / max_angular` never uses it
- Stale comment says it's applied
- **Fix:** Remove unused parameter or apply it

### 12. DWA Is Dead Code
- Instantiated but `compute_velocity()` never called
- `_latest_local_plan` always empty
- Not a bug, just wasted initialization

### 13. RobotCentricGridMap Decay Ignores decay_time_s
- `decay()` is no-op; decay rate tied to scan frequency
- **Fix:** Use wall-clock time

### 14. base_link→base_laser TF Hardcodes z=0.18
- May not match actual mechanical mount
- **Fix:** Parameterize lidar x/y/z offset

---

## Consistency with Today's Controller Changes

| Parameter | Controller (Ron.yaml) | AimeeNav (YAML) | Status |
|-----------|----------------------|-----------------|--------|
| max_speed | 1.0 (hardware max) | 0.3 (nav limit) | ✅ Intentional separation |
| max_angular | 1.0 (hardware max) | 0.3 (nav limit) | ✅ Intentional separation |
| angular_scale | 1.0 | 1.0 | ✅ Consistent |
| control_mode | wheel_speed | wheel_speed | ✅ Consistent |
| accel_limit_linear | 0.3 | — (uses direct-mode driver) | ⚠️ AimeeNav has no accel limiting in ROS mode |
| accel_limit_angular | 0.5 | — | ⚠️ Same |
| ticks_per_meter | 106.0 | 106.0 | ✅ Consistent |
| track_width_multiplier | 2.0 | 2.0 | ✅ Consistent |
| wheel_separation | 0.172 | 0.172 | ✅ Consistent |

**Note:** AimeeNav does NOT apply velocity ramping when `base_interface: "ros"`. The controller now handles accel limiting, so this is fine as long as AimeeNav's commanded velocities are within the controller's ramp limits.

---

## Untested on Ron (Only Tested on Minnie)
- SLAM initialization and mapping
- Goal-directed navigation (planned mode)
- Reactive obstacle avoidance with real lidar
- Recovery behaviors (spin/backup)
- Exploration mode
- Loop closure
- Map persistence (`~/aimee_maps`)

## Recommended Pre-Test Checklist
1. [ ] Fix duplicate `/odom` publishers
2. [ ] Replace hardcoded 0.5 rad/s / -0.15 m/s with param references
3. [ ] Increase global_map_size_m to at least 50 m
4. [ ] Verify scan_match_pos_std/yaw_std semantics (variance vs std)
5. [ ] Test SLAM init in small room first
6. [ ] Test reactive mode (no goal, just obstacle avoidance)
7. [ ] Test planned navigation to a nearby goal
