from py_live import live_plotter
import numpy as np
import random
import psycopg2
import re

size = 100
x_vec = np.linspace(0,300,size+1)[1:-1]
y_vec = np.random.randn(len(x_vec))
#y_vec = np.random.randint(50, 80)
line1 = []
while True:
    ## dodac try i except
    conn = psycopg2.connect(database="data_monitoring", user="postgres", password="albertina", host="localhost", port="5432")
    if conn != None:
         cur = conn.cursor()
         
         otrzymane = "SELECT json_info -> 'values' as keyvalues FROM measurements" 
         cur.execute(otrzymane)
         conn.commit()
         #print(f'Otrzymane: {otrzymane}')
         value = [] 
         #zamienic krotki na liste i pozniej iterowac po liscie # tuple
         for(values) in cur:
             #print(values) ##(' 78',)
             
             value.append(values)
             print(value) ##[(' 56',)]
           #  to_convert = re.findall(r'\d+\.\d+', value)
             #to_convert = re.findall(r'\d', values)
           # converted = float(to_convert[0])

             #input_string = 'x3.1417z'
             #input_string = values
            # to_convert = re.findall(r'\d+\.\d+', input_string)
            # print(to_convert) # ['3.1417']
           #  converted = float(to_convert[0])
           #  print(converted) # 3.1417

             #x = f'{values}'
            # print(value)
           #  print(converted)

              
         cur.close()
         conn.close()
          #rand_val = np.random.randn(1)
   # rand_val = (str(values))[2:-3] #decyduje o wartościach y na wykresie

   # to_convert = re.findall(r'\d+\.\d+', value)
         to_convert = re.findall(r'\d\d+', str(value[0]))
         converted = float(to_convert[0])
         rand_val = (str(converted))
  #  rand_val = (str(value[0]))
         print('ranomowa wartosc:',rand_val)
         y_vec[-1] = float(rand_val)
         line1 = live_plotter(x_vec,y_vec,line1)
         y_vec = np.append(y_vec[1:],0.0)
         

   