import pika
import time
import random
import datetime
import json

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()
channel.queue_declare(queue='measurement_data')

while(True):

    measure = random.randint(55, 90)
    measure_time = datetime.datetime.now()
    measurement_device = "bathtub"
    message = f" {measure}"
    now = datetime.datetime.now().isoformat(' ', 'seconds')

    class Measure:
      def __init__(self, patient_id, sender, context, messageType, answerType, HR, measurement_time):
         self.patient_id = patient_id
         self.sender = sender
         self.context = context
         self.messageType = messageType
         self.answerType = answerType
         self.HR = HR
         self.measurement_time = measurement_time


    p1 = Measure("24", "amech", "bathtube", "data", "measure", message, now)
    with open("plik.json", "a") as plik:
        json_string = json.dumps(p1.__dict__)
        plik.write(json_string)

    channel.basic_publish(exchange='', routing_key='measurement_data', body=json_string)

    print(f"sent message from bathtube: {message}")
    
    time.sleep(3)


