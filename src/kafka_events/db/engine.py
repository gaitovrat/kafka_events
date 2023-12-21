from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///kafka_events.db", echo=True)
session = Session(engine)
