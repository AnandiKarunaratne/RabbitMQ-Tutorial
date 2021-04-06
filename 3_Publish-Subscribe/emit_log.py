# deliver a message to multiple consumers = publish/subscribe

# emit log messages

# exchange = receives messages from producer and pushes them to queues

import pika, sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) 
channel = connection.channel()

channel.exchange_declare(   exchange='logs', # name of the exchange 
                            exchange_type='fanout') # direct, topic, headers, fanout = broadcast all messages

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

# publish the named exchange
channel.basic_publish(exchange='logs', routing_key='', body=message)

print(" [x] Sent %r" % message)
connection.close()