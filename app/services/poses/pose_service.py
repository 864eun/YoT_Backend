# services/pose_service.py
from sqlalchemy.orm import Session
from app.models.models import Pose

def get_all_poses(db: Session):
    return db.query(Pose).all()
