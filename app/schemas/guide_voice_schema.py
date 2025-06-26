from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GuideVoiceBase(BaseModel):
    url: str
    label: str
    length: int

class GuideVoiceCreate(GuideVoiceBase):
    guide_voice_id: str

class GuideVoiceResponse(GuideVoiceBase):
    guide_voice_id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
