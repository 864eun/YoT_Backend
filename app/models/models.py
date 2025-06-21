from sqlalchemy import Column, String, Boolean, DateTime,Enum, TIMESTAMP
from app.database.database import Base

class User(Base):
    __tablename__ = "user"
    user_id = Column(String(255), primary_key=True, index=True)
    display_name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    email_verified = Column(Boolean)
    provider_id = Column(String(255))
    creation_time = Column(DateTime, nullable=True)


# models/models.py

class Pose(Base):
    __tablename__ = "pose"
    pose_id = Column(String, primary_key=True, index=True)
    pose_name_kr = Column(String)
    pose_name_en = Column(String)
    level = Column(Enum('beginner', 'intermediate', 'advanced'))
    image_url = Column(String)
    created_time = Column(TIMESTAMP)
    updated_time = Column(TIMESTAMP)
