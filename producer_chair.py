import pika
import time
import random
import datetime

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel() #connection could have many different channels

channel.queue_declare(queue='measurement_data')

#message = "Hello this is my first message"
#channel.basic_publish(exchange='', routing_key='measurement_data', body=message) # nie można bezposrednio przesylac wiadomosci, musi to byc przez exchange
#print(f"sent message: {message}")
#connection.close()

messageId = 1

while(True):

    measure = random.randint(50, 80)
    measure_time = datetime.datetime.now()
    measurement_device = "chair"

    message = f" {messageId}, {measure}, {measure_time}, {measurement_device} "

    channel.basic_publish(exchange='', routing_key='measurement_data', body=message)

    print(f"sent message from bathtube: {message}")
    
    time.sleep(0.1)

    messageId+=1