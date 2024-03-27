"""
This is producer
"""


import sys
import pika
from simple_chalk import chalk

#establish connection to RMQ server instance
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

#declare queue
channel.queue_declare(queue='task_queue',durable=True)

#accept messages from command line
message = ' '.join(sys.argv[1:]) or "Hello World!"


#msg publish config
channel.basic_publish(exchange='',
                      routing_key="task_queue",
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent #store msg to disk
                      ))
print(chalk.green(f" [x] Sent {message}"))