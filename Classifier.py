from random import sample
import numpy as np

def movement_classifier(data, time, down_sample_rate = 100):
    # able to modify these
    window_size = 0.5 # could be 0.5, try all.
    threshold_events = 20 # we can try 20
    down_sample_rate = 50 # we can try 50 here aswell

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
    middle_time = int(down_sample_rate * window_size/2)
    for i in range(len(predicted_event) - 1):
        if predicted_event[i+1] != predicted_event[i] + 1:
            intervals.append((ind[cut_point] + middle_time, ind[predicted_event[i]] + middle_time))
            cut_point = predicted_event[i+1]
    intervals.append((ind[cut_point] + middle_time, ind[predicted_event[-1]] + middle_time))

    return intervals




