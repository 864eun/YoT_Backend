# app/api/user_api.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import models
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

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        db_user = models.User(
            id=user_id,
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



# app/api/user_api.py
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.models import models
# from app.schemas import schemas
# from app.database.database import SessionLocal
# from sqlalchemy.exc import IntegrityError

# router = APIRouter()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.post("/user/")
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     # 중복 체크
#     if db.query(models.User).filter(models.User.id == user.id).first():
#         raise HTTPException(status_code=409, detail="User already exists")
#     db_user = models.User(
#         id=user.id,
#         display_name=user.display_name,
#         email=user.email,
#         email_verified=user.email_verified,
#         provider_id=user.provider_id,
#         creation_time=user.creation_time
#     )
#     try:
#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)
#         return {"success": True, "user": db_user.id}
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(status_code=409, detail="Duplicate entry")
