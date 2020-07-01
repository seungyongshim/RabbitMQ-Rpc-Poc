import sys
import pika
import os
import json
import logging.config

class InferenceExecutor(object):

    def __init__(self, queueKey):
        self.queueKey = queueKey

    def send_ready(self, hostname, vhost, username, password):
        credentials = pika.PlainCredentials(username, password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, credentials=credentials, virtual_host=vhost))
        channel = connection.channel()
        channel.queue_declare(queue=self.queueKey, durable=True, exclusive=False, auto_delete=True, arguments=None)
        channel.basic_publish(exchange='', routing_key=self.queueKey, body='connect')

    def start_consumer(self, hostname, vhost, username, password):
        credentials = pika.PlainCredentials(username, password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, credentials=credentials, virtual_host=vhost))
        channel = connection.channel()
        channel.queue_declare(queue='rpc_queue_hello')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='rpc_queue_hello', on_message_callback=self.on_request)
        channel.start_consuming()

    def on_request(self, ch, method, props, body):
        msg = str(body, 'utf-8')
        response = "World"
        ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = props.correlation_id),
                        body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        

if __name__ == '__main__':
    hostname = '192.168.100.76'
    vhost = '/'
    username = 'mirero'
    password = 'system'

    pid = os.getpid()
    queueKey = str(pid)
    inferenceExecutor = InferenceExecutor(queueKey)
    inferenceExecutor.start_consumer(hostname, vhost, username, password)