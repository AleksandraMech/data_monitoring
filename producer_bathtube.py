import pika
import time
import random
#import csv
import datetime
import json

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='measurement_data')

#message = "Hello this is my first message"
#channel.basic_publish(exchange='', routing_key='measurement_data', body=message) # nie można bezposrednio przesylac wiadomosci, musi to byc przez exchange
#print(f"sent message: {message}")
#connection.close()

messageId = 1

while(True):

    measure = random.randint(55, 90)
    measure_time = datetime.datetime.now()
    measurement_device = "bathtub"
    message = f" {measure}"
    
    class Measure:
       def __init__(self, device, heart_rate, patient_id):
          self.device = device
          self.heart_rate = heart_rate
          self.patient_id = patient_id

    p1 = Measure("bathtube", message, "24")
    with open("plik.json", "a") as plik:
        json_string = json.dumps(p1.__dict__)
       # print(json_string)
        plik.write(json_string)

  #  message = f" {measure}"
    #message = [messageId, measure, measure_time, measurement_device] #czy ja moge przesyłac tylko wiadomosci i nie moge zmiennych?
    
    channel.basic_publish(exchange='', routing_key='measurement_data', body=json_string)

    print(f"sent message from bathtube: {message}")
    
    #time.sleep(random.randint(1, 4)) #zmienic na 3
    time.sleep(3)

    messageId+=1
   
   # with open('messages.csv', mode='a') as msg_file:
  #      msg_writer = csv.writer(msg_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
   #     msg_writer.writerow([measure, measure_time]) #.second, microsecond



