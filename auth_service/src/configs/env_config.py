'''Данные переменных окружения'''


from os import getenv
from dotenv import load_dotenv


load_dotenv()
DB_PATH = getenv('DB_PATH')
JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = getenv('JWT_ALGORITHM')
JWT_ACCESS_COOKIE_NAME = getenv('JWT_ACCESS_COOKIE_NAME')
DATABASE_LOGS_FILE = getenv('DATABASE_LOGS_FILE')
USERS_SERVICE_LOGS_FILE = getenv('USERS_SERVICE_LOGS_FILE')


def get_database_data():
    return {
        'path': DB_PATH
    }


def get_auth_data():
    return {
        'secret_key': JWT_SECRET_KEY, 
        'algorithm': JWT_ALGORITHM,
        'access_cookie_name': JWT_ACCESS_COOKIE_NAME
    }


def get_logs_data():
    return {
        'database_file_path': DATABASE_LOGS_FILE,
        'users_service_file_path': USERS_SERVICE_LOGS_FILE
    }