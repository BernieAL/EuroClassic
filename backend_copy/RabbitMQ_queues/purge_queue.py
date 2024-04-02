import pika



def purge_all_from_queue(queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_purge(queue)

    connection.close()

if __name__ == "__main__":

    purge_all_from_queue('VEH_QUEUE')
    purge_all_from_queue('EMAIL_QUEUE')