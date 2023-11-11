import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import scpi.signal #12.30 filmu


column_names = [
    'ecg',
    't'
]

restingecg = pd.read_csv('Exercising.csv',
    names=column_names, sep = '.', decimal=',', engine='python', skiprows = 5000, skipfooter = 5000) #pomijam 5000 poczatkowych i koncowych linijek(5s z każdej strony bo pomiar był wykonany z 1000Hz)
   # names=column_names, sep = '.', decimal=',', engine='python')
#change times to seconds
restingecg.t = restingecg.t/1000

plt.plot(restingecg.t, restingecg.ecg, label='ekg') #dlaczego ten wykres mi sie nie wyswietla??
plt.show()
