from py_live import live_plotter
import numpy as np
import random
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import sys
import re
import time

def print_exception(err):
   err_type, err_obj, traceback = sys.exc_info()
   line_num = traceback.tb_lineno
   print("\ERROR:", err, "on line number:", line_num)
   print("traceback:", traceback, "-- typr:", err_type)
   print("\nextensions.Diagnostics:", err.diag)
   print("pgerror:", err.pgerror)
   print("pgcode:", err.pgcode, "\n")


size = 100
x_vec = np.linspace(0,300,size+1)[1:-1]
y_vec = np.random.randn(len(x_vec))
line1 = []
print('1234')
while True:
    try:
        print('123')
        conn = psycopg2.connect(database="data_monitoring", user="postgres", password="albertina", host="localhost", port="5432")
        if conn != None:
            cur = conn.cursor()
            try:

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
                        
                cur.close()
                conn.close()
                #rand_val = np.random.randn(1)
                # rand_val = (str(values))[2:-3] #decyduje o wartościach y na wykresie
                 # to_convert = re.findall(r'\d+\.\d+', value)
                 

                query = 'SELECT measurements_date FROM measurements'
                cur.execute(query)
                conn.commit()
                x = [] 
                converted_value = []
                for(measurements_date) in cur:
                    x.append(measurements_date)
                #  print('x: ',x) 
              #  cur.close()
                #conn.close()       

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
              
                        y_vec[-1] = data
                        y1_data = data2
                    #  y_vec[-1] = float(rand_val)
                        line1 = live_plotter(x_vec,y_vec,line1)
                        y_vec = np.append(y_vec[1:],0.0)
                        break
            except Exception as err:
                print_exception(err)
                conn.rollback()
                continue
    except OperationalError as err:
        print_exception(err)
        conn = None
        time.sleep(5.0)
        print('Wait for connection')
        continue

    