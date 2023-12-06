import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import re
import numpy as np
import random
import time
import datetime



x_vals = []
y_vals = []
MAX_FRAMES = 100

index = count()

def plotting():
    while True:     
        conn = psycopg2.connect(database="data_monitoring", user="postgres", password="albertina", host="localhost", port="5432")
        if conn != None:
            cur = conn.cursor()

            query = 'SELECT measurements_date FROM measurements'
            cur.execute(query)
            conn.commit()
            x = [] 
            converted_value = []
            for(measurements_date) in cur:
                x.append(measurements_date)
              #  print('x: ',x) 
            cur.close()
            conn.close()     
            data2 =[]
            for i in x: 
                    print('i:',i)
                    to_convert2 = re.findall(r'\d+', str(i)) ##jak zmieniac wartosci w tym nawiasie???
                  #  converted = float(to_convert[0])
                    year = str(to_convert2[0])
                    month = str(to_convert2[1])
                    day = str(to_convert2[2])
                    hour = str(to_convert2[3])
                    minute = str(to_convert2[4])
                    second = str(to_convert2[5])
                    print('year:', year)  
                    print('month:', month)  
                    print('day:', day)  
                    print('hour:', hour) 
                    print('minute:', minute)  
                    print('second:', second)   
                    y = (hour+':'+minute+':'+second)   
                    measure_day = (day+'-'+month+'-'+year)
                    print('y: ',y,'measure day: ', measure_day)
    

plotting()
