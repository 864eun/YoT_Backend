from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_model import User
from app.database.database import get_db
from app.utils.firebase_auth import verify_token

router = APIRouter()

@router.post("/user/")
async def create_user(user_data=Depends(verify_token), db: AsyncSession = Depends(get_db)):
    user_id = user_data["uid"]
    display_name = user_data.get("name")
    email = user_data.get("email")
    email_verified = user_data.get("email_verified")
    provider_id = user_data.get("firebase", {}).get("sign_in_provider")
    creation_time = user_data.get("auth_time")
    if creation_time is not None:
        from datetime import datetime
        creation_time = datetime.fromtimestamp(creation_time)

    # 비동기 쿼리
    result = await db.execute(select(User).where(User.user_id == user_id))
    db_user = result.scalars().first()
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
        await db.commit()
        await db.refresh(db_user)
    return {"success": True, "user": user_id}
