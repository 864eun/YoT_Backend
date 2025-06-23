from sqlalchemy.orm import Session
from app.models.pose_model import Pose
import random

def get_all_poses(db: Session):
    return db.query(Pose).all()

# ID로 가져오기
def get_pose_by_id(db: Session, pose_id: str):
    return db.query(Pose).filter(Pose.pose_id == pose_id).first()

# 레벨로 가져오기
def get_poses_by_level(db: Session, level: str):
    return db.query(Pose).filter(Pose.level == level).all()

# 랜던으로 가져오기
def get_random_pose(db: Session):
    poses = db.query(Pose).all()
    if not poses:
        return None
    return random.choice(poses)