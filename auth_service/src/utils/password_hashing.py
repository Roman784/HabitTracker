'''Хеширует и проверяет пароль на совпадение'''


from passlib.hash import pbkdf2_sha256


def hash_password(password: str) -> str:
    '''Хеширует пароль'''
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    '''Проверяет совпадение пароля с хешем'''
    return pbkdf2_sha256.verify(password, hashed_password)
