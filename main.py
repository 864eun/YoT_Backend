import asyncio
import app.firebase_admin_init
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.routers import user_router, pose_router, music_router, pose_voice_router, guide_voice_router

app = FastAPI()

# 테이블 생성 함수
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await create_tables()  # 비동기 테이블 생성

# CORS 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(user_router.router)
app.include_router(pose_router.router)
app.include_router(music_router.router)
app.include_router(pose_voice_router.router)
app.include_router(guide_voice_router.router)
