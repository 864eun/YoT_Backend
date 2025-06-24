from sqlalchemy import Column, String, Integer, DateTime
from app.database.database import Base

class MusicModel(Base):
    __tablename__ = "music"

    music_id = Column(String, primary_key=True, index=True)
    title_kr = Column(String)
    title_en = Column(String)
    url = Column(String)
    length = Column(Integer)
    updated_at = Column(DateTime)
    created_at = Column(DateTime)
