from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel
from app.database.database import get_db
from app.services.video.video_test2 import create_pose_video

router = APIRouter(prefix="/api/video", tags=["video"])

class VideoCreateRequest(BaseModel):
    pose_ids: List[str]
    music_id: str
    guide_labels: List[str]

@router.post("/create")
async def create_video(
    request: VideoCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        video_path = await create_pose_video(
            db=db,
            pose_ids=request.pose_ids,
            music_id=request.music_id,
            guide_labels=request.guide_labels
        )
        return {"video_path": video_path}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
