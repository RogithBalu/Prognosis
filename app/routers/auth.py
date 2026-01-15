from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.database import users_collection
from app.utils.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings

router = APIRouter()

# --- 1. SETUP SECURITY SCHEME ---
# This tells FastAPI that the client should send the token in the Header
# and that the login URL is "/auth/login"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# --- 2. THE MISSING FUNCTION (get_current_user) ---
# This function validates the token for every protected request
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token using your SECRET_KEY
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Check if the user actually exists in the database
    user = await users_collection.find_one({"email": email})
    if user is None:
        raise credentials_exception
        
    return user

# --- SIGNUP ROUTE ---
@router.post("/signup", response_model=dict)
async def signup(user: UserCreate):
    # Check if email already exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    # Check if patient_id already exists
    existing_pid = await users_collection.find_one({"patient_id": user.patient_id})
    if existing_pid:
        raise HTTPException(status_code=400, detail="Patient ID already exists")

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create user document
    new_user = {
        "name": user.name,
        "email": user.email,
        "hashed_password": hashed_password,
        "age": user.age,
        "contact_no": user.contact_no,
        "patient_id": user.patient_id,
        "gender": user.gender
    }

    # Insert into MongoDB
    await users_collection.insert_one(new_user)

    return {"message": "User created successfully"}

# --- LOGIN ROUTE ---
@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    # Find user by email
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verify password
    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Generate JWT Token
    access_token = create_access_token(data={"sub": db_user["email"], "pid": db_user["patient_id"]})

    return {"access_token": access_token, "token_type": "bearer"}