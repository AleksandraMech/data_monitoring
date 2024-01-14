import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import psycopg2
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


def plotting():
    pomiar = 0
    while True:     
        conn = psycopg2.connect(database="data_monitoring", user="postgres", password="albertina", host="localhost", port="5432")
        if conn != None:
            cur = conn.cursor()
            otrzymane = "SELECT json_info -> 'heart_rate' as keyvalues FROM measurements" 
            cur.execute(otrzymane)
            conn.commit()
            pomiar = pomiar+1
            print("pomiar", pomiar )
            value = [] 
            min = None
            max = None
            mean = None
            sum = 0
            numbers = 0
            for(values) in cur:
                value.append(values)
            for n in value: 
                con3 = re.findall(r'\d\d+', str(n))
                nn = int(con3[0])
                sum += nn
                numbers += 1 
                if min == None or min > n:
                     min = n
                     con = re.findall(r'\d\d+', str(min))
                     min_hr = (con[0])
                if max == None or max < n:
                     max = n 
                     con2 = re.findall(r'\d\d+', str(max))
                     max_hr = str(con2[0])

            mean = sum/numbers
            print("min: ", min_hr, "max: ", max_hr, "mean: ", mean)
            
            query = 'SELECT measurements_date FROM measurements'
            cur.execute(query)
            conn.commit()
            x = [] 
            for(measurements_date) in cur:
                x.append(measurements_date)
           # cur.close()
            #conn.close()       
            data =[]
            data2 =[]
           
            for i in value: 
                    to_convert = re.findall(r'\d\d+', str(i))
                    converted = str(to_convert[0])       
                    data.append(converted)      
            id = "SELECT json_info -> 'patient_id' as keyvalues FROM measurements" 
            cur.execute(id)
            patient_id_nr = [] 
            for(nr) in cur:
                patient_id_numbers = "".join(str(nr))
                patient_id_nr.append(patient_id_numbers)
                print('patient id number: ', patient_id_nr)
            dane =[]
            for k in patient_id_nr:
                to_convert2 = re.findall(r'\d\d+', str(k)) 
                converted2 = str(to_convert[0])     
                dane.append(converted2)    
                if converted2 == 24:
                    print('tak')
                else:
                    print('nie')     

            patient_id = 'SELECT patient_id FROM patient'
            cur.execute(patient_id)
            patients_id = [] 
            for(patient_id) in cur:         
                id =  "".join(str(patient_id))
                patients_id.append(id)
            print(' patient_id : ',  patients_id) 
                
            names= 'SELECT name FROM patient'
            cur.execute(names)
            patient_names = [] 
            for(names) in cur:         
                patient_name =  "".join(names)
                patient_names.append(patient_name)
            print(' patient_names : ', patient_names) 
                    
            mails= 'SELECT mail FROM patient'
            cur.execute(mails)
            patient_mails = [] 
            for(mails) in cur:         
                mail =  "".join(mails)
                patient_mails.append(mail)
            print(' patient_mails : ', patient_mails) 

            devicefromtable = "SELECT json_info -> 'device' as keyvalues FROM measurements" 
            cur.execute(devicefromtable)
            devices = [] 
            for(device) in cur:
                devices.append(device)
                measurement_devices =  "".join(device)

            measurement_device = measurement_devices
            print('measurement device: ', measurement_device)

            query = 'SELECT measurements_date FROM measurements'
            cur.execute(query)
            conn.commit()
            x = [] 
            converted_value = []
            for(measurements_date) in cur:
                x.append(measurements_date)
            cur.close()
            conn.close()       
            data =[]
            data2 =[]
           
            for i in value: 
                    to_convert = re.findall(r'\d\d+', str(i)) 
                    converted = str(to_convert[0])       
                    data.append(converted)
            
            for ii in x: 
                    to_convert2 = re.findall(r'\d+', str(ii)) 
                    year = str(to_convert2[0])
                    month = str(to_convert2[1])
                    day = str(to_convert2[2])
                    hour = str(to_convert2[3])
                    minute = str(to_convert2[4])
                    second = str(to_convert2[5])
                    print('year:', year)     
                    y = (hour+':'+minute+':'+second)   
                    measure_day = (day+'-'+month+'-'+year)
                    data2.append(y) 
            plt.plot(data2,data)
            plt.show()
            time.sleep(3)

plotting()

                