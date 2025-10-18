from sqlalchemy import text
from fastapi import Depends, FastAPI, HTTPException
from app.user import router as user_router
from app.auth import router as auth_router
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(title="ACGE Backend")
app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])


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