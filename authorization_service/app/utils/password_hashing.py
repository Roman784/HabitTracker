'''Хеширует и проверяет пароль на совпадение'''


from passlib.hash import pbkdf2_sha256
from app.logging.logger_factory import get_user_repository_logger


logger = get_user_repository_logger()


def hash_password(password: str) -> str:
    '''Хеширует пароль'''
    logger.debug("Password hashing")
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    '''Проверяет совпадение пароля с хешем'''
    logger.debug("Password verifying")
    return pbkdf2_sha256.verify(password, hashed_password)
