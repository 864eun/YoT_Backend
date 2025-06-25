# app/routers/music_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.music_schema import Music
from app.services.music.music_service import get_all_music, get_music_by_id
from app.database.database import get_db
from typing import List

router = APIRouter(
    prefix="/music",
    tags=["music"]
)

@router.get("/all", response_model=List[Music])
async def read_all_music(db: AsyncSession = Depends(get_db)):
    musics = await get_all_music(db)
    return musics

@router.get("/{music_id}", response_model=Music)
async def read_music(music_id: str, db: AsyncSession = Depends(get_db)):
    music = await get_music_by_id(db, music_id)
    if not music:
        raise HTTPException(status_code=404, detail="Music not found")
    return music
