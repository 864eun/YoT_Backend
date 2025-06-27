from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.pose_voice_model import PoseVoice
from typing import Union, List

async def get_all_pose_voices(db: AsyncSession):
    result = await db.execute(select(PoseVoice))
    return result.scalars().all()

async def get_pose_voice_by_id(db: AsyncSession, pose_voice_id: str):
    result = await db.execute(select(PoseVoice).where(PoseVoice.pose_voice_id == pose_voice_id))
    return result.scalars().first()


async def get_pose_voice_by_pose_id(
    db: AsyncSession, 
    pose_id: Union[str, List[str]]
):
    if isinstance(pose_id, str):
        result = await db.execute(
            select(PoseVoice).where(PoseVoice.pose_id == pose_id))
        return result.scalars().all()
    elif isinstance(pose_id, list):
        if not pose_id:
            return []
        result = await db.execute(
            select(PoseVoice).where(PoseVoice.pose_id.in_(pose_id))
        )
        return result.scalars().all()
    else:
        return None
