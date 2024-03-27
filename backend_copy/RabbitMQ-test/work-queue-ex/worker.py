"""
This is consumer

this script simulated a second of work for each dot in the message body

'Hello.' -> 1 second of simulated work
'Hello.. '-> 2 seconds of simulated work

"""
import time  
import pika
import os,sys
from simple_chalk import chalk

def main():
    
    #Establish connection to broker server (RabbitMQ server instance)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    #Declare queue - cant assume queue prev declared - better to be safe
    # channel.queue_declare(queue='hello')
    channel.queue_declare(queue='task_queue',durable=True)

    #callback func for when a message is rec'd
    def callback(ch, method, properties, body):
        print(chalk.green(f" [x] Received {body.decode()}"))
        time.sleep(body.count(b'.'))
        print(chalk.green(" [x] Done"))
        ch.basic_ack(delivery_tag = method.delivery_tag) #manual ack response

    #define basic_consume process
    #listen for messages from 'task_queue' queue and pass to callback for processing
    channel.basic_qos(prefetch_count=1) #fair dispatching, worker msg limit 1 until ack
    channel.basic_consume(queue='task_queue',on_message_callback=callback)
    
    #listen indefinitley for messages
    print(' [*] waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':

    try: 
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)