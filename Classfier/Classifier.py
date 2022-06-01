import matplotlib.pyplot as plt
import numpy as np
import wave
from random import sample
import pandas as pd
from scipy import fftpack
from scipy.signal import butter, filtfilt
from statsmodels.graphics.tsaplots import plot_acf
import plotly.graph_objects as go 
import os
from difflib import SequenceMatcher

def butter_lowpass_filter(data, cutoff, fs, order):
    nyq = 0.3*fs
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y
    
def fft(path, cutoff = 5, plot = False):
    t = 5
    path = str(path)
    spf = wave.open(path, "r")
    signal = spf.readframes(-1)
    signal = np.frombuffer(signal, np.int16)
    fs = spf.getframerate()
    Time = np.linspace(0, len(signal) / fs, num=len(signal))
    sig = signal 
    cutoff = cutoff
    order = 2
    y = butter_lowpass_filter(signal, cutoff, fs, order)

    if plot == True:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
                    y = signal,
                    line =  dict(shape =  'spline' ),
                    name = 'signal with noise'
                    ))
        fig.add_trace(go.Scatter(
                    y = y,
                    line =  dict(shape =  'spline' ),
                    name = 'filtered signal'
                    ))

        fig.show()
    return y, Time 
    
def predict_wave(path,down_sample_rate = 80, window_size = 0.5, threshold_events = 12, difference = 1.3, plot = False, cutoff = 5):
    t = 5
    path = str(path)
    spf = wave.open(path, "r")
    signal = spf.readframes(-1)
    signal = np.frombuffer(signal, np.int16)
    fs = spf.getframerate()
    time = np.linspace(0, len(signal) / fs, num=len(signal))
    sig = signal 
    cutoff = cutoff
    order = 2
    data  = butter_lowpass_filter(signal, cutoff, fs, order)

    if plot == True:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
                    y = signal,
                    line =  dict(shape =  'spline' ),
                    name = 'signal with noise'
                    ))
        fig.add_trace(go.Scatter(
                    y = data,
                    line =  dict(shape =  'spline' ),
                    name = 'filtered signal'
                    ))

        fig.show()
    # 1. Down Sampling
    ind = np.arange(0, np.where(np.round(time,4) == round(time[len(time) - 1] - window_size, 4))[0][0], down_sample_rate)
    t_stat = [0]*len(ind)
    # 2. Calculating SD
    for i in range(len(ind)):
        data_subset = data[ind[i] : ind[i] + int(window_size * down_sample_rate)]
        t_stat[i] = np.std(data_subset)
    # 3. Use threshold to determine movement intervals
    predicted_event = [x for x in range(len(t_stat)) if t_stat[x] > threshold_events]
    # time vector for middle of each window 
    time_middle = []
    for i in predicted_event:
        time_middle.append(time[ind[i]] + window_size/2)
    # 4. Estimation 
    intervals = [] 
    cut_point = predicted_event[0]
    last_interval = 0
    middle_time = int(down_sample_rate * window_size/2)
    for i in range(len(predicted_event) - 1):
        if predicted_event[i+1] != predicted_event[i] + 1:
            # combine intervals together if the predicted intervals are with difference amount
            if last_interval == 0:
                intervals.append([int(ind[cut_point] + middle_time)/10000, int(ind[predicted_event[i]] + middle_time)/10000])
                last_interval = intervals[-1]
            else:
                if ((int(ind[cut_point] + middle_time)/10000) - last_interval[1]) < difference:
                    last_interval[1] = int(ind[predicted_event[i]] + middle_time)/10000
                else:
                    intervals.append([int(ind[cut_point] + middle_time)/10000, int(ind[predicted_event[i]] + middle_time)/10000])
                last_interval = intervals[-1]
            
            cut_point = predicted_event[i+1]             
    for i in range(len(intervals)):
        if intervals[i][1] - intervals[i][0] < 1:
            print("Turn")
        elif intervals[i][1] - intervals[i][0] >= 1:
            print("Tension")
    
  
