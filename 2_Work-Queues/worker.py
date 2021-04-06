import pika, sys, os, time

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) 
    channel = connection.channel() 

    channel.queue_declare(queue='task_queue', durable=True)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        # pretending we are busy by sleep
        time.sleep(body.count(b'.')) # every dot = 1s of work
        print(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_qos(prefetch_count=1) # fair dispatch - do not give more than one message to a worker at a time
    channel.basic_consume(  queue='task_queue', on_message_callback=callback) # manual ack turned on by default

    print(' [*] Waiting for messages. To exit press CTRL+C')
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