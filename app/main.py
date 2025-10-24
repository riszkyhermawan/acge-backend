from sqlalchemy import text
from fastapi import Depends, FastAPI, HTTPException
from app.user import router as user_router
from app.auth import router as auth_router
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.compiler import router as compiler_router

app = FastAPI(title="ACGE Backend")
origins = settings.CLIENT_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(compiler_router.router, prefix="/compiler", tags=["compiler"])


@app.get("/")
async def read_root():
    return {"message": "Buruaan kELARIN WOE SKRIPSI NYA ANJAY"}


@app.get("/health", tags=["health check"])
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=503, detail="Database connection error")