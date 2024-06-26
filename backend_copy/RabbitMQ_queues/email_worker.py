import time
import pika
import os,sys,json
from simple_chalk import chalk


from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())


#get parent dir'backend_copy' from current script dir - append to sys.path to be searched for modules we import
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if parent_dir not in sys.path:
    sys.path.append(parent_dir)


from Email_Logic.email_sender import send_email


"""
Recieves obj of email and veh
   email_and_veh = {
                'email':'<some-email>@gmail.com',
                'veh': {
                    'year':0000,
                    'make': 'Nissan',
                    'model': 'Altima'         
                }
    }
Calls send_mail function and passes email to it to be sent off to
"""

def main():

    connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_HOST','rbmq')))
    # connection = pika.BlockingConnection(pika.ConnectionParameters('172.29.0.4'))

    channel = connection.channel()

    channel.queue_declare(queue='EMAIL_QUEUE',durable=True)

    def callback(ch,method,properties,body):

        #decode body from byte string to string
        email_and_veh = body.decode('utf-8')
        #parse string into json

        """EMAIL_AND_VEH JSON OBJ STRUCTURE

            email_and_veh = {
                'email':'balmanzar883@gmail.com',
                'veh': {
                    'year':0000,
                    'make': 'Nissan',
                    'model': 'Altima'         
                }
            }
        """
        email_and_veh = json.loads(email_and_veh)
        email = email_and_veh['email']
        veh = email_and_veh['veh']
        # model = veh['model']
    
        print(chalk.blue(f"MSG REC'D {email_and_veh}"))
        print(chalk.green(f"SENDING EMAIL.."))
        
        send_email(email,veh)

        ch.basic_ack(delivery_tag=method.delivery_tag)

        #when complete
        print(chalk.green(f"EMAIL SENT")) 

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='EMAIL_QUEUE',on_message_callback=callback)

    #listen indefinitley for messages
    print(chalk.blue('[*] waiting for messages. To exit press CTRL+C'))
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