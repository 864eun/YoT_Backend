# app/services/music/music_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.music_model import MusicModel
from app.schemas.music_schema import Music
from datetime import datetime

async def get_all_music(db: AsyncSession):
    result = await db.execute(select(MusicModel))
    return result.scalars().all()

async def get_music_by_id(db: AsyncSession, music_id: str):
    result = await db.execute(select(MusicModel).where(MusicModel.music_id == music_id))
    return result.scalars().first()

async def delete_music(db: AsyncSession, music_id: str):
    result = await db.execute(select(MusicModel).where(MusicModel.music_id == music_id))
    music = result.scalars().first()
    if not music:
        return None
    await db.delete(music)
    await db.commit()
    return music

async def create_music(db: AsyncSession, music: Music):
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
    await db.commit()
    await db.refresh(db_music)
    return db_music

async def update_music(db: AsyncSession, music_id: str, music: Music):
    result = await db.execute(select(MusicModel).where(MusicModel.music_id == music_id))
    db_music = result.scalars().first()
    if not db_music:
        return None
    db_music.title_kr = music.title_kr
    db_music.title_en = music.title_en
    db_music.url = music.url
    db_music.length = music.length
    db_music.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(db_music)
    return db_music
