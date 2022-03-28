import serial
import numpy as np
import matplotlib.pyplot as plt
import time

def read_arduino(ser,inputBufferSize):
#    data = ser.readline(inputBufferSize)
    data = ser.read(inputBufferSize)
    out =[(int(data[i])) for i in range(0,len(data))]
    return out

def process_data(data):
    data_in = np.array(data)
    result = []
    i = 1
    while i < len(data_in)-1:
        if data_in[i] > 127:
            # Found beginning of frame
            # Extract one sample from 2 bytes
            intout = (np.bitwise_and(data_in[i],127))*128
            i = i + 1
            intout = intout + data_in[i]
            result = np.append(result,intout)
        i=i+1
    return result

# Read example data
baudrate = 230400
#cport = 'COM12'  # set the correct port before you run it
cport = '/dev/cu.usbserial-DJ00DVKR'#.usbmodem141101'  # set the correct port before run it
ser = serial.Serial(port=cport, baudrate=baudrate)

inputBufferSize = 10000 # keep betweein 2000-20000
ser.timeout = inputBufferSize/20000.0  # set read timeout, 20000 is one second
#ser.set_buffer_size(rx_size = inputBufferSize)


total_time = 200.0; # time in seconds [[1 s = 20000 buffer size]]
max_time = 10.0; # time plotted in window [s]
N_loops = 20000.0/inputBufferSize*total_time

T_acquire = inputBufferSize/20000.0    # length of time that data is acquired for
N_max_loops = max_time/T_acquire    # total number of loops to cover desire time window

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
plt.ion()
fig.show()
fig.canvas.draw()

k = 0
#while True:
while k < N_loops: #Will end early so can't run forever.
    data = read_arduino(ser,inputBufferSize)
    data_temp = process_data(data)
    if k <= N_max_loops:
        if k==0:
            data_plot = data_temp
        else:
            data_plot = np.append(data_temp,data_plot)
        t = (min(k+1,N_max_loops))*inputBufferSize/20000.0*np.linspace(0,1,(data_plot).size)
    else:
        data_plot = np.roll(data_plot,len(data_temp))
        data_plot[0:len(data_temp)] = data_temp
    t = (min(k+1,N_max_loops))*inputBufferSize/20000.0*np.linspace(0,1,(data_plot).size)


#    plt.xlim([0,max_time])
    ax1.clear()
    ax1.set_xlim(0, max_time)
    plt.xlabel('time [s]')
    ax1.plot(t,data_plot)
    fig.canvas.draw()
    plt.draw()
    plt.pause(0.001)
    print(data_plot,t)
    k += 1

# save the plot above when ready
name_of_file = 'example_file.txt'
np.savetxt(name_of_file, np.c_[t, np.real(data_plot)])

"""
# load the above if needed
temp = np.loadtxt(name_of_file)
plt.figure()
plt.plot(temp[:,0],temp[:,1])
plt.plot(temp[:,2],temp[:,3])
plt.show()
"""

# close serial port if necessary
if ser.read():
    ser.flushInput()
    ser.flushOutput()
    ser.close()
