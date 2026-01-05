from pydantic import BaseModel, EmailStr

# Schema for Signup Request
class UserCreate(BaseModel):
    name: str             # Changed from 'username' to 'name' based on your list
    email: EmailStr
    password: str
    age: int
    contact_no: str       # String is better for phones (preserves leading zeros, +, etc.)
    patient_id: str       # Assuming user enters this manually
    gender: str

# Schema for Login Request
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for the Response (Token)
class Token(BaseModel):
    access_token: str
    token_type: str