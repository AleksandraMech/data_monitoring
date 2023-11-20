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

#connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('guest', 'guest'))

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
    #print(f'recived new message: {body}')
    line = body.decode('ascii')  ##dzięki temu nie mam np b' 67' zamiast po prostu 67
    json_info = line.replace("\'","\"")
    print(line)
    #with open('messages.csv', mode='a') as msg_file:
     # msg_writer = csv.writer(msg_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
     # msg_writer.writerow({body}) #.second, microsecond

    class Measure:
       def __init__(self, device, values):
          self.device = device
          self.values = values

    p1 = Measure("bathtube", line)
    with open("plik.json", "a") as plik:
        json_string = json.dumps(p1.__dict__, indent = 4)
        plik.write(json_string)

#### po co ja tworze ten plik json? czy kilka danych mam przypisać do jednej wartości? 

    #with open("plik.json", "r") as plik:
     # measure = Measure(**json.loads(plik.read()))
      # print(measure.device, measure.values)

   # insert_stmt = (
   #   "INSERT INTO measurements (device, value) "
   #  "VALUES (%s, %s)"
   # )
   # measurement_device = "bathtub"
    #data = (measurement_device, line)

    while(1):
       try: 
          conn = psycopg2.connect(database="data_monitoring", user="postgres", password="albertina", host="localhost", port="5432")
          if conn != None:
             cur = conn.cursor()
             now = datetime.datetime.now().isoformat(' ', 'seconds')
             try:
              #  cur.execute(insert_stmt, data)
                cur.execute("INSERT INTO measurements (json_info) VALUES ('{\"values\": \"line\"}')") ### podopisywac sobie wiecej wartosci
              #  cur.execute("INSERT INTO measurements (json_info ) VALUES (%s)", (json_info))
                #cur.execute("INSERT INTO measurements (producer, date, values ) VALUES ('{\"employees\": \"przykład\"}')") ### 
                conn.commit()
                cur.close()
                conn.close()
                print(f'{line} is received')
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