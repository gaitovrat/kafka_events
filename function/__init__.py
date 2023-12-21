import os
import json

from confluent_kafka import Consumer, KafkaError
from dotenv import load_dotenv


load_dotenv()

KAFKA_ADDRESS = os.environ.get('KAFKA_ADDRESS')
if not KAFKA_ADDRESS:
    raise OSError('KAFKA_ADDRESS is not set')

PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG = {
    'bootstrap.servers': KAFKA_ADDRESS,
    'group.id': 'kafka-events-consumer',
    'auto.offset.reset': 'earliest'
}


def start(event: dict):
    print(event)


def main():
    with open(f"{PATH}/config.json") as fd:
        config = json.load(fd)
    if 'topic' not in config:
        raise ValueError('Topic is not specified in config.json')

    topic = config['topic']
    consumer = Consumer(CONFIG)

    consumer.subscribe([topic])
    print(f'Subscribed on topic "{topic}"')

    while True:
        msg = consumer.poll(1.0)

        if not msg:
            continue

        error = msg.error()
        if error:
            print(error)
        else:
            start(msg.value().decode('utf-8'))


if __name__ == '__main__':
    main()
