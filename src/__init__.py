import os

from dotenv import load_dotenv
from kafka_events import app

load_dotenv()

FLASK_PORT = os.environ.get("FLASK_PORT")
if not FLASK_PORT:
    raise OSError("FLASK_PORT is not set")


if __name__ == '__main__':
    app.run(port=FLASK_PORT)
