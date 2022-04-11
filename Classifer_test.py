import numpy as np


def movement_classifier(data, xtime, sample_rate):
    window_size = 0.1
    threshold_events = 100
    down_sample_rate = 100

    ind = np.arange(0, np.where(xtime == round(xtime[len(xtime) - 1] - window_size, 4))[0][0], down_sample_rate)

    t_stat = [0]*len(ind)

    for i in range(len(ind)):
        data_subset = data[ind[i] : ind[i] + int(window_size * sample_rate)]
        t_stat[i] = np.std(data_subset)

    predicted_event = [x for x in range(len(t_stat)) if t_stat[x] > threshold_events]
    time_middle = [] 
    for i in predicted_event:
        time_middle.append(xtime[ind[i]] + window_size/2)

    intervals = [] 
    cut_point = predicted_event[0] 
    middle_time = int(sample_rate * window_size/2)
    for i in range(len(predicted_event)-1):
        if predicted_event[i+1] != predicted_event[i] + 1:
            intervals.append((ind[cut_point] + middle_time, ind[predicted_event[i]]+middle_time))

    return intervals
