'''Логгер брокера сообщений'''


from src.logging.base_logger import AbstractLogger
from src.configs.env_config import LogsData


class MessageBrokerLogger(AbstractLogger):
    '''Логгер брокера сообщений'''
    def __init__(self):
        '''init'''
        module_name = 'message_broker'
        file_path = LogsData.MESSAGE_BROKER_FILE
        super().__init__(module_name, file_path)
