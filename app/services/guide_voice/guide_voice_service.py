from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.guide_voice_model import GuideVoice
from typing import Union, List

async def get_all_guide_voices(db: AsyncSession):
    result = await db.execute(select(GuideVoice))
    return result.scalars().all()

async def get_guide_voice_by_id(
    db: AsyncSession, 
    guide_voice_id: Union[str, List[str]]
):
    if isinstance(guide_voice_id, str):
        result = await db.execute(
            select(GuideVoice).where(GuideVoice.guide_voice_id == guide_voice_id)
        )
        return result.scalars().first()
    elif isinstance(guide_voice_id, list):
        if not guide_voice_id:
            return []
        result = await db.execute(
            select(GuideVoice).where(GuideVoice.guide_voice_id.in_(guide_voice_id))
        )
        return result.scalars().all()
    else:
        return None

async def get_guide_voice_by_label(
    db: AsyncSession, 
    label: Union[str, List[str]]
):
    if isinstance(label, str):
        result = await db.execute(
            select(GuideVoice).where(GuideVoice.label == label)
        )
        return result.scalars().first()
    elif isinstance(label, list):
        if not label:
            return []
        result = await db.execute(
            select(GuideVoice).where(GuideVoice.label.in_(label))
        )
        return result.scalars().all()
    else:
        return None
