'''Данные переменных окружения'''


from os import getenv
from dotenv import load_dotenv


load_dotenv()


class DatabaseData:
    '''Константы данных для базы данных'''
    PATH = getenv('DB_PATH')


class AuthData:
    '''Константы данных для авторизации'''
    SECRET_KEY = getenv('JWT_SECRET_KEY')
    ALGORITHM = getenv('JWT_ALGORITHM')
    ACCESS_COOKIE_NAME = getenv('JWT_ACCESS_COOKIE_NAME')


class LogsData:
    '''Константы данных для логгирования'''
    DATABASE_FILE_PATH = getenv('DATABASE_LOGS_FILE')
    USERS_SERVICE_LOGS_FILE = getenv('USERS_SERVICE_LOGS_FILE')
