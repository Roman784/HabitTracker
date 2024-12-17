

from aio_pika import IncomingMessage
from json import loads

from src.api.dependencies import message_broker, habits_service


async def on_habits_activity(message: IncomingMessage):
    async with message.process():
        user_id = loads(message.body)['user_id']
        service = habits_service()
        activities = await service.get_all_activity(user_id)

        broker = message_broker()
        await broker.connect()
        await broker.send_message(message.reply_to, {'activities': activities})
        await broker.close()
    