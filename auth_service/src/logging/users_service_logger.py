'''Логгер сервиса пользователей'''


from src.logging.base_logger import AbstractLogger
from src.configs.env_config import LogsData


class UsersServiceLogger(AbstractLogger):
    '''Логгер сервиса пользователей'''
    def __init__(self):
        '''init'''
        module_name = 'user_service'
        file_path = LogsData.USERS_SERVICE_LOGS_FILE
        super().__init__(module_name, file_path)
