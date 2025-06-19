from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from app.database.database import SessionLocal, engine
from datetime import datetime

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/user/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        id=user.id,
        display_name=user.display_name,
        email=user.email,
        email_verified=user.email_verified,
        provider_id=user.provider_id,
        creation_time=user.creation_time
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"success": True, "user": db_user.id}