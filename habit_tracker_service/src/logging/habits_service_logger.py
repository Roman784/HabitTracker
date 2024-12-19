'''Логгер сервиса по работе с привычками'''


from src.logging.base_logger import AbstractLogger
from src.configs.env_config import LogsData


class HabitsServiceLogger(AbstractLogger):
    '''Логгер сервиса привычек'''
    def __init__(self):
        '''init'''
        module_name = 'habits_service'
        file_path = LogsData.HABITS_SERVICE_FILE_PATH
        super().__init__(module_name, file_path)
