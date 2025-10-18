from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from urllib.parse import quote

encoded_password = quote(settings.PASSWORD) # type: ignore

DATABASE_URL = f"postgresql+asyncpg://{settings.USER}:{encoded_password}@{settings.HOST}:{settings.PORT}/{settings.DBNAME}" # type: ignore


engine = create_async_engine(DATABASE_URL)  # type: ignore

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
        
        
