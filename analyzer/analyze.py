
import win_unicode_console
import numpy
import pandas
import time
import matplotlib.pyplot as plt

win_unicode_console.enable()

def remove_multiple_spikes(data, max_points_per_spike):
    no_spikes_data = data.copy()
   
    window = [None]*(max_points_per_spike+2)
    for i in range(0, len(window)):
        window[i] = data[i]

    for window_start_index in range(0, len(data)-len(window)):
        # detect spike
        edges_almost_the_same = abs(window[0]-window[-1]) < 2
        middles_are_spikes = False
        for i in range(1, len(window)-1):
            if abs(window[i]-window[0]) > 3 and abs(window[-1]-window[i]) > 3:
                middles_are_spikes = True
                break

        # if spike, replace with interpolated values
        if edges_almost_the_same and middles_are_spikes:
            d = (window[-1]-window[0])/(len(window)-1)
            for i in range(1, len(window)-1):
                no_spikes_data[window_start_index+i] = window[0]+i*d
            print('replacing',i,'points spike',data[window_start_index:window_start_index+len(window)].to_string(header=False,index=False).replace('\n',','),'with',no_spikes_data[window_start_index:window_start_index+len(window)].to_string(header=False,index=False).replace('\n',','))

        # move window
        for i in range(0, len(window)-1):
            window[i] = window[i+1]
        window[-1] = data[window_start_index+len(window)]

    return no_spikes_data

# def unit_test_remove_multiple_spikes():
#     assert [0,0,0] == remove_multiple_spikes([0,4,0], 1)
#     assert [0,0,0,0] == remove_multiple_spikes([0,7,8,0], 2)
#     assert [0,0,0,0,0] == remove_multiple_spikes([0,7,8,2,0], 3)

# print(remove_multiple_spikes([0,7,8,4,0], 3))
# unit_test_remove_multiple_spikes()
# exit()

def kalman_filter(unfiltered_data, K):
    kalman_data = unfiltered_data.copy()
    previous_kalman = unfiltered_data[0]
    for i in range(0, unfiltered_data.size):
        if i in unfiltered_data:
            kalman = K*unfiltered_data[i] + (1-K)*previous_kalman
            kalman_data[i] = kalman
            previous_kalman = kalman
            if i%10000 == 0:
                print('Kalman',i,'of', unfiltered_data.size)
    return kalman_data

def reduce(data, index, n):
    reduced_size = int(len(data)/n)
    reduced_data = [None]*reduced_size
    reduced_index = [None]*reduced_size

    for i in range(0, reduced_size):
        reduced_data[i] = data[i*n]
        reduced_index[i] = index[i*n]
    return reduced_data, reduced_index

start = time.time()
data = pandas.read_csv("../data/hardware.csv", delimiter=",", low_memory=True, parse_dates=['time'])
#data = pandas.read_csv("../data/hardware.csv", delimiter=",", low_memory=True, parse_dates=['time'], skiprows=lambda r: 0<r<3000000, nrows=100000)
end = time.time()
print('pandas',pandas.__version__,'read',len(data),'lines in',end-start)

start = time.time()
no_spikes_data = remove_multiple_spikes(data['level'], 1)
no_spikes_data = remove_multiple_spikes(no_spikes_data, 2)
no_spikes_data = remove_multiple_spikes(no_spikes_data, 3)
end = time.time()
print('remove spikes processed',len(data),'values in',end-start)

dataframe = pandas.DataFrame()
dataframe["level"] = no_spikes_data
dataframe.index = data['time']
dataframe.plot()
plt.gca().invert_yaxis()
plt.show()
exit()

level_kalman = kalman_filter(no_triple_spikes_data, K=0.01)

reduced_data, reduced_index = reduce(level_kalman, data['time'], 10)