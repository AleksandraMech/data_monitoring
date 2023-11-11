from py_live import live_plotter
import numpy as np
import random

size = 100
x_vec = np.linspace(0,300,size+1)[1:-1]
y_vec = np.random.randn(len(x_vec))
#y_vec = np.random.randint(50, 80)
line1 = []
while True:
    rand_val = np.random.randn(1)
    y_vec[-1] = rand_val
    line1 = live_plotter(x_vec,y_vec,line1)
    y_vec = np.append(y_vec[1:],0.0)