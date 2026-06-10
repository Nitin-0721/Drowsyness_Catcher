import numpy as np
from scipy.io.wavfile import write

sample_rate = 44100
duration = 1.0
frequency = 1000.0
t = np.linspace(0, duration, int(sample_rate * duration))
wave = (np.sin(2 * np.pi * frequency * t) * 32767).astype(np.int16)
write('alerts/alarm.wav', sample_rate, wave)
print('alarm.wav created!')