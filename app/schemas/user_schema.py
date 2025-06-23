from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#schemas/: API 입출력 데이터 정의 (Pydantic)
class UserCreate(BaseModel):
    user_id: str
    display_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    provider_id: Optional[str] = None
    creation_time: Optional[datetime] = None