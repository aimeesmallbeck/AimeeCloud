# Aimee Robot - Session Checkpoint

**Date:** 2026-04-13  
**Session Focus:** Separate video capture from OBSBOT SDK control; fix monitor node CPU starvation

---

## 🎉 MISSION ACCOMPLISHED!

### What Was Done Today

1. **Separated Video Pipeline from OBSBOT SDK Node**
   - Stripped `obsbot_brick.py` to SDK-only (no OpenCV/UVC capture code)
   - Stripped `obsbot_node.py` of all video publishing (`/camera/image_raw`, cv_bridge, video timer)
   - `obsbot_node` is now a pure PTZ/tracking/status node

2. **Added Dedicated USB Camera Node**
   - `core.launch.py` now launches `usb_cam_node_exe` from `ros-humble-usb-cam`
   - Configured for `/dev/video2`, 1280×720, `mjpeg2rgb`, `mmap` I/O
   - Publishes to `/camera/image_raw` and `/camera/camera_info`
   - **Note:** `ros-humble-v4l2-camera` v0.6.2 was installed first but does not support MJPG format (crashes with `cv_bridge::Exception: Unrecognized image encoding []`)

3. **Performance Results**
   - `obsbot_node` CPU usage: **~88% → ~5%**
   - Video stream stable at **~23 fps** at 1280×720
   - Python GIL + MJPEG decode overhead completely eliminated from video pipeline

4. **Startup Script Updated**
   - `start_dashboard.sh` now uses Docker image `aimee-ros-dashboard:usb-cam`
   - `monitor_node` temporarily removed from automatic startup to avoid CPU starvation from `ros2 node list`/`ros2 topic list` subprocess loops

---

## 📊 Running Services

| Service | Container | Status | URL |
|---------|-----------|--------|-----|
| **ROS2 Core** | `aimee-robot` | 🟢 Running | — |
| **Monitor** | `aimee-robot` | 🟡 Paused | http://192.168.1.100:8081 (manual start) |

---

## 📁 Files Created/Modified

```
/home/arduino/
├── start_dashboard.sh              [UPDATED - usb-cam image, no auto monitor]
├── aimee-robot-ws/src/
│   ├── aimee_bringup/launch/core.launch.py
│   │   [UPDATED - removed video params from obsbot_node, added usb_cam_node]
│   ├── aimee_vision_obsbot/
│   │   ├── obsbot_node.py          [UPDATED - stripped video publishing]
│   │   └── brick/obsbot_brick.py   [UPDATED - stripped UVC/OpenCV capture]
│   └── aimee_ros2_monitor/
│       └── monitor_node.py         [PENDING - fix subprocess CPU starvation]
```

---

## 🔮 Next Steps (Future Sessions)

1. **Fix Monitor Node**
   - Replace `ros2 node list` subprocess with `get_node_names_and_namespaces()`
   - Replace `ros2 topic list -t` subprocess with `get_topic_names_and_types()`
   - Compute `/camera/image_raw` Hz from callback timestamps instead of `ros2 topic hz`
   - Add `usb_camera` to node definitions; remove obsolete `publish_video:=true` arg

2. **Dashboard Enhancements**
   - Add action goal widgets (test PickPlace from dashboard)
   - Add voice pipeline visualization

3. **Hardware Testing**
   - Connect UGV02 via serial and verify `/cmd_vel` response
   - Test OBSBOT PTZ commands through ROS2 topics

---

## 📝 Notes

- `usb_cam` package works well for MJPEG streams on the UNO Q; `v4l2_camera` does not.
- The `color_detector_node` and `object_tracker_node` are transparent to this change — they still subscribe to `/camera/image_raw`.
- Fast DDS SHM config is still disabled (`FASTRTPS_DEFAULT_PROFILES_FILE` set to disable SHM) to avoid `open_and_lock_file` errors.

**Status:** 🤖 **VIDEO PIPELINE SEPARATED AND OPERATIONAL!**
