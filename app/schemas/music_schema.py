from pydantic import BaseModel
from datetime import datetime

class Music(BaseModel):
    music_id: str
    title_kr: str
    title_en: str
    url: str
    length: int
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
