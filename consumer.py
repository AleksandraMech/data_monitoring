import pika
import time
#import random
#from producer_bathtube import measure, measure_time, measurement_device
#import csv
import sys
import psycopg2
#import the error handling libraries for psychopg2
from psycopg2 import OperationalError, errorcodes, errors
import datetime

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
    print(f'recived new message: {body}')
    line = body.decode('ascii')
    json_info = line.replace("\'","\"")
    print(line)
    #with open('messages.csv', mode='a') as msg_file:
     # msg_writer = csv.writer(msg_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
     # msg_writer.writerow({body}) #.second, microsecond

    while(1):
       try: 
          conn = psycopg2.connect(database="data_monitoring", user="postgres", password="albertina", host="localhost", port="5432")
          if conn != None:
             cur = conn.cursor()
             now = datetime.datetime.now().isoformat(' ', 'seconds')
             try:
                cur.execute("INSERT INTO measurements (json_info) VALUES ('{\"employees\": \"dx\"}')") ### podopisywac sobie wiecej wartosci
                conn.commit()
                cur.close()
                conn.close()
                print(f'{body} is received')
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

              
#connection_parameters = pika.ConnectionParameters('localhost')
#connection = pika.BlockingConnection(connection_parameters)
#channel = connection.channel()
#channel.queue_declare(queue='C')
#queue = channel.queue_declare(queue='', exclusive=True)  #exclusive=true mowi brokerowi, ze gdy polaczenie consummera jest zamkniete, to kolejka moze zostac usunieta
#channel.basic_qos(prefetch_count=1) #qos = quality of service //1 bo kazdy konsument bedzie dostawał jedną wiadomość na raz
#channel.basic_consume(queue= 'measurement_data_bathtub', on_message_callback=on_message_received)

channel.basic_consume(queue= 'measurement_data', auto_ack=True, on_message_callback=on_message_received)
#channel.basic_consume(queue="measurement_data", on_message_callback=on_message_received, auto_ack=True)

print('Starting Consuming')

channel.start_consuming()