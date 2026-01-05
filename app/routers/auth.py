from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.database import users_collection
from app.utils.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

# --- SIGNUP ROUTE ---
@router.post("/signup", response_model=dict)
async def signup(user: UserCreate):
    # 1. Check if email already exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    # Optional: Check if patient_id already exists?
    existing_pid = await users_collection.find_one({"patient_id": user.patient_id})
    if existing_pid:
        raise HTTPException(status_code=400, detail="Patient ID already exists")

    # 2. Hash the password
    hashed_password = get_password_hash(user.password)

    # 3. Create user document
    new_user = {
        "name": user.name,
        "email": user.email,
        "hashed_password": hashed_password,
        "age": user.age,
        "contact_no": user.contact_no,
        "patient_id": user.patient_id,
        "gender": user.gender
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
    # We can include the patient_id in the token if we want to use it later
    access_token = create_access_token(data={"sub": db_user["email"], "pid": db_user["patient_id"]})

    return {"access_token": access_token, "token_type": "bearer"}