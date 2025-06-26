from sqlalchemy import Column, String, Integer, TIMESTAMP
from app.database.database import Base

class GuideVoice(Base):
    __tablename__ = "guide_voice"
    guide_voice_id = Column(String, primary_key=True, index=True)
    created_at = Column(TIMESTAMP)
    url = Column(String)
    label = Column(String)  # "start", "count10s" 등
    length = Column(Integer)
    updated_at = Column(TIMESTAMP)
