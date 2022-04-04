import matplotlib.pyplot as plt
import numpy as np
import wave
import sys


spf = wave.open("Spiker_box_Louis/Short/LLL_L1.wav", "r")

signal = spf.readframes(-1)
signal = np.fromstring(signal, np.int16)
fs = spf.getframerate()

Time = np.linspace(0, len(signal) / fs, num=len(signal))

plt.figure(1)
plt.title("Signal Wave...")
plt.plot(Time, signal)
plt.show()



