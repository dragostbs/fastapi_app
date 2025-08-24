from fastapi import Depends
from datetime import timedelta
from typing import Annotated
from main.models.user import User
from main.models.todo import Todo
from main.database.utils import db_dependency, user_dependency
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException
from main.schemas.user import Token, UserRequest, UserVerification
from main.database.utils import authenticate_user, create_access_token, bcrypt_context

router = APIRouter(
    prefix="/user",
    tags=["user"]
)
    
@router.post("/token", response_model=Token)
async def login_user_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user_model = authenticate_user(form_data.username, form_data.password, db)

    if not user_model:
        raise HTTPException(status_code=401, detail="Could not validate credentials...")
    
    token = create_access_token(
        user_model.id,
        user_model.username,
        user_model.role,
        timedelta(minutes=15)
    )

    return {"access_token": token, "token_type": "bearer"}

@router.get("/")
async def get_user(db: db_dependency, user: user_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication failed...")

        user_model = db.query(User).filter(User.id == user.get("id")).first()

        return user_model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/")
async def create_user(user_request: UserRequest, db: db_dependency):
    try:
        new_user = User(
            username=user_request.username,
            first_name=user_request.first_name,
            last_name=user_request.last_name,
            email=user_request.email,
            phone_number=user_request.phone_number,
            hashed_password=bcrypt_context.hash(user_request.password),
            is_active=user_request.is_active,
            role=user_request.role
        )

        db.add(new_user)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/password")
async def change_password(user_verification: UserVerification, db: db_dependency, user: user_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication failed...")

        user_model = db.query(User).filter(User.id == user.get("id")).first()

        if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
            raise HTTPException(status_code=401, detail="Error changing the password...")
        
        user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)

        db.add(user_model)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/")
async def delete_user(db: db_dependency, user: user_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication failed...")
        
        db.query(User).filter(User.id == user.get("id")).first()
        db.query(Todo).filter(Todo.user_id == user.get("id")).delete()
        db.query(User).filter(User.id == user.get("id")).delete()
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
