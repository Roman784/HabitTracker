'''Логгер базы данных'''


from src.logging.base_logger import AbstractLogger
from src.configs.env_config import get_logs_data


logs_data = get_logs_data()


class DatabaseLogger(AbstractLogger):
    '''Логгер базы данных'''
    def __init__(self):
        '''init'''
        module_name = 'database'
        file_path = logs_data['database_file_path']
        super().__init__(module_name, file_path)
