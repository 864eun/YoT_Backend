from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PoseVoiceBase(BaseModel):
    url: str
    length: int
    pose_id: str

class PoseVoiceCreate(PoseVoiceBase):
    pose_voice_id: str

class PoseVoiceResponse(PoseVoiceBase):
    pose_voice_id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
