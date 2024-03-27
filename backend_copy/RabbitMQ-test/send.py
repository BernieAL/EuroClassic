

import pika

#Establish connection to broker server (RabbitMQ server instance)
#For a broker on another machine - use name or IP of where its located
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

#create recipient queue called 'hello', where message will be delivered.
#if you send a message to non-existent lcoation, RabbitMQ drops the message
channel.queue_declare(queue='hello')

#Messages MUST go through an exchange to reach the queue
#Use default exchange (empty string) to send message to queue (hello)
channel.basic_publish(exchange='',routing_key='hello',body='Hello World!')
print("[x] Sent 'Hello World!'")

#before exiting, make sure network buffers are flushed and message was delivered to RabbitMQ
#Gently close connection
connection.close()