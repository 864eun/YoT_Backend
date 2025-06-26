from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.services.pose_voice.pose_voice_serivce import get_all_pose_voices, get_pose_voice_by_id, get_pose_voice_by_pose_id
from app.schemas.pose_voice_schema import PoseVoiceResponse
from typing import List

router = APIRouter(prefix="/pose-voices", tags=["pose-voices"])

@router.get("/", response_model=List[PoseVoiceResponse])
async def get_pose_voices(db: AsyncSession = Depends(get_db)):
    pose_voices = await get_all_pose_voices(db)
    return pose_voices

@router.get("/{pose_voice_id}", response_model=PoseVoiceResponse)
async def get_pose_voice(pose_voice_id: str, db: AsyncSession = Depends(get_db)):
    pose_voice = await get_pose_voice_by_id(db, pose_voice_id)
    if not pose_voice:
        raise HTTPException(status_code=404, detail="Pose voice not found")
    return pose_voice

@router.get("/pose/{pose_id}", response_model=PoseVoiceResponse)
async def get_pose_voice_by_pose(pose_id: str, db: AsyncSession = Depends(get_db)):
    pose_voice = await get_pose_voice_by_pose_id(db, pose_id)
    if not pose_voice:
        raise HTTPException(status_code=404, detail="Pose voice not found")
    return pose_voice
