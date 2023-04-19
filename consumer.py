import asyncio
from json import loads

from aio_pika.abc import AbstractIncomingMessage

from shared.amqp_pack_adapter import AioPikaAsyncConsumer
from shared.amqp_pack_consumer import AmqpConsumerAdapter
from shared.config import settings


async def main():
    async def process_message(message: AbstractIncomingMessage) -> None:
        async with message.process(requeue=True):
            dish_id = loads(message.body)[0]
            operation_type = message.routing_key
            print(dish_id, operation_type)

    amqp = AmqpConsumer(settings['RABBITMQ_DSN'])
    amqp.in_exchange('food_factory')
    amqp.will_have_a_queue('dishes', ['dish_created', 'dish_updated', 'dish_removed'])

    amqp.in_exchange('auth')
    amqp.will_have_a_queue('users', ['user_promoted', 'user_demoted'])
    amqp.will_have_a_queue('authentications', ['success', 'failed'])

    aio_pika: AmqpConsumerAdapter = AioPikaAsyncConsumer(amqp.connection)
    aio_pika_queues = await aio_pika.connect()
    await aio_pika.consume(aio_pika_queues, process_message)


if __name__ == "__main__":
    asyncio.run(main())
