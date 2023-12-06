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

def print_exception(err):
   err_type, err_obj, traceback = sys.exc_info()
   line_num = traceback.tb_lineno
   print("\ERROR:", err, "on line number:", line_num)
   print("traceback:", traceback, "-- typr:", err_type)
   print("\nextensions.Diagnostics:", err.diag)
   print("pgerror:", err.pgerror)
   print("pgcode:", err.pgcode, "\n")


def plotting():
    while True:     
        conn = psycopg2.connect(database="data_monitoring", user="postgres", password="albertina", host="localhost", port="5432")
        if conn != None:
            cur = conn.cursor()
            otrzymane = "SELECT json_info -> 'values' as keyvalues FROM measurements" 
            cur.execute(otrzymane)
            # ll =  cur.fetchall()
            conn.commit()
            value = [] 
            converted_value = []
             #zamienic krotki na liste i pozniej iterowac po liscie # tuple
            for(values) in cur:
                #print(values) ##(' 78',)
                value.append(values)
                #print('value: ',value) ##[(' 56',)]

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

          #  print('lista',value)
            data =[]
            data2 =[]
            for i in value: 
                    #print('i:',i)
                    to_convert = re.findall(r'\d\d+', str(i)) ##jak zmieniac wartosci w tym nawiasie???
                  #  converted = float(to_convert[0])
                    converted = str(to_convert[0])
                    print('converted:', converted)        
                    data.append(converted)
                    print('data:', data)

            
            for ii in x: 
                   # print('i:',i)
                    to_convert2 = re.findall(r'\d+', str(ii)) ##jak zmieniac wartosci w tym nawiasie???
                  #  converted = float(to_convert[0])
                    year = str(to_convert2[0])
                    month = str(to_convert2[1])
                    day = str(to_convert2[2])
                    hour = str(to_convert2[3])
                    minute = str(to_convert2[4])
                    second = str(to_convert2[5])
                  #  print('year:', year)  
                  #  print('month:', month)  
                  #  print('day:', day)  
                   # print('hour:', hour) 
                  #  print('minute:', minute)  
                   # print('second:', second)   
                    y = (hour+':'+minute+':'+second)   
                    measure_day = (day+'-'+month+'-'+year)
                    print('y: ',y,'measure day: ', measure_day) 
                    data2.append(y) 
                    print('data2: ',data2)   

           
            #plt.plot(data,data2)
           # plt.show()
           # time.sleep(3)

plotting()

                #plt.cla()

                         #plt.plot(x, y1, label='Channel 1')
                         #plt.plot(x, y2, label='Channel 2')

                         #plt.legend(loc='upper left')
                        # plt.tight_layout()
                        

   # data = pd.read_csv('data.csv')
  #  x = data['x_value']
   # y1 = data['total_1']
  #  y2 = data['total_2']

   # plt.cla()

    #plt.plot(x, y1, label='Channel 1')
    #plt.plot(x, y2, label='Channel 2')

    #plt.legend(loc='upper left')
    #plt.tight_layout()


#ani = FuncAnimation(plt.gcf(), animate, interval=1000, save_count=MAX_FRAMES) #gcf= get current figure ; 1000=1sekunda

#plt.tight_layout()
#plt.show()