import os
import json
from random import randint

from confluent_kafka import Producer
from dotenv import load_dotenv


load_dotenv()

KAFKA_ADDRESS = os.environ.get('KAFKA_ADDRESS')
if not KAFKA_ADDRESS:
    raise OSError('KAFKA_ADDRESS is not set')

CONFIG = {
    'bootstrap.servers': KAFKA_ADDRESS,
    'client.id': 'kafka-events-producer'
}

producer = Producer(CONFIG)


def produce_event(name: str):
    data = {
        'sleep': randint(1, 10)
    }

    producer.produce(name, key='function', value=json.dumps(data))
    producer.flush()
