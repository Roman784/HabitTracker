

from aio_pika import IncomingMessage
from json import loads

from src.api.dependencies import message_broker, habits_service


async def on_habits_activity(message: IncomingMessage):
    async with message.process():
        user_id = loads(message.body)['user_id']
        service = habits_service()
        habits = await service.get_all(user_id)
        habits_response = [row.to_read_model().model_dump() for row in habits]
        broker = message_broker()
        await broker.connect()
        await broker.send_message(message.reply_to, {'habits': habits_response})
        await broker.close()
    