from enum import Enum
from typing import Optional
from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column, Session

from .engine import session
from .base import Base


class EventStatus(Enum):
    QUEUED = 'Queued'
    IN_PROGRESS = 'InProgress'
    COMPLETED = 'Completed'


class Event(Base):
    __tablename__ = 'event'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f'Event(id={self.id!r}, name={self.name!r}, status={self.status!r})'

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status
        }

    @staticmethod
    def all() -> list['Event']:
        statement = select(Event)
        return session.execute(statement).scalars().all()

    @staticmethod
    def by_id(event_id: int) -> Optional['Event']:
        statement = select(Event).where(Event.id == event_id)
        return session.execute(statement).scalar()

    @staticmethod
    def create(name: str) -> Optional['Event']:
        event = Event(name=name, status=EventStatus.QUEUED.value)
        try:
            session.add(event)
            session.commit()
            return event
        except Exception:
            session.rollback()
            return None

    @staticmethod
    def update(event_id: int, status: EventStatus) -> Optional['Event']:
        statement = select(Event).where(Event.id == event_id)
        event = session.execute(statement).scalar()
        if not event:
            return None

        event.status = status.value
        try:
            session.commit()
            return event
        except Exception:
            session.rollback()
            return None
