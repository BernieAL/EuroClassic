
import time
import pika
import os,sys,json
from simple_chalk import chalk


# Calculate the path to the directory containing app_main_runner.py relative to the current script
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app_main_runner_path = os.path.join(parent_dir)

# Add the directory to sys.path
if app_main_runner_path not in sys.path:
    sys.path.append(app_main_runner_path)

# Now you can import app_main_runner.py as if it was in the same directory
import app_main_runner

def main():

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='VEH_QUEUE',durable=True)

    def callback(ch,method,properties,body):

        #decode body from byte string to string
        message = body.decode('utf-8')
        #parse string into json
        message_data = json.loads(body)

        print(chalk.blue(f"MSG REC'D"))
        print(chalk.green(f"SCRAPE NEEDED FOR -> VEH: {body}"))
        ch.basic_ack(delivery_tag=method.delivery_tag)

        
        
        #PERFORM ENTIRE SCRAPE PROCESS USING Main_Runner
        app_main_runner.main_runner(message_data)

        #when complete
        print(chalk.green(f" SCRAPE COMPLETED - [x] Done"))  

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='VEH_QUEUE',on_message_callback=callback)

    #listen indefinitley for messages
    print(' [*] waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':

   main()
    # try: 
    #     main()
    # except KeyboardInterrupt:
    #     print('Interrupted')
    #     try:
    #         sys.exit(0)
    #     except SystemExit:
    #         os._exit(0)