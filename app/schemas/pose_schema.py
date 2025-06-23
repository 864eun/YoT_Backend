from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PoseResponse(BaseModel):
    pose_id: str
    pose_name_kr: str
    pose_name_en: str
    level: str
    image_url: str

    class Config:
        orm_mode = True