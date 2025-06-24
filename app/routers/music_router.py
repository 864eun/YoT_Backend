from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.music_schema import Music
from app.services.music.music_service import get_all_music, get_music_by_id
from app.database.database import get_db
from typing import List

router = APIRouter(
    prefix="/music",
    tags=["music"]
)

@router.get("/all", response_model=List[Music])
def read_all_music(db: Session = Depends(get_db)):
    musics = get_all_music(db)
    return musics

@router.get("/{music_id}", response_model=Music)
def read_music(music_id: str, db: Session = Depends(get_db)):
    music = get_music_by_id(db, music_id)
    if not music:
        raise HTTPException(status_code=404, detail="Music not found")
    return music
