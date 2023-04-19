from __future__ import annotations

from dataclasses import dataclass

from shared.amqp_error import AmqpDefinitionBuilderError


@dataclass(frozen=True)
class AmqpQueue:
    name: str
    routing_keys: list[str]
    durable: bool


@dataclass(frozen=True)
class AmqpExchange:
    name: str
    queues: list[AmqpQueue]
    type: str
    durable: bool


@dataclass(frozen=True)
class AmqpChannel:
    number: int
    exchanges: list[AmqpExchange]


@dataclass(frozen=True)
class AmqpConnection:
    dsn: str
    channel: AmqpChannel | None = None


class AmqpDefinitionBuilder:
    def __init__(self):
        self._exchange_definitions: dict[str, AmqpExchange] = {}
        self._queue_definitions: dict[str, AmqpQueue] = {}
        self._exchange_definition_context: AmqpExchange | None = None
        # self._queue_context:

    def in_exchange(self, name: str):
        self._exchange_definitions[name] = AmqpExchange(name, [], 'direct', True)
        self._exchange_definition_context = self._exchange_definitions[name]

    def will_have_a_queue(self, name: str, routing_keys: list[str]) -> None:
        if self._exchange_definition_context is None:
            raise AmqpDefinitionBuilderError(f'Exchange context is missing, did you call in_exchange() method?')

        self._queue_definitions[name] = AmqpQueue(name, routing_keys, True)
        self._exchange_definition_context.queues.append(self._queue_definitions[name])

    @property
    def connection(self) -> AmqpConnection:
        channel = AmqpChannel(1, [])
        for exchange_name, exchange_definition in self._exchange_definitions.items():
            channel.exchanges.append(exchange_definition)

        connection: AmqpConnection = AmqpConnection(self._dsn, channel)
        return connection
