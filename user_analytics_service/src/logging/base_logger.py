'''Абстрактный логгер'''


from abc import ABC
import logging


class AbstractLogger(ABC):
    '''Абстрактный логгер, от которого наследуются логгеры для конкретных модулей'''
    __loggers = {}

    def __init__(self, module_name, file_path):
        '''init'''
        self.__module_name = module_name
        self.__file_path = file_path

    def create(self) -> logging.Logger:
        '''Создаёт логер'''
        logger = logging.getLogger(self.__module_name)
        logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(self.__file_path)
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        return logger

    def get_logger(self) -> logging.Logger:
        '''Возвращает логер, если его нет - создаёт'''
        if self.__module_name not in AbstractLogger.__loggers:
            AbstractLogger.__loggers[self.__module_name] = self.create()
        return AbstractLogger.__loggers[self.__module_name]
