import numpy as np


def eye_movement(Y, time, windowSize = 0.5, thresholdEvents = 20, downSampleRate = 50):

    ind = np.array(range(1, np.where(time == np.round(time[len(time) - 1], 4) + 1) + 1))
    ind = np.array(range(1, ind[len(ind)], step = downSampleRate))

    timeMiddle = time[ind] + windowSize/2
    zc = mean = [] 

    testStat = []
    for i in range(len(ind)):
        trueFalse = 0
        # ??? 
        # IN R:
        # Y_subset <- Y[time >= time[ind[i]] & time < time[ind[i]] + windowSize]
        # try python: not sure
        # if time >= time[ind[i]] and time < time[ind[i]] + windowSize:

        if (sum(Y_subset[0:len(Y_subset) - 1)] * Y_subset[1:len(Y_subset)] <= 0) == True:
            trueFalse += 1
        
        testStat.append(trueFalse)

    predictedEvent = np.where(testStat < thresholdEvents)
    eventTimes = timeMiddle[predictedEvent]
    gaps = np.where(diff(eventTimes) > windowSize)

    event_time_interval = min(eventTimes)

    for i in 1:len(gaps):
        event_time_interval.append(event_time_interval, )


            


            