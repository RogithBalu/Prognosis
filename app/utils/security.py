from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings

# 1. Setup Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Function to Hash Password (like bcrypt.hash)
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 3. Function to Verify Password (like bcrypt.compare)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 4. Function to Create JWT Token (like jwt.sign)
def create_access_token(data: dict):
    to_encode = data.copy()
    # Token expires in 30 minutes
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt