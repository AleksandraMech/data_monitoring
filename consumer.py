import pika
import time
#import random
#from producer_bathtube import measure, measure_time, measurement_device
import csv
import sys
import psycopg2
#import the error handling libraries for psychopg2
from psycopg2 import OperationalError, errorcodes, errors
import datetime
import json

#connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('guest', 'guest')))

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

def print_exception(err):
   err_type, err_obj, traceback = sys.exc_info()
   line_num = traceback.tb_lineno
   print("\ERROR:", err, "on line number:", line_num)
   print("traceback:", traceback, "-- typr:", err_type)
   print("\nextensions.Diagnostics:", err.diag)
   print("pgerror:", err.pgerror)
   print("pgcode:", err.pgcode, "\n")


def on_message_received(ch, method, properties, body):
    line = body.decode('ascii')  ##dzięki temu nie mam np b' 67' zamiast po prostu 67
    json_info = line.replace("\'","\"")

    while(1):
       try: 
          conn = psycopg2.connect(database="data_monitoring", user="postgres", password="albertina", host="localhost", port="5432")
          if conn != None:
             cur = conn.cursor()
             now = datetime.datetime.now().isoformat(' ', 'seconds')
             try:
               # cur.execute("INSERT INTO measurements (value) VALUES ('{\"values\": \"line\"}')") 
              #  zm = "INSERT INTO measurements (json_info) VALUES (%(line)s)" 
                zm = "INSERT INTO measurements (json_info, measurements_date) VALUES (\'"+str(line)+"\', '"+now+"')"
                #print(zm)  ## zrobic to za pomocą formatowanego stringa
                #cur.execute("INSERT INTO measurements (json_info) VALUES ('",str(json_string),"')")
                cur.execute(zm)
                print(f'{line} is received')

                patient_id= "SELECT json_info -> 'patient_id' as keyvalues FROM measurements" 
                cur.execute(patient_id)
                conn.commit()
                for(patient_id) in cur:
                  x = f'id pacjenta: {patient_id}'
                  print(x)
               
                otrzymane = "SELECT json_info -> 'values' as keyvalues FROM measurements" 
                cur.execute(otrzymane)
                conn.commit()

                for(values) in cur:
                  x = f'{values}'
                  print(x)
                cur.close()
                conn.close()
               # print(f'Otrzymane: {otrzymane}')

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


channel.basic_consume(queue= 'measurement_data', auto_ack=True, on_message_callback=on_message_received)

print('Starting Consuming')

channel.start_consuming()