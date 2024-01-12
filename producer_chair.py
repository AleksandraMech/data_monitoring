import pika
import time
import random
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

    message = f" {measure}"
    
    class Measure:
       def __init__(self, patient_id, sender, context, messageType, answerType, HR):
          self.patient_id = patient_id
          self.sender = sender
          self.context = context
          self.messageType = messageType
          self.answerType = answerType
          self.HR = HR


    p2 = Measure("24", "amech", "echair", "messageId", "measure", message)
    with open("plik.json", "a") as plik:
        json_string = json.dumps(p2.__dict__)
        plik.write(json_string)
    
    channel.basic_publish(exchange='', routing_key='measurement_data', body=json_string)

    print(f"sent message from chair: {message}")
    
    time.sleep(random.randint(1, 4))

    messageId+=1
   




