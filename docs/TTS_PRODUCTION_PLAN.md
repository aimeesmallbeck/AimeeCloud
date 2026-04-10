# TTS Production Plan

## Current Implementation (Development)

### Default: gTTS (Google Text-to-Speech)
- **Pros**: High quality, natural sounding, multiple languages
- **Cons**: Requires internet, latency ~1-3s, privacy concerns
- **Use case**: Development, testing, when internet available

## Production Target: Local TTS

### Option 1: Piper (Recommended)
- **Pros**: Neural quality, fast (~real-time), offline, low resource
- **Cons**: Requires model download (~50-100MB per voice)
- **Best for**: Production robots, privacy-critical applications

### Option 2: pyttsx3 (Fallback)
- **Pros**: No models needed, works immediately, offline
- **Cons**: Robotic quality, limited voices
- **Best for**: Fallback when Piper fails, quick testing

### Option 3: Coqui TTS (Future)
- **Pros**: High quality neural, voice cloning
- **Cons**: Larger models (~1GB), slower on 4GB RAM
- **Best for**: High-quality production with sufficient resources

## Implementation Strategy

### Phase 1: Current (Development)
```yaml
tts:
  primary: gtts
  fallback: none
```

### Phase 2: Hybrid (Pre-Production)
```yaml
tts:
  primary: gtts
  fallback: piper
  fallback_on_error: true
  fallback_offline: true  # Auto-fallback when no internet
```

### Phase 3: Production
```yaml
tts:
  primary: piper
  fallback: pyttsx3
  gtts_enabled: false  # Disable cloud TTS
```

## Piper Model Recommendations

### For English (AIMEE)
| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| en_US-lessac-medium | 63MB | Fast | Good |
| en_US-ryan-medium | 63MB | Fast | Good |
| en_US-libritts-high | 110MB | Medium | Better |
| en_US-amy-medium | 63MB | Fast | Good (female) |

### Download Script
```bash
#!/bin/bash
# download_piper_models.sh

MODEL_DIR="$HOME/.local/share/piper-tts"
mkdir -p "$MODEL_DIR"

cd "$MODEL_DIR"

# Download en_US-lessac-medium
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json

echo "Models downloaded to $MODEL_DIR"
```

## Configuration Examples

### Development (Current)
```yaml
tts:
  engine: gtts
  gtts:
    lang: en
    slow: false
    tld: com
```

### Pre-Production (Hybrid)
```yaml
tts:
  engine: auto  # Try gtts, fallback to piper
  auto_fallback: true
  gtts:
    lang: en
  piper:
    model_path: ~/.local/share/piper-tts/en_US-lessac-medium.onnx
    speaker_id: 0
  pyttsx3:
    voice: default
    rate: 150
```

### Production (Local Only)
```yaml
tts:
  engine: piper
  piper:
    model_path: ~/.local/share/piper-tts/en_US-lessac-medium.onnx
    use_cuda: false  # CPU only for Pi 5
  fallback_engine: pyttsx3
```

## Performance Comparison (Raspberry Pi 5, 4GB)

| Engine | First Audio Latency | RAM Usage | Quality | Offline |
|--------|-------------------|-----------|---------|---------|
| gTTS | 1-3s | Low | High | No |
| Piper | 0.1-0.3s | ~100MB | High | Yes |
| pyttsx3 | 0.05s | ~20MB | Low | Yes |
| Coqui TTS | 2-5s | ~1GB | Very High | Yes |

## Migration Path

1. **Now**: Implement gTTS + Piper hybrid
2. **Testing Phase**: Test Piper extensively, compare quality
3. **Pre-Production**: Set hybrid mode, monitor fallback rate
4. **Production**: Switch to Piper primary, disable gTTS

## Offline Detection

The TTS brick will auto-detect offline mode:
```python
def is_online():
    try:
        urllib.request.urlopen('https://www.google.com', timeout=3)
        return True
    except:
        return False

# Auto-switch to local TTS when offline
if not is_online() and config.auto_fallback:
    use_local_tts()
```

## Notes

- Piper models are ONNX format, run efficiently on CPU
- First load has slight delay (~1s), subsequent are fast
- Consider model preloading at startup for lowest latency
- pyttsx3 is always available as emergency fallback
