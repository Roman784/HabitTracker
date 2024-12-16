'''Логгер сервиса пользователей'''


from src.logging.base_logger import AbstractLogger


class UsersServiceLogger(AbstractLogger):
    '''Логгер сервиса пользователей'''
    def __init__(self):
        '''init'''
        module_name = 'user_service'
        file_path = 'logs/user_service.log'
        super().__init__(module_name, file_path)
