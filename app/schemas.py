from pydantic import BaseModel, PositiveInt
from typing import Optional


class Message(BaseModel):
    MessageID: PositiveInt
    Message: Optional[str]
    Views: Optional[int]

    class Config:
        orm_mode = True


class ReturnedMessage(BaseModel):
    MessageID: PositiveInt
    Message: Optional[str]
    Views: Optional[int]

    class Config:
        orm_mode = True


class PostMessage(BaseModel):
    Message: Optional[str]

    class Config:
        orm_mode = True


class UpdatedMessage(BaseModel):
    Message: Optional[str]

    class Config:
        orm_mode = True
