# Edge Impulse Model Creation Guide

This document outlines how to create and deploy custom Edge Impulse models for the AIMEE robot.

> **Note**: You can create custom Edge Impulse models as needed for different wake words, audio classifications, or other edge ML tasks.

## Overview

Edge Impulse provides a platform for training and deploying machine learning models on edge devices. AIMEE uses Edge Impulse models for:

- **Wake Word Detection**: Keyword spotting (e.g., "Aimee")
- **Audio Classification**: Sound/event recognition
- **Future**: Gesture recognition, anomaly detection

## Current Models

### Wake Word Model
- **Project**: Smallbeck-project-1
- **Location**: `/home/arduino/.arduino-bricks/models/custom-ei/ei-model-953002-1/model.eim`
- **Labels**: `aimee`, `noise`, `unknown`
- **Sample Rate**: 16kHz
- **Input Features**: 16,000 samples (1 second at 16kHz)

## Creating New Models

### Step 1: Collect Training Data

1. **Access Edge Impulse Studio**: https://studio.edgeimpulse.com
2. **Create New Project**: Choose "Keyword Spotting" or "Audio Classification"
3. **Collect Samples**:
   - Target keyword: 50-100+ samples per variation
   - Background noise: 50+ samples
   - Unknown words: 50+ samples
   - Recommended: 1-2 second clips at 16kHz

### Step 2: Data Collection Script

```python
#!/usr/bin/env python3
"""Record audio samples for Edge Impulse training."""
import subprocess
import os

def record_sample(output_dir, label, sample_num, duration=2):
    """Record a single sample."""
    filename = f"{label}.{sample_num:03d}.wav"
    filepath = os.path.join(output_dir, filename)
    
    print(f"Recording: {filename}")
    print("Get ready...")
    
    subprocess.run([
        "arecord", "-D", "default",
        "-f", "S16_LE",
        "-r", "16000",
        "-c", "1",
        "-d", str(duration),
        filepath
    ])
    
    print(f"Saved: {filepath}")

# Usage
output_dir = "training_data/aimee"
os.makedirs(output_dir, exist_ok=True)

for i in range(10):
    record_sample(output_dir, "aimee", i)
```

### Step 3: Upload to Edge Impulse

1. **Data Acquisition** → **Upload Data**
2. **Label** your samples appropriately
3. **Split** into training (80%) and test (20%) sets

### Step 4: Create Impulse

1. **Create Impulse**:
   - **Time Series Data**: Window size 1000ms, Window increase 100ms
   - **Processing Block**: Audio (MFE or Spectrogram)
   - **Learning Block**: Classification

2. **Generate Features**:
   - Choose processing parameters
   - Click "Generate features"

3. **Train Model**:
   - Neural network architecture: 1D CNN or Transfer Learning
   - Training cycles: 50-100
   - Learning rate: 0.001-0.005
   - Target accuracy: >90%

### Step 5: Deploy to AIMEE

1. **Deployment** → **Linux (AARCH64)**
2. **Build**: Select "Linux (AARCH64)" target
3. **Download**: `.eim` model file

### Step 6: Install on AIMEE

```bash
# Create model directory
mkdir -p ~/.arduino-bricks/models/custom-ei/<project-name>/

# Copy model
cp ~/Downloads/<model>.eim ~/.arduino-bricks/models/custom-ei/<project-name>/model.eim

# Update brick configuration (if needed)
# Edit: ~/aimee-robot-ws/src/aimee_wake_word_ei/config/brick_config.yaml
```

## Model Configuration

Update the brick configuration to use the new model:

```yaml
# config/brick_config.yaml
variables:
  - name: MODEL_PATH
    description: Path to Edge Impulse .eim model file
    default: "/home/arduino/.arduino-bricks/models/custom-ei/<your-project>/model.eim"
    type: string
    
  - name: TARGET_KEYWORD
    description: Keyword to detect
    default: "your_keyword"  # Must match label in model
    type: string

model:
  type: edge_impulse
  path: /home/arduino/.arduino-bricks/models/custom-ei/<your-project>/model.eim
  labels:
    - your_keyword
    - noise
    - unknown
  sample_rate: 16000
```

## Testing New Models

### Verify Model Info

```bash
# Get model metadata
~/.arduino-bricks/models/custom-ei/<project>/model.eim --print-info
```

### Test Detection

```python
#!/usr/bin/env python3
"""Test wake word detection with new model."""
import asyncio
from aimee_wake_word_ei.brick.wake_word_ei import WakeWordEIBrick

async def test():
    brick = WakeWordEIBrick(
        model_path="/home/arduino/.arduino-bricks/models/custom-ei/<project>/model.eim",
        target_keyword="your_keyword",
        confidence_threshold=0.70,
        debug=True
    )
    
    await brick.initialize()
    
    def on_detect(result):
        print(f"Detected: {result.keyword} ({result.confidence:.2f})")
    
    brick.on_wake_word(on_detect)
    await brick.start_listening()
    
    print("Listening... Press Ctrl+C to stop")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    
    await brick.shutdown()

if __name__ == "__main__":
    asyncio.run(test())
```

## Best Practices

### Data Collection
- Record in the actual environment (robot's location)
- Include various background noises
- Record at different distances from microphone
- Include different speakers (if multi-user)
- Balance positive and negative samples

### Model Training
- Start with 50+ samples per class
- Use data augmentation (noise, pitch shift)
- Monitor for overfitting
- Test on held-out data
- Optimize for latency vs accuracy

### Deployment
- Use consistent sample rates (16kHz recommended)
- Verify model is executable: `chmod +x model.eim`
- Test thoroughly before production
- Keep backups of working models

## Troubleshooting

### Model Won't Load
```bash
# Check file exists and is executable
ls -la ~/.arduino-bricks/models/custom-ei/<project>/model.eim

# Test model info
~/.arduino-bricks/models/custom-ei/<project>/model.eim --print-info
```

### Low Detection Accuracy
- Increase training samples
- Adjust confidence threshold
- Check audio input quality
- Verify model labels match target keyword

### High False Positive Rate
- Add more "unknown" and "noise" training samples
- Increase confidence threshold
- Adjust cooldown period
- Improve data quality

## Resources

- **Edge Impulse Docs**: https://docs.edgeimpulse.com
- **Keyword Spotting Guide**: https://docs.edgeimpulse.com/docs/tutorials/end-to-end-tutorials/responding-to-your-voice
- **AIMEE Model Location**: `~/.arduino-bricks/models/custom-ei/`

## Notes

- Models are architecture-specific (AARCH64 for Raspberry Pi 5)
- The `.eim` format is Edge Impulse's Linux executable format
- Models can be updated without rebuilding the ROS2 workspace
- Multiple models can coexist; switch via configuration
