# routers/pose_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.poses.pose_service import (
    get_all_poses, get_pose_by_id, get_poses_by_level, get_random_pose
)
from app.schemas.pose_schema import PoseResponse

router = APIRouter(
    prefix="/poses",
    tags=["poses"]
)

@router.get("/all", response_model=list[PoseResponse])
def read_poses(db: Session = Depends(get_db)):
    poses = get_all_poses(db)
    return poses

# 포즈 ID로 가져오기
@router.get("/{pose_id}", response_model=PoseResponse)
def read_pose_by_id(pose_id: str, db: Session = Depends(get_db)):
    pose = get_pose_by_id(db, pose_id)
    if pose is None:
        raise HTTPException(status_code=404, detail="Pose not found")
    return pose

# 포즈 레벨로 가져오기
@router.get("/level/{level}", response_model=list[PoseResponse])
def read_poses_by_level(level: str, db: Session = Depends(get_db)):
    poses = get_poses_by_level(db, level)
    return poses

@router.get("/random", response_model=PoseResponse)
def read_random_pose(db: Session = Depends(get_db)):
    pose = get_random_pose(db)
    if pose is None:
        raise HTTPException(status_code=404, detail="Pose not found")
    return pose