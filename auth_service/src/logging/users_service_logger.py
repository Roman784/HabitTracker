'''Логгер сервиса пользователей'''


from src.logging.base_logger import AbstractLogger
from src.configs.env_config import get_logs_data


logs_data = get_logs_data()


class UsersServiceLogger(AbstractLogger):
    '''Логгер сервиса пользователей'''
    def __init__(self):
        '''init'''
        module_name = 'user_service'
        file_path = logs_data['users_service_file_path']
        super().__init__(module_name, file_path)
