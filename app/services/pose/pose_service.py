from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.pose_model import Pose
import random

async def get_all_poses(db: AsyncSession):
    result = await db.execute(select(Pose))
    return result.scalars().all()

async def get_pose_by_id(db: AsyncSession, pose_id: str):
    result = await db.execute(select(Pose).where(Pose.pose_id == pose_id))
    return result.scalars().first()

async def get_poses_by_level(db: AsyncSession, level: str):
    result = await db.execute(select(Pose).where(Pose.level == level))
    return result.scalars().all()

async def get_random_pose(db: AsyncSession):
    # 전체 포즈 수 계산
    count_result = await db.execute(select(func.count()).select_from(Pose))
    total = count_result.scalar()
    
    if total == 0:
        return None
    
    # 랜덤 오프셋 생성
    random_offset = random.randint(0, total - 1)
    
    # 랜덤 포즈 선택
    result = await db.execute(
        select(Pose).offset(random_offset).limit(1)
    )
    return result.scalars().first()
