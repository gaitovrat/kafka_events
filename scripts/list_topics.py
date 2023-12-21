import os

from confluent_kafka.admin import AdminClient
from dotenv import load_dotenv


load_dotenv()

KAFKA_ADDRESS = os.environ.get('KAFKA_ADDRESS')
if not KAFKA_ADDRESS:
    raise OSError('KAFKA_ADDRESS is not set')

CONFIG = {'bootstrap.servers': KAFKA_ADDRESS}


def main():
    client = AdminClient(CONFIG)
    print(client.list_topics().topics)


if __name__ == '__main__':
    main()
