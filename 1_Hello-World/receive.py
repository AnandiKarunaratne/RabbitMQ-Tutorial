import pika, sys, os

def main():
    # establish a connection with rabbitmq server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) 
    channel = connection.channel() 
    # connected to a broker on the local machine

    # make sure the queue exists
    channel.queue_declare(queue='hello')
    # we have already declared it in send.py,, but we dont know which will run first, so better to do this

    # receiving by callback
    # when we receive a message, callback function is called by pika
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    # tell rabbitmq that callback function should receive messages from hello queue
    channel.basic_consume(  queue='hello',
                            auto_ack=True,
                            on_message_callback=callback)
    # for this to be success, the queue should exist

    # we enter a never ending loop that waits for data and runs callbacks whenever necessary
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