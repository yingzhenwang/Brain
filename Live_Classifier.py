import serial
import wave
import numpy as np
import matplotlib.pyplot as plt
from drawnow import *
from scipy.signal import butter, filtfilt
from scipy import fftpack




plt.ion()   

b_rate = 230400
Fs = 10000

inputBufferSize = int(Fs)

ask_port = False
if ask_port == True:
    c_port = input('Which port?\n')
else:
    c_port = "/dev/tty.usbserial-DM02INQ2"


try:
    ser = serial.Serial(port=c_port, baudrate=b_rate)
    ser.timeout = inputBufferSize/Fs
except serial.serialutil.SerialException:
    raise Exception('Could not open port {c_port}.')


def makeFig():
    plt.plot(data_plot, 'g-')


def process_data(b_data):
    data_in = np.array(b_data)
    data_processed = np.zeros(0)

    i = 0
    while i < len(data_in) - 1:
        if data_in[i] > 127:
            int_processed = (np.bitwise_and(data_in[i], 127)) * 128 - 512
            i += 1
            int_processed += data_in[i]
            data_processed = np.append(data_processed, int_processed)
        i += 1

    return data_processed


def tt_new(seq):
    seq = seq.tolist()
    big = [x for x in seq if x>275]
    print(big)
    if len(big)>75:
        print("New_Tension")
    else:
        print("New_Turn")
    return 1


def prep_wave(waveSeq):
    spf = waveSeq
    signal = spf.readframes(-1)
    signal = np.frombuffer(signal, np.int16)
    fs = spf.getframerate()

    time = np.linspace(0, len(signal) / fs, num=len(signal))
    return signal, fs, time, spf 

nyq = 0.3*Fs
def butter_lowpass_filter(data, cutoff, fs, order):
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def event(sample_rate, waveSeq):
    threshold = 125
    interval = waveSeq
    if(max(interval) > threshold or min(interval) < -threshold):
        return True


def Arm_detection(intervals):#predict
    if intervals == False:
        print("Fake_Tension")
    else:
        for i in range(len(intervals)):
            if intervals[i][1] - intervals[i][0] < 1:
                print("Turn")
            elif intervals[i][1] - intervals[i][0] >= 1:
                print("Real_Tension")

def movement_classifier(data, time, down_sample_rate = 50, window_size = 0.3, threshold_events = 125, difference = 0.4):
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
    print("predicted_event")
    if len(predicted_event) == 1:
        print("Turn!!!!!!")
    print(predicted_event)
    if len(predicted_event) > 0:
        cut_point = predicted_event[0]
    last_interval = 0

    middle_time = int(down_sample_rate * window_size/2)
    if len(predicted_event) > 0:
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
                        
        return intervals
    else:
        return False

def fft(waveSeq, cutoff = 5, plot = False):
    t = 5
    spf = waveSeq
    signal = spf.readframes(-1)
    signal = np.frombuffer(signal, np.int16)
    Fs = 10000
    Time = np.linspace(0, len(signal) / Fs, num=len(signal))
    sig = signal 
    cutoff = cutoff
    order = 2
    y = butter_lowpass_filter(signal, cutoff, Fs, order)
    return y, Time 

def fft_ori(path, cutoff = 5, plot = False):
    t = 5
    path = str(path)
    spf = wave.open(path, "r")
    signal = spf.readframes(-1)
    signal = np.frombuffer(signal, np.int16)
    fs = spf.getframerate()
    Time = np.linspace(0, len(signal) / fs, num=len(signal))
    cutoff = cutoff
    order = 2
    y = butter_lowpass_filter(signal, cutoff, fs, order)
    return y, Time 

signal_EEU, time = fft_ori("arm_signal/EEU.wav", plot = False)
total_time = 60.0; # time in seconds [[1 s = 20000 buffer size]]
max_time = 5; # time plotted in window [s]
N_loops = (2*Fs/inputBufferSize)*total_time

T_acquire = inputBufferSize/(2*Fs)    # length of time that data is acquired for 
N_max_loops = max_time/T_acquire    # total number of loops to cover desire time window

data_cache = []
step_count = -4
not_in_signal = True
for k in range(0,int(N_loops)):
    
    # Read data from SpikerBox into a buffer of size input_buffer_size.
    byte_data = ser.read(inputBufferSize)

    # Cast to list of ints.
    byte_data = [int(byte_data[i]) for i in range(len(byte_data))]

    # Process with function defined above
    data_temp = process_data(byte_data)

    # data_temp = data_temp - 512

    if k <= N_max_loops:
        
        if k==0:
            data_plot = data_temp
        else:
            #data_plot = np.append(data_temp, data_plot)
            data_plot = np.append(data_temp, data_plot) # Plot from left to right by appending on the end
        
        t = (min(k+1,N_max_loops))*inputBufferSize/20000.0*np.linspace(0,1,len(data_plot)) 
    else:
        # We have reached the end of the specified number of loops
        data_plot = np.roll(data_plot, len(data_temp))
        data_plot[0:len(data_temp)] = data_temp
    
    t = (min(k+1,N_max_loops))*inputBufferSize/20000.0*np.linspace(0,1,len(data_plot)) 

    data_cache.append(data_temp)

    if(len(data_cache) == 5):
        data_cache.pop(0)
    
    if(len(data_cache) == 4):
        combined_data = np.concatenate(data_cache)

        if(k > step_count + 3 and not_in_signal):
            if(event(Fs, combined_data) == True):
                print("signal_detected")
                step_count = k
                not_in_signal = False
        
        if(k == step_count + 1):
            print("combined_data:")
            print(combined_data)
            print(tt_new(combined_data))


        if(k == step_count + 5):
            not_in_signal = True

    drawnow(makeFig)
    plt.pause(.000001)

if ser.read():
    ser.flushInput()
    ser.flushOutput()
    ser.close()