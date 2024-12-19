'''Логгер базы данных'''


from src.logging.base_logger import AbstractLogger
from src.configs.env_config import LogsData


class DatabaseLogger(AbstractLogger):
    '''Логгер базы данных'''
    def __init__(self):
        '''init'''
        module_name = 'database'
        file_path = LogsData.DATABASE_FILE_PATH
        super().__init__(module_name, file_path)
