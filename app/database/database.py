# app/database/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("S3_DATABASE_API_URL").replace("mysql+pymysql://", "mysql+aiomysql://")

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
