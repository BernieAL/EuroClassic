
import time
import pika
import os,sys,json
from simple_chalk import chalk


#get path to the directory containing app_main_runner.py relative to the current script
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app_main_runner_path = os.path.join(parent_dir)

# Add the directory to sys.path
if app_main_runner_path not in sys.path:
    sys.path.append(app_main_runner_path)

# Can now import app_main_runner.py as if it was in the same directory
import app_main_runner







def main():

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='VEH_QUEUE',durable=True)
    channel.queue_declare(queue='EMAIL_QUEUE',durable=True)

    def callback(ch,method,properties,body):
        

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
        # #decode body from byte string to string
        email_and_veh= body.decode('utf-8')
        # #parse string into json
        email_and_veh_data = json.loads(email_and_veh)
        print(email_and_veh_data)
        veh = email_and_veh_data['veh']
        
        #parse out veh obj - needed for scrape

        # #decode body from byte string to string
        # requested_veh = body.decode('utf-8')
        # #parse string into json
        # requested_veh_data = json.loads(requested_veh)

        print(chalk.blue(f"MSG REC'D"))
        print(chalk.green(f"SCRAPE NEEDED FOR -> VEH: {veh}"))
        ch.basic_ack(delivery_tag=method.delivery_tag)

        #PERFORM ENTIRE SCRAPE PROCESS USING Main_Runner
        # app_main_runner.main_runner(veh)

        #when complete
        print(chalk.green(f" SCRAPE COMPLETED - [x] Done"))  


        #encode email_and_veh into byte string for publishing


    

        print(chalk.green(f"SENDING NOTICE OF SCRAPE COMPLETION TO EMAIL_QUEUE")) 
        #publish message to EMAIL_QUEUE
        channel.basic_publish(exchange='',
                              routing_key='EMAIL_QUEUE',
                              body=email_and_veh,
                              properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))
        


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='VEH_QUEUE',on_message_callback=callback)

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