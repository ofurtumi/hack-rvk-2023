import sounddevice as sd
import numpy as np

# Generate a 440 Hz sine wave for 1 second
sr = 44100
t = np.linspace(0, 1, sr, False)
x = 0.5 * np.sin(2 * np.pi * 440 * t)

# Play the audio signal
sd.play(x, sr)

