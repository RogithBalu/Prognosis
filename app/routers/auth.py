from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.database import users_collection
from app.utils.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

# --- SIGNUP ROUTE ---
@router.post("/signup", response_model=dict)
async def signup(user: UserCreate):
    # 1. Check if user already exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Hash the password
    hashed_password = get_password_hash(user.password)

    # 3. Create user document (Dictionary)
    new_user = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password
    }

    # 4. Insert into MongoDB
    await users_collection.insert_one(new_user)

    return {"message": "User created successfully"}

# --- LOGIN ROUTE ---
@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    # 1. Find user by email
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # 2. Verify password
    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # 3. Generate JWT Token
    access_token = create_access_token(data={"sub": db_user["email"]})

    return {"access_token": access_token, "token_type": "bearer"}