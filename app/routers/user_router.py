from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.database.database import SessionLocal
from app.utils.firebase_auth import verify_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/user/")
def create_user(user_data=Depends(verify_token), db: Session = Depends(get_db)):
    # user_data에는 Firebase 토큰에서 검증된 유저 정보가 들어 있음
    user_id = user_data["uid"]
    display_name = user_data.get("name")
    email = user_data.get("email")
    email_verified = user_data.get("email_verified")
    provider_id = user_data.get("firebase", {}).get("sign_in_provider")
    creation_time = user_data.get("auth_time") 
    if creation_time is not None:
        from datetime import datetime
        creation_time = datetime.fromtimestamp(creation_time)# 필요시 변환

    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        db_user = User(
            user_id=user_id,
            display_name=display_name,
            email=email,
            email_verified=email_verified,
            provider_id=provider_id,
            creation_time=creation_time
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return {"success": True, "user": user_id}


