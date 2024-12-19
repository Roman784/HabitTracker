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


class MessageBrokerData:
    '''Константы данных для брокера сообщений'''
    HOST = getenv('MESSAGE_BROKER_HOST')
    PORT = int(getenv('MESSAGE_BROKER_PORT'))
    USER = getenv('MESSAGE_BROKER_USER')
    PASSWORD = getenv('MESSAGE_BROKER_PASSWORD')


class LogsData:
    '''Константы данных для логгирования'''
    DATABASE_FILE_PATH = getenv('DATABASE_LOGS_FILE')
    HABITS_SERVICE_FILE_PATH = getenv('HABITS_SERVICE_LOGS_FILE')
    MESSAGE_BROKER_FILE_PATH = getenv('MESSAGE_BROKER_LOGS_FILE')
