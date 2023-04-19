from abc import ABC, abstractmethod
from typing import Any


class AmqpConsumerAdapter(ABC):
    @abstractmethod
    async def connect(self) -> list[Any]:
        ...

    @abstractmethod
    async def consume(self, queues: list[Any], callback: callable):
        ...


class AmqpConsumer:
    def __init__(self, dsn: str):
        self._dsn = dsn

