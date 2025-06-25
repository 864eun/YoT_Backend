from fastapi import HTTPException, Header
from firebase_admin import auth
import asyncio

async def verify_token(authorization: str = Header(None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    id_token = authorization.split(" ")[1]
    loop = asyncio.get_running_loop()
    try:
        # 동기 함수를 비동기로 실행
        decoded_token = await loop.run_in_executor(None, auth.verify_id_token, id_token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
