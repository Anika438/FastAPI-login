from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from models import User
from sqlalchemy.orm import Session
from database import SessionLocal
from starlette import status
from passlib.context import CryptContext
router=APIRouter(prefix="/auth",tags=["auth"])
SECRET_KEY="63f4945d921d599f27ae4fdf5bada3f1"
ALGORITHM="HS256"
bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_bearer=OAuth2PasswordBearer(tokenUrl="auth/token")
class createuser(BaseModel):
    username:str
    password:str
class token(BaseModel):
    access_token:str
    token_type:str
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency=Annotated[Session,Depends(get_db)]
@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,user:createuser):
    hashed_password=bcrypt_context.hash(user.password)
    user_model=User(username=user.username,password=hashed_password)
    db.add(user_model)
    db.commit()