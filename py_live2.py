import matplotlib.pyplot as plt
import numpy as np
import datetime

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')

def live_plotter(data,data2,line1,identifier='',pause_time=0.1):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(data,data2,'-o',alpha=1)        
        #update plot label/title
        plt.ylabel('heart rate')
        plt.title('Heart rate value measurement {}'.format(identifier))
        plt.show()
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(data2) ##powoduje update wartosci na wykresie
   # line1.set_data(x_vec,y1_data)
   # measure_time = datetime.datetime.now()
   # measure_time = 1
    #line1.axes.set_xticklabels(y_vec)
    
    # adjust limits if new data goes beyond bounds
    if np.min(data2)<=line1.axes.get_ylim()[0] or np.max(data2)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(data2)-np.std(data2),np.max(data2)+np.std(data2)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return line1