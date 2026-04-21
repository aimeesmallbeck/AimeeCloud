# AIMEE Robot Hardware Specification

## Host Computer: Arduino UNO Q

The AIMEE robot runs on the **Arduino UNO Q**, a single-board computer optimized for Arduino applications.

### Specifications

| Component | Specification |
|-----------|---------------|
| **Board** | Arduino UNO Q |
| **SoC** | ARM AARCH64 (64-bit ARM architecture) |
| **RAM** | 4GB LPDDR4 |
| **Storage** | microSD card (recommended: 64GB+ Class 10) |
| **Operating System** | Linux (Ubuntu/Debian-based) |
| **ROS2 Version** | ROS2 Humble Hawksbill |

### Why Arduino UNO Q?

- **Native Arduino Compatibility**: Designed for Arduino ecosystem integration
- **AARCH64 Architecture**: Supports modern Edge Impulse models and ML inference
- **4GB RAM**: Sufficient for ROS2 + local LLM (with optimizations)
- **I/O Interfaces**: GPIO, I2C, SPI for hardware integration
- **Network**: Wi-Fi and Ethernet for connectivity

### Architecture Notes

```
┌─────────────────────────────────────┐
│         Arduino UNO Q               │
│  ┌─────────────────────────────┐    │
│  │  4GB RAM                    │    │
│  │  AARCH64 SoC                │    │
│  │                             │    │
│  │  ┌─────────────────────┐    │    │
│  │  │  AIMEE Robot Stack  │    │    │
│  │  │  - ROS2 Humble      │    │    │
│  │  │  - Fast DDS SHM     │    │    │
│  │  │  - Edge Impulse     │    │    │
│  │  │  - llama.cpp        │    │    │
│  │  └─────────────────────┘    │    │
│  └─────────────────────────────┘    │
│                                     │
│  I/O: GPIO | I2C | SPI | USB | Eth  │
└─────────────────────────────────────┘
           │
     ┌─────┴─────┐
     │           │
  ┌──▼──┐     ┌──▼──┐
  │ UGV │     │ Arm │
  └─────┘     └─────┘
```

### Peripherals

#### Ron (Robot 1)
- **Base**: UGV02 tracked mobile robot
- **Arm**: RoArm-M3-Pro 5-DOF manipulator + gripper (6 DOF total)
  - Connection: WiFi HTTP API at `192.168.1.57`
  - Driver: `aimee_lerobot_bridge/roarm_m3_http_driver.py`
  - Verified joint limits (empirical, firmware-native coordinates):
    | Joint | Range | Home | Note |
    |-------|-------|------|------|
    | Base (joint1) | -180° to +180° | 0° | Full rotation |
    | Shoulder (joint2) | -90° to +90° | 0° | SDK claims ±109°, actual ±90° |
    | Elbow (joint3) | **0° to 170°** | **90°** | 180° hits base |
    | Wrist (joint4) | -90° to +90° | 0° | SDK claims ±109°, actual ±90° |
    | Roll (joint5) | -180° to +180° | 0° | Full rotation |
    | Gripper | 0° to 180° | 0° | Effective ~64°–178° |
- **Camera**: OBSBOT Tiny 2 (USB, with RNDIS at 192.168.5.1)

#### Wren (Robot 2)
- **Base**: Wave Rover 4WD
- **Camera**: OBSBOT Tiny 2 (USB)

### Resource Constraints & Optimizations

Given the 4GB RAM constraint, the following optimizations are implemented:

1. **Fast DDS Shared Memory**: Eliminates message duplication for local nodes
2. **Small LLM Models**: 135M-500M parameter models instead of 7B+
3. **Quantized Models**: Q4_K_M quantization for reduced memory
4. **Efficient STT**: Vosk small models (40MB) instead of Whisper
5. **Streaming Architecture**: Prevents blocking and memory buildup

### Development vs Production

| Aspect | Development | Production |
|--------|-------------|------------|
| **LLM** | Cloud APIs or local | Local only (Piper, small LLM) |
| **TTS** | gTTS (cloud) | Piper (local) |
| **STT** | Vosk or Whisper | Vosk (offline) |
| **Internet** | Required for dev | Optional (offline capable) |

### References

- [Arduino UNO Q Documentation](https://docs.arduino.cc/)
- [Edge Impulse AARCH64 Deployment](https://docs.edgeimpulse.com/docs/deployment/running-your-model-locally/running-your-model-on-linux-aarch64)
- [ROS2 Humble on ARM](https://docs.ros.org/en/humble/Installation/Alternatives/Ubuntu-Install-Binarys.html)

## Notes for Developers

When working with the Arduino UNO Q:

1. **Architecture**: All binaries must be AARCH64 compatible
2. **Edge Impulse Models**: Use `linux-aarch64` target when deploying
3. **ROS2 Packages**: Build from source if binary packages unavailable
4. **Memory**: Monitor RAM usage with `htop` - 4GB fills quickly with large models
5. **Storage**: Use high-quality SD card; consider USB SSD for better I/O
