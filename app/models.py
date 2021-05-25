from sqlalchemy import Column, SmallInteger, String
from .database import Base


class Message(Base):
    __tablename__ = "messages"

    MessageID = Column(SmallInteger, primary_key=True)
    Message = Column(String(160), nullable=False)
    Views = Column(SmallInteger, default=0)
