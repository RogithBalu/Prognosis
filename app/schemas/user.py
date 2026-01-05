from pydantic import BaseModel, EmailStr

# Schema for Signup Request
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Schema for Login Request
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for the Response (Token)
class Token(BaseModel):
    access_token: str
    token_type: str