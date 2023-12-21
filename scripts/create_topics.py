import os
from sys import argv
from confluent_kafka.admin import AdminClient, NewTopic

from dotenv import load_dotenv


load_dotenv()

KAFKA_ADDRESS = os.environ.get('KAFKA_ADDRESS')
if not KAFKA_ADDRESS:
    raise OSError('KAFKA_ADDRESS is not set')

CONFIG = {'bootstrap.servers': KAFKA_ADDRESS}
PARTITIONS_COUNT = 3
REPLICATION_COUNT = 1


def main():
    if len(argv) < 2:
        print('No topic specified')
        return

    client = AdminClient(CONFIG)
    topic_names = argv[1:]
    topics = [NewTopic(
        topic=topic_name,
        num_partitions=PARTITIONS_COUNT,
        replication_factor=REPLICATION_COUNT
    ) for topic_name in topic_names]

    topics = client.create_topics(topics)
    for topic in topics.keys():
        print(topic)


if __name__ == '__main__':
    main()
