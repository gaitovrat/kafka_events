from .base import Base
from .engine import engine
from .event import Event, EventStatus

Base.metadata.create_all(engine)
