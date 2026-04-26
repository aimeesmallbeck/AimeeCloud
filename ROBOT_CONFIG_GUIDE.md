# Multi-Robot Configuration Management

This repo supports multiple physical robots (Ron, Minnie, etc.) from a single codebase. This guide explains how to keep robot-specific settings from colliding in git.

---

## Philosophy

- **Shared code, private configs.** The navigation algorithms, controller logic, and launch files are shared. Each robot's physical calibration (wheel track, encoder ticks, serial ports) lives in an **untracked** YAML file.
- **Hostname = identity.** Each UNO Q board sets its own hostname (`ron`, `minnie`, etc.). The launch system auto-discovers the right config from the hostname.
- **Examples in git, active configs out.** We commit `*.example.yaml` templates so new robots have a starting point. The actual `ron.yaml` and `minnie.yaml` are `.gitignored`.

---

## Directory Layout

```
src/aimee_bringup/config/robots/
├── default.yaml              # Tracked template + documentation
├── ron.example.yaml          # Tracked template (Ron's settings)
├── minnie.example.yaml       # Tracked template (Minnie's settings)
├── ron.yaml                  # UNTRACKED — Ron's active config
├── minnie.yaml               # UNTRACKED — Minnie's active config
└── Ron.yaml -> ron.yaml      # Symlink for case-sensitive hostname match
```

---

## First-Time Setup (per robot)

### 1. Set the hostname

```bash
sudo hostnamectl set-hostname ron   # or minnie, wren, etc.
```

Reboot so the hostname sticks:

```bash
sudo reboot
```

### 2. Create the robot config from the example

```bash
cd ~/aimee-robot-ws
cp src/aimee_bringup/config/robots/ron.example.yaml \
   src/aimee_bringup/config/robots/ron.yaml
```

Edit `ron.yaml` with that robot's specific values:
- `serial_port` (`/dev/ttyACM0` vs `/dev/ttyUSB0`)
- `wheel_separation`
- `ticks_per_meter` (calibrated for THIS robot)
- `track_width_multiplier`
- `base_interface` (`ros` or `direct`)
- Which hardware is attached (`arm`, `camera`, `lidar`)

### 3. Verify auto-discovery

```bash
ros2 launch aimee_bringup robot.launch.py
```

You should see a log line like:

```
Aimee robot bringup — config: .../robots/ron.yaml | robot: ron | base: ugv02 ...
```

---

## What Goes Where

| Setting | Where | Why |
|---------|-------|-----|
| `wheel_separation`, `wheel_radius` | `robots/<name>.yaml` → `base_params` | Physical geometry differs per robot |
| `ticks_per_meter` | `robots/<name>.yaml` → `base_params` | Calibrated per robot |
| `track_width_multiplier` | `robots/<name>.yaml` → `base_params` | Skid-steer scrub compensation per robot |
| `base_interface` (`ros`/`direct`) | `robots/<name>.yaml` → `base_params` | Ron uses ROS mode; future robots may use direct |
| `serial_port`, `baud_rate` | `robots/<name>.yaml` → `base_params` | Port wiring differs per robot |
| `max_speed` (hardware limit) | `robots/<name>.yaml` → `base_params` | Motor/controller ceiling |
| `max_speed` (navigation limit) | `aimee_nav_params.yaml` | How fast AimeeNav is allowed to command |
| `max_angular` (navigation limit) | `aimee_nav_params.yaml` | How fast AimeeNav turns |
| `scan_match_pos_variance` | `aimee_nav_params.yaml` | Tuning per environment, not per robot |
| `nav_rate_hz`, `lidar_downsample` | `aimee_nav_params.yaml` | CPU performance tuning |

---

## Git Workflow

### On each robot

```bash
# Pull latest shared code
git pull origin main

# Your local ron.yaml is untracked — it will NEVER be overwritten by git pull.
# It will also never be committed accidentally.
```

### When setting up a new robot

```bash
# On your development machine
cp src/aimee_bringup/config/robots/default.yaml \
   src/aimee_bringup/config/robots/newbot.example.yaml
# Edit the example with sensible defaults for the new hardware
git add src/aimee_bringup/config/robots/newbot.example.yaml
git commit -m "Add newbot.example.yaml config template"
```

### What NOT to commit

```bash
# These are .gitignored — never `git add -f` them
git status
# Should NOT show:
#   src/aimee_bringup/config/robots/ron.yaml
#   src/aimee_bringup/config/robots/minnie.yaml
```

---

## Common Pitfalls

### "I edited aimee_nav_params.yaml and now the other robot acts weird"

**Rule:** `aimee_nav_params.yaml` holds **generic defaults** and environment tuning. Robot-specific calibrations belong in `robots/<name>.yaml` under `base_params`.

If you find yourself thinking "this value is only correct for Ron," move it to `ron.yaml` and forward it via `robot.launch.py`.

### "I ran `aimee_nav.launch.py` directly and it used the wrong ticks_per_meter"

The standalone `aimee_nav.launch.py` only loads `aimee_nav_params.yaml` — it has no knowledge of per-robot configs. **Always launch through `robot.launch.py`** for physical robots:

```bash
ros2 launch aimee_bringup robot.launch.py
```

If you must run AimeeNav standalone, pass the overrides explicitly:

```bash
ros2 launch aimee_nav aimee_nav.launch.py params_file:=/path/to/ron_nav_params.yaml
```

### "Git shows minnie.yaml as modified after I pulled Ron's changes"

This happens when robot configs are tracked in git. If you see this, the repo hasn't been migrated to the untracked config pattern yet. Run:

```bash
git rm --cached src/aimee_bringup/config/robots/ron.yaml
git rm --cached src/aimee_bringup/config/robots/minnie.yaml
git commit -m "untrack robot-specific configs"
```

Both robots then keep their local files without git interfering.

---

## Environment Variable Overrides

For one-off testing without editing YAML:

```bash
# Force a specific config
ROBOT_CONFIG=/workspace/src/aimee_bringup/config/robots/ron.yaml \
  ros2 launch aimee_bringup robot.launch.py

# Override a specific param
ros2 launch aimee_bringup robot.launch.py use_voice:=false use_llm:=false
```

---

## Adding a New Parameter Forward

When a new robot-specific param needs to reach AimeeNav:

1. Add it to `aimee_nav_node.py` parameter declarations.
2. Add it to `aimee_nav_params.yaml` with a safe generic default.
3. Add it to `robot.launch.py` under the `aimee_nav_node` parameters dict.
4. Add it to each robot's `*.example.yaml` with that robot's value.
5. **Do NOT** add it to `aimee_nav_params.yaml` with a calibrated value.
