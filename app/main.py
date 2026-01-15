from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import database
from app.routers import auth, diet 

# 1️⃣ Initialize the FastAPI app
app = FastAPI(
    title="Smart Diet Planner API",
    description="Backend for Diet Prediction App using FastAPI and MongoDB",
    version="1.0.0"
)

# 2️⃣ Setup CORS (FIXED)
# We use "*" to allow ALL origins. 
# This fixes the "Failed to fetch" and "400 Bad Request" errors.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3️⃣ Register routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# FIX: Removed 'tags=["ML Prediction"]' because it is already named in diet.py
app.include_router(diet.router) 

# 4️⃣ Database connection check on startup
@app.on_event("startup")
async def startup_db_client():
    try:
        await database.client.admin.command('ping')
        print("✅ MongoDB Connected Successfully!")
    except Exception as e:
        print(f"❌ MongoDB Connection Failed: {e}")

# 5️⃣ Root route (health check)
@app.get("/")
async def health_check():
    return {"status": "active", "message": "Diet Planner Backend is running!"}