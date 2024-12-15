'''Базовый класс для логирования'''


import logging
from app.configs.env_config import get_logs_data


logs_data = get_logs_data()


loggers = {}


def get_database_logger() -> logging.Logger:
    '''Возвращает логер для базы данных'''
    return create_logger('database', logs_data['database_file_name'])

def get_user_repository_logger() -> logging.Logger:
    '''Возвращает логер для репозитория пользователей'''
    return get_logger('user_repository', logs_data['repository_file_name'])


def get_logger(module_name, file_name) -> logging.Logger:
    '''
    Возвращает логер по имени файла
    Или создаёт новый, если такого нет
    '''
    if file_name in loggers:
        return loggers[file_name]
    
    logger = create_logger(module_name, file_name)
    loggers[file_name] = logger
    return logger

def create_logger(module_name, file_name) -> logging.Logger:
    '''Создаёт логер'''
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(file_name)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
