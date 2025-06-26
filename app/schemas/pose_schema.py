from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PoseBase(BaseModel):
    name_kr: str
    name_en: str
    level: str
    url: str

class PoseCreate(PoseBase):
    pose_id: str  # 생성 시 직접 지정한다면 포함

class PoseResponse(PoseBase):
    pose_id: str
    created_time: Optional[datetime] = None
    updated_time: Optional[datetime] = None

    class Config:
        from_attributes = True
