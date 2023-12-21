from flask import Flask
from flask.json import jsonify

from .producer import produce_event


app = Flask(__name__)


@app.post('/event/<string:name>')
def create_event(name: str):
    produce_event(name)
    return jsonify(name=name)
