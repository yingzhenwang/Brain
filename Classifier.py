import numpy as np


def eye_movement(Y, time, windowSize = 0.5, thresholdEvents = 20, downSampleRate = 50):

    ind = np.array(range(1, np.where(time == np.round(time[len(time) - 1], 4) + 1) + 1))
    ind = np.array(range(1, ind[len(ind)], step = downSampleRate))

    timeMiddle = time[ind] + windowSize/2
    zc = mean = [] 

    for i in range(len(ind)):
        if time >= time[ind[i]] and time < time[ind[i]] + windowSize:


