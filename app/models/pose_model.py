from sqlalchemy import Column, String, Boolean, DateTime,Enum, TIMESTAMP
from app.database.database import Base

class Pose(Base):
    __tablename__ = "pose"
    pose_id = Column(String, primary_key=True, index=True)
    pose_name_kr = Column(String)
    pose_name_en = Column(String)
    level = Column(Enum('beginner', 'intermediate', 'advanced'))
    image_url = Column(String)
    created_time = Column(TIMESTAMP)
    updated_time = Column(TIMESTAMP)
