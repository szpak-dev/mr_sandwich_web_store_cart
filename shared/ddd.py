from abc import ABC, abstractmethod
from typing import List


class BaseRepository(ABC):
    pass


class DomainError(Exception):
    pass


class DomainEvent(ABC):
    def __init__(self, full_name):
        self._bc, self._aggregate, self._name = full_name.split('.')

    def bounded_context(self) -> str:
        return self._bc

    def aggregate(self) -> str:
        return self._aggregate

    def name(self) -> str:
        return self._name

    @abstractmethod
    def serialize(self) -> str:
        pass


class AggregateRoot:
    _events: List[DomainEvent] = []

    def _emit_event(self, event: DomainEvent) -> None:
        self._events.append(event)

    def release_events(self) -> List[DomainEvent]:
        events = self._events
        self._events = []
        return events


class ValueObject(ABC):
    @abstractmethod
    def value(self):
        pass
