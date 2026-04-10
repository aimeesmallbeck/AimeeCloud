# Voice transcription message
# Published by: Voice Manager (ASR)
# Subscribed by: Intent Router

string text               # Transcribed text
float32 confidence        # ASR confidence (0.0-1.0)
string source             # vosk | whisper | cloud
bool is_command           # True if this is a command (post-wake-word)
bool is_partial           # True if this is a partial result (streaming)

# Wake word info
bool wake_word_detected   # True if preceded by wake word
string wake_word          # Which wake word was detected

# Metadata
builtin_interfaces/Time timestamp
string session_id
string correlation_id
