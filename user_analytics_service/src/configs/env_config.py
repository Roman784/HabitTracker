'''Данные переменных окружения'''


from os import getenv
from dotenv import load_dotenv


load_dotenv()

JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = getenv('JWT_ALGORITHM')
JWT_ACCESS_COOKIE_NAME = getenv('JWT_ACCESS_COOKIE_NAME')

MESSAGE_BROKER_HOST = getenv('MESSAGE_BROKER_HOST')
MESSAGE_BROKER_PORT = getenv('MESSAGE_BROKER_PORT')
MESSAGE_BROKER_USER = getenv('MESSAGE_BROKER_USER')
MESSAGE_BROKER_PASSWORD = getenv('MESSAGE_BROKER_PASSWORD')

MESSAGE_BROKER_FILE = getenv('MESSAGE_BROKER_FILE')


def get_auth_data():
    return {
        'secret_key': JWT_SECRET_KEY,
        'algorithm': JWT_ALGORITHM,
        'access_cookie_name': JWT_ACCESS_COOKIE_NAME
    }


def get_message_broker_data():
    return {
        'host': MESSAGE_BROKER_HOST,
        'port': int(MESSAGE_BROKER_PORT),
        'user': MESSAGE_BROKER_USER,
        'password': MESSAGE_BROKER_PASSWORD
    }


def get_logs_data():
    return {
        'message_broker_file_path': MESSAGE_BROKER_FILE
    }