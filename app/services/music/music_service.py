from sqlalchemy.orm import Session
from app.models.music_model import MusicModel

def get_all_music(db: Session):
    return db.query(MusicModel).all()

def get_music_by_id(db: Session, music_id: str):
    return db.query(MusicModel).filter(MusicModel.music_id == music_id).first()