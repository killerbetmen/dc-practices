from sqlalchemy.orm import Session
from . import models


def get_messages(db: Session):
    return db.query(models.Message).all()


def get_message(db: Session, message_id: int):
    return (
        db.query(models.Message).filter(models.Message.MessageID == message_id).first()
    )
