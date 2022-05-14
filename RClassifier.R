
eye_movement_ZC = function(Y, time, 
                           windowSize = 0.5, 
                           thresholdEvents = 20,
                           downSampleRate = 50) {
  
  ## down sample
  ind = seq_len(which(time == round(time[length(time)] - windowSize, 4)) + 1)
  ind = seq(1, ind[length(ind)], by = downSampleRate)
  
  ## time vector for middle of each window
  timeMiddle <- time[ind] + windowSize/2 
  
  
  ## calculate zero-crossings
  SD = Max = ZeroCrossing = mean = min = testStat = rep(NA, length(ind))
  
  for (i in 1:length(ind)) {
    Y_subset <- Y[time >= time[ind[i]] & time < time[ind[i]] + windowSize]
    testStat[i] <- sum(Y_subset[1:(length(Y_subset) - 1)] * Y_subset[2:(length(Y_subset))] <= 0)
    
    
    SD[i] <- sd(Y_subset)
    Max[i] = max(Y_subset)
    mean[i] = mean(Y_subset)
    min[i] = -min(Y_subset) # take the negative here just for visualisations and easier to compare with other statistics
  }
  
  
  ## using threshold to determine eye movement intervals
  predictedEvent <- which(testStat < thresholdEvents)
  eventTimes <- timeMiddle[predictedEvent] # map back to the time of this 
  gaps <- which(diff(eventTimes) > windowSize )
  
  ## estimate event_time_interval
  event_time_interval <- min(eventTimes)
  for (i in 1:length(gaps)) {
    event_time_interval <- append(event_time_interval, 
                                  c(eventTimes[gaps[i]],
                                    eventTimes[gaps[i] + 1]))
  }
  event_time_interval <- append(event_time_interval, max(eventTimes))
  event_time_interval <- matrix(event_time_interval, ncol = 2, byrow = TRUE)
  
  predictedEventTimes <- rep(FALSE, length(Y))
  for (i in 1:nrow(event_time_interval)) {
    predictedEventTimes[event_time_interval[i, 1] <= time & event_time_interval[i, 2] >= time] <- TRUE
  }
  
  num_event <- length(gaps) + 1
  return(list(num_event = num_event, 
              predictedEventTimes = predictedEventTimes,
              predictedInterval = event_time_interval,
              testStat = testStat))
}