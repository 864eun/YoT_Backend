from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.services.guide_voice.guide_voice_service import get_all_guide_voices, get_guide_voice_by_id, get_guide_voice_by_label
from app.schemas.guide_voice_schema import GuideVoiceResponse
from typing import List, Union 

router = APIRouter(prefix="/guide-voices", tags=["guide-voices"])

@router.get("/all", response_model=List[GuideVoiceResponse])
async def read_guide_voices(db: AsyncSession = Depends(get_db)):
    guide_voices = await get_all_guide_voices(db)
    return guide_voices

@router.get("/", response_model=Union[GuideVoiceResponse, List[GuideVoiceResponse]])
async def read_guide_voice_by_id(
    guide_voice_id: Union[str, List[str]] = Query(...),
    db: AsyncSession = Depends(get_db)
):
    guide_voice = await get_guide_voice_by_id(db, guide_voice_id)
    if not guide_voice:
        raise HTTPException(status_code=404, detail="Guide voice not found")
    return guide_voice

@router.get("/label", response_model=Union[GuideVoiceResponse, List[GuideVoiceResponse]])
async def read_guide_voice_by_label(
    label: Union[str, List[str]] = Query(...),
    db: AsyncSession = Depends(get_db)
):
    guide_voice = await get_guide_voice_by_label(db, label)
    if not guide_voice:
        raise HTTPException(status_code=404, detail="Guide voice not found")
    return guide_voice
