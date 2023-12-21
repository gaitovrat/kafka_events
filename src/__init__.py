import os

from dotenv import load_dotenv
from flask import Flask
from flask.json import jsonify


load_dotenv()

FLASK_PORT = os.environ.get("FLASK_PORT")
if not FLASK_PORT:
    raise OSError("FLASK_PORT is not set")

app = Flask(__name__)


@app.post('/event/<string:name>')
def create_event(name: str):
    return jsonify(name=name)


if __name__ == '__main__':
    app.run(port=FLASK_PORT)
