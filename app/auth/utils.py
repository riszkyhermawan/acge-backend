from app.core import config, database
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from app.user import crud, models


from app.user.crud import get_user_by_username

settings = config.settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM) # type: ignore
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]) # type: ignore
        username: str = payload.get("sub") # type: ignore
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception
    
    return username

async def get_current_user(token:str = Depends(oauth2_scheme), db:AsyncSession = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        username = verify_token(token, credentials_exception)
    except Exception as e:
        raise credentials_exception
    
    username = verify_token(token, credentials_exception)
    user =  await crud.get_user_by_username(db, username) # type: ignore
    if user is None:
        raise credentials_exception
    
    return user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



async def get_user_role (current_user: models.User = Depends(get_current_user)):
    return current_user.role