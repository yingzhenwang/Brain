import Classifier as c
import numpy as np
import wave 


spf = wave.open("/Users/martinhuang/Desktop/OneDrive/2022/2022 Sem 1/DATA3888/Brain 5/Brain/Spiker_box_Louis/Short/LLL_L1.wav", "r")

signal = spf.readframes(-1)
signal = np.frombuffer(signal, np.int16)
fs = spf.getframerate()

time = np.linspace(0, len(signal) / fs, num=len(signal))

intervals = c.movement_classifier(signal, time = time)
print(intervals)

