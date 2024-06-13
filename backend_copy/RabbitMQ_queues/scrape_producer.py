import pika
import os,sys
from dotenv import load_dotenv,find_dotenv
from simple_chalk import chalk
import json

#load_dotenv(find_dotenv())
# RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
# RABBIT_MQ_HOST = 'rbmq_service'

#get parent dir 'backend_copy' from current script dir - append to sys.path to be searched for modules we import
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the directory to sys.path
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from config import DB_URI,RABBITMQ_HOST




#called from api - acts as producer - adds veh to queue as message
def add_veh_to_queue(email_and_veh):

    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST,'rbmq'))
    channel = connection.channel()

    channel.queue_declare(queue='VEH_QUEUE',durable=True)
    
    #serialize veh obj into json string
    body = json.dumps(email_and_veh)
    #then encode into byte string for body - body must be a byte string
    body = body.encode()

    channel.basic_publish(exchange='',
                        routing_key='VEH_QUEUE',
                        body=body, 
                        properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
                        )
    
    print(chalk.green(f"(scrape_producer)VEH ADDED TO SCRAPE QUEUE: {email_and_veh['veh']}"))
    

if __name__ == "__main__":

    email_and_veh = {
                'email':'balmanzar883@gmail.com',
                'veh': {
                    'year':0000,
                    'make': 'Nissan',
                    'model': 'Altima'         
                }
    }   

    add_veh_to_queue(email_and_veh)