import os
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends, HTTPException
from supabase import create_client, Client
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET")

if not all([SUPABASE_URL, SUPABASE_KEY, SUPABASE_JWT_SECRET]):
    raise ValueError("Supabase environment variables must be set...")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl="auth/token"
)

async def authenticate_user(email: str, password: str):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email, 
            "password": password
        })

        if not response:
            raise HTTPException(status_code=401, detail="Invalid email or password...")
        
        return response.user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Authentication failed...")

async def create_access_token(user_id: str, email: str, role: str, expires_delta: timedelta):
    try:
        payload = {
            "sub": user_id,
            "email": email,
            "role": role,
            "aud": "authenticated",
            "exp": datetime.utcnow() + expires_delta
        }

        access_token = jwt.encode(payload, SUPABASE_JWT_SECRET, algorithm="HS256")

        return access_token
    except Exception as e:
        raise HTTPException(status_code=500, detail="Token creation failed...")

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        response = supabase.auth.get_user(token)

        if not response:
            raise HTTPException(status_code=401, detail="Could not validate credentials...")
        
        return response.user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

user_dependency = Annotated[dict, Depends(get_current_user)]