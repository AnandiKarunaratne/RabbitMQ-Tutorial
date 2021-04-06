# work queue - used to distribute time-consuming tasks among multiple workers
# main idea - avoid doing a resource-intensive task immediately and having to wait for it to complete
# encapsulate a task as a message and send it to the queue
# a worker process running in the background will pop the task and execute the job
# if there are many workers, tasks will be shared
# useful when its impossible to handle a complex task during a short http request window

import pika, sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) 
channel = connection.channel()

# 1. make sure queue will survive a rabbitmq node restart*
# must be done at the 1st time its declared, cannot be modified an already declared queue
channel.queue_declare(queue='task_queue', durable=True) 

# sending strings that stand for complex tasks
# number of dots in the string = complexity
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='', 
                        routing_key='task_queue', 
                        body=message, 
                        properties=pika.BasicProperties(
                            delivery_mode=2, # 2. make message persistent*
                        ))

print(" [x] Sent %r" % message)
connection.close()

# * both steps should be done for message durability