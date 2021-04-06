import pika

# establish a connection with rabbitmq server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) 
channel = connection.channel() 
# connected to a broker on the local machine

# make sure the recipient queue exists
# create a hello queue to which the message will be delivered
channel.queue_declare(queue='hello')
# ready to send a message

# cannot directly send a message to the queue, need to go through an exchange
# exchange allows to specify exacly to which queue the message should go
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")

# before exiting make sure the network buffers were flushed and message was delivered to rabbitmq
connection.close()