import os
import json
from random import randint

from confluent_kafka import Producer
from dotenv import load_dotenv

from .db import Event

load_dotenv()

KAFKA_ADDRESS = os.environ.get('KAFKA_ADDRESS')
if not KAFKA_ADDRESS:
    raise OSError('KAFKA_ADDRESS is not set')

CONFIG = {
    'bootstrap.servers': KAFKA_ADDRESS,
    'client.id': 'kafka-events-producer'
}

producer = Producer(CONFIG)


def produce_event() -> Event | None:
    event = Event.create('function')
    if not event:
        return None

    data = {
        'event_id': event.id,
        'sleep': randint(1, 10)
    }

    producer.produce('example', key='function', value=json.dumps(data))
    producer.flush()

    return event
