import asyncio
from typing import Optional

from aio_pika import connect, ExchangeType
from aio_pika.abc import AbstractIncomingMessage
from aio_pika.abc import AbstractQueue
from aio_pika.abc import AbstractExchange
from aio_pika.abc import AbstractChannel
from aio_pika.abc import AbstractConnection

from shared.amqp_definition import AmqpConnection, AmqpExchange, AmqpQueue
from shared.amqp_pack_consumer import AmqpConsumerAdapter


class AioPikaAsyncConsumer(AmqpConsumerAdapter):
    def __init__(self, connection: AmqpConnection):
        self._connection = connection

    async def connect(self) -> list[AbstractQueue]:
        async def create_connection() -> AbstractConnection:
            connection = await connect(self._connection.dsn)
            return connection

        async def create_channel(amqp_connection: AbstractConnection) -> AbstractChannel:
            amqp_channel = await amqp_connection.channel()
            await amqp_channel.set_qos(prefetch_count=1)
            return amqp_channel

        async def create_queues(channel: AbstractChannel) -> list[AbstractQueue]:
            exchanges: list[AbstractExchange] = []
            queues: list[AbstractQueue] = []

            exchange_definition: AmqpExchange
            for exchange_definition in self._connection.channel.exchanges:
                exchange: AbstractExchange = await channel.declare_exchange(
                    name=exchange_definition.name,
                    type=exchange_definition.type,
                    durable=exchange_definition.durable
                )

                exchanges.append(exchange)

                query_definition: AmqpQueue
                for query_definition in exchange_definition.queues:
                    queue: AbstractQueue = await channel.declare_queue(
                        name=query_definition.name,
                        durable=query_definition.durable,
                    )

                    for key in query_definition.routing_keys:
                        await queue.bind(exchange=exchange, routing_key=key)

                    queues.append(queue)

            return queues

        aio_pika_connection = await create_connection()
        aio_pika_channel = await create_channel(aio_pika_connection)
        aio_pika_queues = await create_queues(aio_pika_channel)
        return aio_pika_queues

    async def consume(self, aio_pika_queues: list[AbstractQueue], cb) -> None:
        for queue in aio_pika_queues:
            async with queue.iterator() as iterator:
                message: AbstractIncomingMessage
                async for message in iterator:
                    await cb(message)

            await asyncio.Future()


class AioPikaManager:
    def __init__(self, dsn: str):
        self._dsn = dsn

    async def create_connection(self) -> AbstractConnection:
        connection = await connect(self._dsn)
        return connection

    async def create_channel(self, connection: AbstractConnection, number: Optional[int]) -> AbstractChannel:
        amqp_channel = await connection.channel(number)
        await amqp_channel.set_qos(prefetch_count=1)
        return amqp_channel

    async def create_exchange(self, channel: AbstractChannel):