from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, status, Depends, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from . import crud, models, schemas
import os


models.Base.metadata.create_all(bind=engine)


app = FastAPI()
username = os.getenv('USER')
password = os.getenv('PASSWORD')
security = HTTPBasic()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def root():
    return {'message': 'Hello DaftCode'}


def auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_user = secrets.compare_digest(credentials.username, username)
    correct_pass = secrets.compare_digest(credentials.password, password)
    if not (correct_user and correct_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect credentials',
            headers={'WWW-Authenticate': 'Basic'}
        )

    return credentials.username


@app.get('/users/me')
async def current_user(username: str = Depends(auth)):
    return {'username': username}


@app.get("/messages")
async def messages_list(db: Session = Depends(get_db)):
    return crud.get_messages(db=db)


@app.get("/messages/{message_id}")
async def message_detail(message_id: int, db: Session = Depends(get_db)):
    message = db.query(models.Message).get(message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message does not exist")
    message.Views += 1
    db.flush()
    db.commit()
    db.refresh(message)
    return {"message": message}


@app.post("/add_message", status_code=201, response_model=schemas.ReturnedMessage)
async def create_message(new_message: schemas.PostMessage,
                         db: Session = Depends(get_db),
                         username: str = Depends(auth)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        last_message = db.query(models.Message).order_by(models.Message.MessageID.desc()).first()

        new_message = models.Message(**new_message.dict())
        new_message.MessageID = last_message.MessageID + 1
        content = new_message.Message.isspace()
        if content is True or new_message.Message == '':
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail='Message is empty'
            )
        else:
            db.add(new_message)
            db.flush()
            db.commit()
    return new_message


@app.put("/update_message/{message_id}", status_code=status.HTTP_200_OK, response_model=schemas.ReturnedMessage)
async def update_message(message_id: int,
                         update_message: schemas.UpdatedMessage,
                         db: Session = Depends(get_db),
                         username: str = Depends(auth)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        if not message_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ID not provided."
            )

        to_update = db.query(models.Message).get(message_id)
        to_update.Views = 0
        if not to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ID not provided."
            )
        # if v is not None -> Parameters are Optional
        up_dict = {k: v for k, v in update_message.dict().items() if v is not None}

        if up_dict:
            is_updated = (db.query(models.Message)
                          .filter(models.Message.MessageID == message_id)
                          .update(up_dict, synchronize_session="fetch"))

        content = to_update.Message.isspace()
        if content is True or to_update.Message == '':
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail='Message is empty'
            )
        else:
            db.flush()
            db.commit()
            db.refresh(to_update)

        return to_update


@app.delete("/delete_message/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(message_id: int,
                         db: Session = Depends(get_db),
                         username: str = Depends(auth)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        if not message_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ID not provided."
            )

        to_delete = db.query(models.Message).get(message_id)
        if not to_delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ID not provided."
            )

        db.delete(to_delete)
        db.flush()
        db.commit()

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )
