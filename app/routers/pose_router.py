# routers/pose_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.poses.pose_service import get_all_poses
from app.schemas.schemas import PoseResponse

router = APIRouter(
    prefix="/poses",
    tags=["poses"]
)

@router.get("/all", response_model=list[PoseResponse])
def read_poses(db: Session = Depends(get_db)):
    poses = get_all_poses(db)
    return poses
