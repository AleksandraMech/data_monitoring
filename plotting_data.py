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



while True:     
    conn = psycopg2.connect(database="data_monitoring", user="postgres", password="albertina", host="localhost", port="5432")
    if conn != None:
        cur = conn.cursor()
        otrzymane = "SELECT json_info -> 'values' as keyvalues FROM measurements" 
        ##sprobowac za zapytania zrobic liste
        cur.execute(otrzymane)
       # ll =  cur.fetchall()
        conn.commit()
        value = [] 
        converted_value = []
    #zamienic krotki na liste i pozniej iterowac po liscie # tuple
       # print('cur:', ll)
        for(values) in cur:
            #print(values) ##(' 78',)
            value.append(values)
            print(value) ##[(' 56',)]
        for(values) in cur:
            #print(values) ##(' 78',)
            value.append(values)
            print(value) ##[(' 56',)]
        cur.close()
        conn.close()     
        print('lista',value)
        data =[]
        for i in value: 
                print('i:',i)
                to_convert = re.findall(r'\d\d+', str(i)) ##jak zmieniac wartosci w tym nawiasie???
                converted = float(to_convert[0])
                print('converted:', converted)
                #rand_val = (str(converted))
               
                data.append(converted)
                print('data:', data)
                y_vec = np.random.randn(len(data))
        plt.plot(data)
        plt.show()
        time.sleep(3)
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