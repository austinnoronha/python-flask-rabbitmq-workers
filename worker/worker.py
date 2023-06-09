import pika
import os, json, datetime
from mongoengine import *

connect(
    db='test',
    host='mongodb',
    port=27017
)

# Iterate loop to read and print all environment variables
print("The keys and values of all environment variables:")
for key in os.environ:
    print(key, '=>', os.environ[key])
    
print(' Connecting to server ...')

class User(Document):
    name = StringField(max_length=300, required=True, primary_key=True)
    status = IntField(default=1)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
    meta = {
        'indexes': [
            '$name',  # text index
        ]
    }
    def to_json(self):
        return {"name": self.name}

connection = None   
try:
    RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
    RABBITMQ_USER = os.environ['RABBITMQ_USER']
    RABBITMQ_PASSWORD = os.environ['RABBITMQ_PASSWORD']
    RABBITMQ_PORT = os.environ['RABBITMQ_PORT']
    
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(RABBITMQ_HOST,
                                        RABBITMQ_PORT,
                                        '/',
                                        credentials)
    connection = pika.BlockingConnection(parameters)
        
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    print(' Waiting for messages...')


    def callback(ch, method, properties, body):
        username=body.decode()
        user_insert = User(name=username)
        user_insert.save()

        print(" Received username as %s" % username)
        print(" Done! ")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    channel.start_consuming()

except pika.exceptions.AMQPConnectionError as exc:
    print("Failed to connect to RabbitMQ service. Message wont be sent.", exc)
except Exception as e:
    print("Failed to connect to RabbitMQ service, common err", e)
