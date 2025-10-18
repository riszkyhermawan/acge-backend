from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.user.crud import get_user_by_username 

router = APIRouter()


@router.get("/users/{username}")
async def read_user(username: str, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, username) # type: ignore
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user