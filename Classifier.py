from random import sample
import numpy as np

def movement_classifier(data, time, down_sample_rate = 100):
    # able to modify these
    window_size = 0.5 # could be 0.5, try all.
    threshold_events = 20 # we can try 20
    down_sample_rate = 100 # we can try 50 here aswell

    # 1. Down Sampling
    ind = np.arange(0, np.where(np.round(time,4) == round(time[len(time) - 1] - window_size, 4))[0][0], down_sample_rate)

    t_stat = [0]*len(ind)


    # 2. Calculating SD
    array = result = [] 

    for i in range(len(ind)):
        data_subset = data[ind[i] : ind[i] + int(window_size * down_sample_rate)]
        t_stat[i] = np.std(data_subset)
    # zc = [0]*len(ind)
    # for i in range(len(ind)):
    #     data_subset = data[ind[i] : ind[i] + int(window_size * down_sample_rate)]
    #     t_stat[i] = np.std(data_subset)
        
    #     data_subset = np.array(data_subset)

    #     bools = np.dot(data_subset[0:len(data_subset) - 1], data_subset[1:len(data_subset)])
    #     array.append(bools) # declare and sub in

    #     for j in array:
    #         if j <= 0:
    #             result.append(1) # change to declare from numpy 
    #         else:
    #             result.append(0)
    #         zc[i] = sum(result)

    # 3. Use threshold to determine movement intervals
    predicted_event = [x for x in range(len(t_stat)) if t_stat[x] < threshold_events]

    # predicted_event_zc = [x for x in range(len(zc)) if zc[x] < threshold_events]
    # time vector for middle of each window 

    time_middle = []
    for i in predicted_event:
        time_middle.append(time[ind[i]] + window_size/2)

    # for i in predicted_event_zc:
    #     time_middle.append(time[ind[i]] + window_size/2)

    # 4. Estimation 
    intervals = [] 
    # intervals_zc = []
    cut_point = predicted_event[0]
    # cut_point_zc = predicted_event_zc[0]

    middle_time = int(down_sample_rate * window_size/2)
    for i in range(len(predicted_event) - 1):
        if predicted_event[i+1] != predicted_event[i] + 1:
            intervals.append((int(ind[cut_point] + middle_time)/10000, int(ind[predicted_event[i]] + middle_time)/10000))
            cut_point = predicted_event[i+1]
    intervals.append((int(ind[cut_point] + middle_time)/10000, int(ind[predicted_event[-1]] + middle_time)/10000))


# # INTERVALS ZC
#     for i in range(len(predicted_event_zc) - 1):
#         if predicted_event_zc[i+1] != predicted_event_zc[i] + 1:
#             intervals_zc.append((int(ind[cut_point_zc] + middle_time)/10000, int(ind[predicted_event_zc[i]] + middle_time)/10000))
#             cut_point_zc = predicted_event_zc[i+1]
#     intervals_zc.append((int(ind[cut_point] + middle_time)/10000, int(ind[predicted_event_zc[-1]] + middle_time)/10000))
    
    # return intervals
    return intervals
    




