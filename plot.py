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
                        
                x=0
                for line in value: 
                    to_convert = re.findall(r'\d\d+', str(value[0]))
                    converted = float(to_convert[0])
                    rand_val = (str(converted))
                    #  rand_val = (str(value[0]))
                    print('ranomowa wartosc:', rand_val)
                    line =+1
                    y_vec[-1] = rand_val
                    y1_data = rand_val
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

    