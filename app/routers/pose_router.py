from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from typing import Union, List
from app.services.pose.pose_service import (
    get_all_poses, get_pose_by_id, get_poses_by_level, get_random_pose
)
from app.schemas.pose_schema import PoseResponse

router = APIRouter(
    prefix="/poses",
    tags=["poses"]
)

@router.get("/all", response_model=list[PoseResponse])
async def read_poses(db: AsyncSession = Depends(get_db)):
    poses = await get_all_poses(db)
    return poses

@router.get("/", response_model=Union[PoseResponse, List[PoseResponse]])
async def read_pose_by_id(
    pose_id: Union[str, List[str]] = Query(...),
    db: AsyncSession = Depends(get_db)
):
    pose_data = await get_pose_by_id(db, pose_id)
    
    if not pose_data:
        raise HTTPException(status_code=404, detail="Pose not found")
    
    return pose_data

@router.get("/level/{level}", response_model=list[PoseResponse])
async def read_poses_by_level(level: str, db: AsyncSession = Depends(get_db)):
    poses = await get_poses_by_level(db, level)
    return poses

@router.get("/random", response_model=PoseResponse)
async def read_random_pose(db: AsyncSession = Depends(get_db)):
    pose = await get_random_pose(db)
    if pose is None:
        raise HTTPException(status_code=404, detail="Pose not found")
    return pose
