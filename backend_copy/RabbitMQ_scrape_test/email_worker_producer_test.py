import pika
import os
from dotenv import load_dotenv,find_dotenv
from simple_chalk import chalk
import json

load_dotenv(find_dotenv())

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')

#called from api - acts as producer - adds veh to queue as message
def add_email_to_queue(veh):

    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='EMAIL_QUEUE',durable=True)
    
    #serialize veh obj into json string
    body = json.dumps(veh)
    #then encode into byte string for body - body must be a byte string
    body = body.encode()

    channel.basic_publish(exchange='',
                        routing_key='EMAIL_QUEUE',
                        body=body, 
                        properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
                        )
    
    # print(chalk.green(f"VEH ADDED TO SCRAPE QUEUE: {veh}"))

if __name__ == "__main__":

    veh = {
        'year':0000,
        'make': 'Nissan',
        'model': 'Altima'
    }   

    email_and_veh ={
        'email':'balmanzar883@gmail.com',
        'veh': {
            'year':0000,
            'make': 'Nissan',
            'model': 'Altima'         
        }
    }
    add_email_to_queue(email_and_veh)