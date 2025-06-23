# app/main.py
import app.firebase_admin_init
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from app.routers import user_router
from app.database.database import engine, Base
from app.routers import pose_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 프론트엔드 주소 (포트까지 정확히)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)

app.include_router(pose_router.router)