from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.guide_voice_model import GuideVoice

async def get_all_guide_voices(db: AsyncSession):
    result = await db.execute(select(GuideVoice))
    return result.scalars().all()

async def get_guide_voice_by_id(db: AsyncSession, guide_voice_id: str):
    result = await db.execute(select(GuideVoice).where(GuideVoice.guide_voice_id == guide_voice_id))
    return result.scalars().first()

async def get_guide_voice_by_label(db: AsyncSession, label: str):
    result = await db.execute(select(GuideVoice).where(GuideVoice.label == label))
    return result.scalars().first()

async def get_guide_voices_by_labels(db: AsyncSession, labels: list):
    result = await db.execute(select(GuideVoice).where(GuideVoice.label.in_(labels)))
    return result.scalars().all()
