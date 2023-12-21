import asyncio
import os

from confluent_kafka import Consumer
from dotenv import load_dotenv
from kafka_events.db import Event, EventStatus

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
MAX_TASKS = 10


async def start(body: dict):
    print(body)
    event_id = body["event_id"]
    event = Event.update(event_id, EventStatus.IN_PROGRESS)
    print(event)

    asyncio.sleep(body["sleep"])

    event = Event.update(event_id, EventStatus.COMPLETED)
    print(event)


async def main():
    topic = "example"
    consumer = Consumer(CONFIG)
    tasks = []

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
            task = asyncio.create_task(start(msg.value().decode('utf-8')))
            tasks.append(task)

        if len(tasks) == MAX_TASKS:
            await asyncio.wait(tasks)

if __name__ == '__main__':
    asyncio.run(main())
