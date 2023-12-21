import asyncio
import aiohttp
import os
import json

from confluent_kafka import Consumer
from dotenv import load_dotenv
from kafka_events.db import EventStatus

load_dotenv()

KAFKA_ADDRESS = os.environ.get('KAFKA_ADDRESS')
if not KAFKA_ADDRESS:
    raise OSError('KAFKA_ADDRESS is not set')
FLASK_PORT = os.environ.get('FLASK_PORT')
if not FLASK_PORT:
    raise OSError('FLASK_PORT is not set')

PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG = {
    'bootstrap.servers': KAFKA_ADDRESS,
    'group.id': 'kafka-events-consumer',
    'auto.offset.reset': 'earliest'
}
HOST = f'http://127.0.0.1:{FLASK_PORT}'

tasks = []


async def start(body: dict):
    print(body)
    event_id = body['event_id']

    async with aiohttp.ClientSession() as session:
        async with session.put(f'{HOST}/event/{event_id}/{EventStatus.IN_PROGRESS.value}') as response:
            print(await response.json())

        await asyncio.sleep(body['sleep'])

        async with session.put(f'{HOST}/event/{event_id}/{EventStatus.COMPLETED.value}') as response:
            print(await response.json())


async def consume():
    while True:
        if tasks:
            await asyncio.wait(tasks)

        await asyncio.sleep(1)


async def produce():
    topic = 'example'
    consumer = Consumer(CONFIG)
    tasks = []

    consumer.subscribe([topic])
    print(f'Subscribed on topic "{topic}"')

    while True:
        msg = consumer.poll(1)
        print(msg)

        if not msg:
            await asyncio.sleep(1)
            continue

        error = msg.error()
        if error:
            print(error)
        else:
            body = msg.value().decode('utf-8')
            task = asyncio.create_task(start(json.loads(body)))
            tasks.append(task)

        await asyncio.sleep(1)


async def main():
    task1 = asyncio.create_task(produce())
    task2 = asyncio.create_task(consume())
    await asyncio.gather(task1, task2)

if __name__ == '__main__':
    asyncio.run(main())
