from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    user_id: str
    display_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    provider_id: Optional[str] = None
    creation_time: Optional[datetime] = None



#pose 응답 스키마
class PoseResponse(BaseModel):
    pose_id: str
    pose_name_kr: str
    pose_name_en: str
    level: str
    image_url: str

    class Config:
        orm_mode = True
