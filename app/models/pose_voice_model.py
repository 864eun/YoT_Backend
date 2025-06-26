from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey
from app.database.database import Base

class PoseVoice(Base):
    __tablename__ = "pose_voice"
    pose_voice_id = Column(String, primary_key=True, index=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    url = Column(String)
    length = Column(Integer)
    pose_id = Column(String, ForeignKey("pose.pose_id"))
