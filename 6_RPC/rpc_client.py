# remote procedure call

# work queues = distribute time consuming tasks among multiple workers
# rpc = run a function on a remote computer and wait for the result

import pika, uuid

class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume( # subscribe to the callback_queue
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    # executed on every response - checks if the correlation id is the one we are looking for, if so save the response
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id: # corr_id is unique to each request
            self.response = body

    # to receive response, client needs to send a 'callback' queue address with the request
    # callback queue for each request => inefficient
    # callback queue per client => more efficient
    # correlation_id = set a unique value for each request, and match a response with a request
    
    def call(self, n): # does the actual rpc request
        self.response = None
        self.corr_id = str(uuid.uuid4()) # create newe correlation id
        self.channel.basic_publish( # publish request message with 2 properties reply to and corr id
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)
        

fibonacci_rpc = FibonacciRpcClient()
print(" [x] Requesting fib(30)")
result = fibonacci_rpc.call(30) # call = sends an rpc request and blocks until the answer is received
print(" [.] Got %r" % result)





