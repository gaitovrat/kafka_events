import os
import json

PATH = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    with open(f"{PATH}/config.json") as fd:
        config = json.load(fd)
    print(config)
