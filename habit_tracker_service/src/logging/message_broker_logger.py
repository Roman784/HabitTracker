'''Логгер брокера сообщений'''


from src.logging.base_logger import AbstractLogger
from src.configs.env_config import get_logs_data


logs_data = get_logs_data()


class MessageBrokerLogger(AbstractLogger):
    '''Логгер брокера сообщений'''
    def __init__(self):
        '''init'''
        module_name = 'message_broker'
        file_path = logs_data['message_broker_file_path']
        super().__init__(module_name, file_path)
