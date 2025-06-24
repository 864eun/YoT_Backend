from sqlalchemy.orm import Session
from app.models.music_model import MusicModel
from app.schemas.music_schema import Music
from datetime import datetime

def get_all_music(db: Session):
    return db.query(MusicModel).all()

def get_music_by_id(db: Session, music_id: str):
    return db.query(MusicModel).filter(MusicModel.music_id == music_id).first()
  
def delete_music(db: Session, music_id: str):
    music = db.query(MusicModel).filter(MusicModel.music_id == music_id).first()
    if not music:
        return None
    db.delete(music)
    db.commit()
    return music

def create_music(db: Session, music: Music):
    db_music = MusicModel(
        music_id=music.music_id,
        title_kr=music.title_kr,
        title_en=music.title_en,
        url=music.url,
        length=music.length,
        updated_at=datetime.utcnow(),
        created_at=datetime.utcnow()
    )
    db.add(db_music)
    db.commit()
    db.refresh(db_music)
    return db_music

def update_music(db: Session, music_id: str, music: Music):
    db_music = db.query(MusicModel).filter(MusicModel.music_id == music_id).first()
    if not db_music:
        return None
    db_music.title_kr = music.title_kr
    db_music.title_en = music.title_en
    db_music.url = music.url
    db_music.length = music.length
    db_music.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_music)
    return db_music