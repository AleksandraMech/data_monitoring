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
           #converted_value = []
            min = None
            max = None
            mean = None
           
            sum = 0
            numbers = 0
             #zamienic krotki na liste i pozniej iterowac po liscie # tuple
            for(values) in cur:
                #print(values) ##(' 78',)
                value.append(values)
                
                #print('value: ',value) ##[(' 56',)]

            for n in value: 
                con3 = re.findall(r'\d\d+', str(n))
                nn = int(con3[0])
                sum += nn
               # print("sum:", sum)
                numbers += 1 

                if min == None or min > n:
                     min = n
                    # print("typemin",type(min))
                     con = re.findall(r'\d\d+', str(min))
                     min_hr = (con[0])
                if max == None or max < n:
                     max = n 
                     con2 = re.findall(r'\d\d+', str(max))
                     max_hr = str(con2[0])

            mean = sum/numbers
            print("min: ", min_hr, "max: ", max_hr, "mean: ", mean)
           # print("typeminn",type(min_hr))
           ############################################
            
         
                    
            id = 'SELECT patient_id FROM measurements'
            cur.execute(id)
            patient_id_nr = [] 
            for(nr) in cur:
                patient_id_numbers = "".join(str(nr))
                patient_id_nr.append(patient_id_numbers)
                print('patient id number: ', patient_id_nr)
            dane =[]
            for k in patient_id_nr:
                to_convert2 = re.findall(r'\d\d+', str(k)) ##jak zmieniac wartosci w tym nawiasie???
                converted2 = str(to_convert2[0])     
                dane.append(converted2)    
                if converted2 == 24:
                    print('tak')
                else:
                    print('nie')
                    
            
            

            patient_id = 'SELECT patient_id FROM patient'
            cur.execute(patient_id)
            #print(patient_id)
            patients_id = [] 
            for(patient_id) in cur:         
                id =  "".join(str(patient_id))
                patients_id.append(id)
            print(' patient_id : ',  patients_id) #lista

           
                
            names= 'SELECT name FROM patient'
            cur.execute(names)
           # print(names)
            patient_names = [] 
            for(names) in cur:         
                patient_name =  "".join(names)
                patient_names.append(patient_name)
            print(' patient_names : ', patient_names) #lista
                    
            mails= 'SELECT mail FROM patient'
            cur.execute(mails)
           # print(mails)
            patient_mails = [] 
            for(mails) in cur:         
                mail =  "".join(mails)
                patient_mails.append(mail)
            print(' patient_mails : ', patient_mails) #lista

         

            devicefromtable = "SELECT json_info -> 'device' as keyvalues FROM measurements" 
            cur.execute(devicefromtable)
            devices = [] 
            for(device) in cur:
                devices.append(device)
                measurement_devices =  "".join(device)
           # for n in devices: 
              # measurement_devices = n
           
               # print('measurement device: ', measurement_devices)
            measurement_device = measurement_devices
            print('measurement device: ', measurement_device)

            query = 'SELECT measurements_date FROM measurements'
            cur.execute(query)
            conn.commit()
            x = [] 
            converted_value = []
            for(measurements_date) in cur:
                x.append(measurements_date)
              ###  measurement_time =  "".join(measurements_date)
               ### print('meesure time: ', measurement_time)
            cur.close()
            conn.close()       
            data =[]
            data2 =[]
           
            for i in value: 
                    to_convert = re.findall(r'\d\d+', str(i)) ##jak zmieniac wartosci w tym nawiasie???
                    converted = str(to_convert[0])
                    #print('converted:', converted)        
                    data.append(converted)
                   # print('data:', data)
                   # ostatnie_dwadziescia = 
            
            for ii in x: 
                    to_convert2 = re.findall(r'\d+', str(ii)) ##jak zmieniac wartosci w tym nawiasie???
                    year = str(to_convert2[0])
                    month = str(to_convert2[1])
                    day = str(to_convert2[2])
                    hour = str(to_convert2[3])
                    minute = str(to_convert2[4])
                    second = str(to_convert2[5])
                   # print('year:', year)  
                  #  print('month:', month)  
                  #  print('day:', day)  
                   # print('hour:', hour) 
                  #  print('minute:', minute)  
                   # print('second:', second)   
                    y = (hour+':'+minute+':'+second)   
                    measure_day = (day+'-'+month+'-'+year)
                  #  print('y: ',y,'measure day: ', measure_day) 
                    data2.append(y) 
                   # print('data2: ',data2) 

            plt.plot(data2,data)
            plt.show()
            time.sleep(3)

plotting()

                