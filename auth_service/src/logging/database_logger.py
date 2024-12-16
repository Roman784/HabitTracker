'''Логгер базы данных'''


from src.logging.base_logger import AbstractLogger


class DatabaseLogger(AbstractLogger):
    '''Логгер базы данных'''
    def __init__(self):
        '''init'''
        module_name = 'database'
        file_path = 'logs/database.log'
        super().__init__(module_name, file_path)
