
import pika
import os,sys

def main():
    
    #Establish connection to broker server (RabbitMQ server instance)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    #Declare queue - cant assume queue prev declared - better to be safe
    channel.queue_declare(queue='hello')

    #callback func for when a message is rec'd
    def callback(ch,method,properties,body):
        print(f" [x] Recieved {body}")

    #define basic_consume process
    #listen for messages on 'hello' queue and pass msg to callback
    channel.basic_consume(queue='hello',
                          on_message_callback=callback)

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