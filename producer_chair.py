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

messageId = 1

while(True):

    measure = random.randint(50, 80)
    measure_time = datetime.datetime.now()
    measurement_device = "bathtub"

  #  message = f"{messageId}, {measure}, {measure_time}, {measurement_device} "
    message = f" {measure}"
    
    class Measure:
       def __init__(self, device, values):
          self.device = device
          self.values = values

    p2 = Measure("chair", message)
    with open("plik.json", "a") as plik:
        json_string = json.dumps(p2.__dict__)
       # print(json_string)
        plik.write(json_string)

  #  message = f" {measure}"
    
    channel.basic_publish(exchange='', routing_key='measurement_data', body=json_string)

    print(f"sent message from chair: {message}")
    
    time.sleep(random.randint(1, 4))

    messageId+=1
   




