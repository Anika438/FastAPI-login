from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter,Form,Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from models import User
from sqlalchemy.orm import Session
from database import SessionLocal
from starlette import status
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
router=APIRouter(prefix="/auth",tags=["auth"])
SECRET_KEY="63f4945d921d599f27ae4fdf5bada3f1"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_bearer=OAuth2PasswordBearer(tokenUrl="/auth/token")
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
def verify_password(plain_password,hashed_password):
    return bcrypt_context.verify(plain_password,hashed_password)
def create_access_token(username :str):
    payload={"sub":username,"exp":datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
db_dependency=Annotated[Session,Depends(get_db)]
@router.post("/",status_code=status.HTTP_201_CREATED)
def register_user(user: str=Form(...),password: str=Form(...), db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = bcrypt_context.hash(user.password)
    new_user = User(
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}
@router.post("/token")
def login(form_data:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(user.username)
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True
    )
    return response
def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return username