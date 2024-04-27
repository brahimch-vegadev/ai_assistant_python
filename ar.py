from TTS.tts.utils.io import load_config
from TTS.tts.tts import TTS
import numpy as np
import sounddevice as sd

# Load configuration
config_path = "path/to/config.json"
config = load_config(config_path)

# Initialize TTS model
tts = TTS(config)

# Synthesize speech
text = "مرحبا، كيف حالك؟"
wav, alignment, mel = tts.synthesize(text)

# Convert audio from 32-bit float to 16-bit integer
wav = (np.clip(wav, -1, 1) * 32767).astype(np.int16)

# Play the synthesized speech
sd.play(wav, config["sample_rate"])
sd.wait()