from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

class UserRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str
    is_active: bool
    role: str

class UserIdentity(BaseModel):
    id: str
    identity_id: str
    user_id: str
    identity_data: dict
    provider: str
    created_at: datetime
    last_sign_in_at: datetime
    updated_at: datetime

class SupabaseUser(BaseModel):
    id: str
    email: str
    phone: Optional[str]
    role: str
    created_at: datetime
    updated_at: datetime
    app_metadata: dict
    user_metadata: dict
    identities: Optional[List[UserIdentity]]

class SupabaseAuthResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    user: SupabaseUser