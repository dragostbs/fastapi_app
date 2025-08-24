import os
from fastapi import Depends
from dotenv import load_dotenv
from jose import jwt, JWTError
from typing import Annotated
from sqlalchemy.orm import Session
from main.database.db import get_db
from passlib.context import CryptContext
from main.models.user import User
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

if not all([SECRET_KEY, ALGORITHM]):
    raise ValueError("Environment variables must be set !")

db_dependency = Annotated[Session, Depends(get_db)]

bcrypt_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto"
)

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl="user/token"
)

def authenticate_user(username: str, password: str, db: db_dependency):
    try:
        user_model = db.query(User).filter(User.username == username).first()

        if not user_model:
            return False
        
        if not bcrypt_context.verify(password, user_model.hashed_password):
            return False
        
        return user_model
    except Exception as e:
        print(f"Error: {e}")

def create_access_token(user_id: int, username: str, role: str, expires_delta: timedelta):
    try:
        encode = {
            "id": user_id,
            "sub": username,
            "role": role
        }

        expires = datetime.now(timezone.utc) + expires_delta

        encode.update({
            "exp": expires
        })

        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        print(f"Error: {e}")

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if user_id is None or username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials...")
        
        return {"id": user_id, "username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials...")

user_dependency = Annotated[dict, Depends(get_current_user)]