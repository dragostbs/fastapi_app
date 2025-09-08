from typing import Annotated
from datetime import timedelta
from fastapi import Depends, HTTPException, APIRouter
from main.schemas.user import SupabaseUser, UserVerification
from main.schemas.user import Token
from fastapi.security import OAuth2PasswordRequestForm
from main.database.auth import supabase, authenticate_user, create_access_token, user_dependency

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/token", response_model=Token)
async def login_user_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user_model = await authenticate_user(
            form_data.username, 
            form_data.password
        )

        if not user_model:
            raise HTTPException(status_code=401, detail="Could not validate credentials...")

        token = await create_access_token(
            user_id=user_model.id,
            email=user_model.email,
            role=user_model.role,
            expires_delta=timedelta(minutes=15)
        )

        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/", response_model=SupabaseUser)
async def get_user(user:  user_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication failed...")
        
        user_dict = user.__dict__

        if "identities" in user_dict and user_dict["identities"]:
            user_dict["identities"] = [identity.__dict__ for identity in user_dict["identities"]]

        return SupabaseUser(**user_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/")
async def create_user(email: str, password: str):
    try:
        response = supabase.auth.sign_up({
            "email": email, 
            "password": password
        })
        
        if not response:
            raise HTTPException(status_code=400, detail="Error creating user...")
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/password")
async def change_password(user_verification: UserVerification, user: user_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication failed...")

        update_password = supabase.auth.update_user(
            {"password": user_verification.new_password}
        )
        
        return {"message": "Password updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/")
async def delete_user(user: user_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication failed...")

        supabase.auth.admin.delete_user(user.id)
        
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")