from flask import Flask, Response, abort
from flask.json import jsonify

from .producer import produce_event
from .db import Event, EventStatus


app = Flask(__name__)


@app.post('/event')
def create_event() -> Response:
    event = produce_event()
    if not event:
        abort(500)

    return jsonify(response=event.to_dict())


@app.get('/event')
def get_events() -> Response:
    events = Event.all()
    return jsonify(response=[event.to_dict() for event in events])


@app.get('/event/<int:event_id>')
def get_event(event_id: int) -> Response:
    event = Event.by_id(event_id)
    if not event:
        abort(404)

    return jsonify(response=event.to_dict())


@app.put('/event/<int:event_id>/<string:status_name>')
def update_event(event_id: int, status_name: str) -> Response:
    statuses = list(EventStatus)
    statuses = [status for status in statuses if status.name == status_name]
    if not statuses:
        abort(400)

    event = Event.update(event_id, statuses[0])
    if not event:
        abort(404)

    return jsonify(response=event.to_dict())
