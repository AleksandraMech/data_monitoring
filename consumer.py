import pika
import time
import random
#from producer_bathtube import measure, measure_time, measurement_device
import csv

#def on_message_received(ch, method, properties, body):
   # processing_time = random.randint(1, 6)
 #   print(f'received: "{body}", will take {processing_time} to process')
  #  time.sleep(processing_time)
  #  ch.basic_ack(delivery_tag=method.delivery_tag) #ch=channel
  #  print(f'finished processing and acknowledged message')

def on_message_received(ch, method, properties, body):
    print(f'recived new message: {body}')
   # fieldnames = ["messageId", "measure", "measure_time", "measurement_device"]
    with open('messages.csv', mode='a') as msg_file:
    #  msg_writer = csv.DictWriter(msg_file, fieldnames=fieldnames)
     # msg_writer.writeheader()
     # while True:
        #with open('messages.csv', 'a') as msg_writer:
       # msg_writer = csv.DictWriter(csv_file, headers_for_csv=headers_for_csv)
       # info = {
         #   "messageId": messageId,
         #   "measure": measure,
          #  "measure_time": measure_time
          #  "measurement_device": measurement_device
       # }
       # csv_writer.writerow(info)
      #  print(messageId, measure, measure_time, measurement_device)
      msg_writer = csv.writer(msg_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      msg_writer.writerow({body}) #.second, microsecond
    
connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='C')

#queue = channel.queue_declare(queue='', exclusive=True)  #exclusive=true mowi brokerowi, ze gdy polaczenie consummera jest zamkniete, to kolejka moze zostac usunieta

channel.basic_qos(prefetch_count=1) #qos = quality of service //1 bo kazdy konsument bedzie dostawał jedną wiadomość na raz
#channel.basic_consume(queue= 'measurement_data_bathtub', on_message_callback=on_message_received)

channel.basic_consume(queue= 'measurement_data', auto_ack=True, on_message_callback=on_message_received)

print('Starting Consuming')

channel.start_consuming()

#with open('messages.csv', mode='a') as msg_file:
        #msg_writer = csv.writer(msg_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      #  msg_writer.writerow([measure, measure_time, measurement_device]) #.second, microsecond