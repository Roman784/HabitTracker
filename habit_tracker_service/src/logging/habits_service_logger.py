'''Логгер сервиса по работе с привычками'''


from src.logging.base_logger import AbstractLogger
from src.configs.env_config import get_logs_data


logs_data = get_logs_data()


class HabitsServiceLogger(AbstractLogger):
    '''Логгер сервиса привычек'''
    def __init__(self):
        '''init'''
        module_name = 'habits_service'
        file_path = logs_data['habits_service_file_path']
        super().__init__(module_name, file_path)
