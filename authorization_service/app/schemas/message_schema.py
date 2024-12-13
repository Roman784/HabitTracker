'''Схема текстового ответа'''


from pydantic import BaseModel


class MessageResponse(BaseModel):
    '''Схема для текстового ответа'''
    message: str
