
from sqlite3 import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import database
from app.auth import utils, schemas as auth_schemas
from fastapi import APIRouter, Depends, HTTPException, status
from app.user import crud, models, schemas as user_schemas

router = APIRouter()


@router.post("/login", response_model=auth_schemas.Token) # type: ignore
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(database.get_db)):
    
    user = await crud.get_user_by_username(db, username=form_data.username) # type: ignore
    if not user or not utils.verify_password(form_data.password, user.hashed_password): # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
      
      
    access_token = utils.create_access_token(data= {"sub": user.username, "user_id": user.id}) # type: ignore
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=user_schemas.User) # type: ignore
async def register(user: auth_schemas.registerUser, db: AsyncSession = Depends(database.get_db)):
   hashed_password = utils.hash_password(user.password)
   db_user = models.User(
       username = user.username,
       full_name = user.full_name,
       hashed_password = hashed_password
   )
   db.add(db_user)
   try:
       await db.commit()
       await db.refresh(db_user)
   except IntegrityError:
       raise HTTPException(status_code=400, detail="Username already registered")
   return db_user


@router.get("/me", response_model=user_schemas.User) # type: ignore
async def read_users_me(current_user: models.User = Depends(utils.get_current_user)):
    return current_user


@router.get("/role")
async def read_user_role(role: str = Depends(utils.get_user_role)):
    return {"role": role}