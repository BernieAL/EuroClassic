
import time
import pika
import os,sys
from simple_chalk import chalk
from backend_copy.app_main_runner import main_runner

def main():

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='veh_queue',durable=True)

    def callback(ch,method,properties,body):
        print(chalk.green(f"MSG REC'D"))
        print(chalk.green(f"SCRAPE NEEDED FOR -> VEH: {body}"))
        ch.basic_ack(delivery_tag=method.delivery_tag)



        #PERFORM ENTIRE SCRAPE PROCESS USING Main_Runner
        
        #when complete
        print(chalk.green(" [x] Done"))  

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue',on_message_callback=callback)

    #listen indefinitley for messages
    print(' [*] waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':

    main_runner()

    try: 
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)