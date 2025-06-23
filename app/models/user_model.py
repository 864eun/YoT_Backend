from sqlalchemy import Column, String, Boolean, DateTime,Enum, TIMESTAMP
from app.database.database import Base

#models/: DB 테이블 구조 정의 (SQLAlchemy)
class User(Base):
    __tablename__ = "user"
    user_id = Column(String(255), primary_key=True, index=True)
    display_name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    email_verified = Column(Boolean)
    provider_id = Column(String(255))
    creation_time = Column(DateTime, nullable=True)

