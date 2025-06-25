from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PoseResponse(BaseModel):
    pose_id: str
    name_kr: str
    name_en: str
    level: str
    url: str

    class Config:
      from_attributes = True 