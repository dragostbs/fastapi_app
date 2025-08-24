from pydantic import BaseModel, Field

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