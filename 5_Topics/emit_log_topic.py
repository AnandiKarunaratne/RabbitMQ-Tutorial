# direct cannot do routing based on multiple criteria
# ex: subscribe based on severity and source emmitted

# topics can not have arbitrary routing keys - must be list of words delimited by dots
# * = substitue for exactly one word
# # = substitute for zero or more words
# queue is bound with # = receives all messages

# <facility>.<severity>

import pika, sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) 
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)

print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()