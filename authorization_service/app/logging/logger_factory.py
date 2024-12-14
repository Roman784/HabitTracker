'''Базовый класс для логирования'''


import logging
from os import getenv
from dotenv import load_dotenv


load_dotenv()
DATABASE_FILE_NAME = getenv('DATABASE_LOGS_FILE')
REPOSITORY_FILE_NAME = getenv('REPOSITORY_LOGS_FILE')


loggers = {}


def get_database_logger() -> logging.Logger:
    '''Возвращает логер для базы данных'''
    return create_logger('database', DATABASE_FILE_NAME)

def get_user_repository_logger() -> logging.Logger:
    '''Возвращает логер для репозитория пользователей'''
    return get_logger('user_repository', REPOSITORY_FILE_NAME)


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
