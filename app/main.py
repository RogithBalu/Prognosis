from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import database  # <--- IMPORT THIS

# 1. Initialize the App
app = FastAPI(
    title="Smart Diet Planner API",
    description="Backend for Diet Prediction App using FastAPI and MongoDB",
    version="1.0.0"
)

# 2. Setup CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register the Auth Router
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# 3. Database Connection Check on Startup
@app.on_event("startup")
async def startup_db_client():
    try:
        # Send a "ping" to the database to check connection
        await database.command("ping")
        print("✅ MongoDB Connected Successfully!")
    except Exception as e:
        print(f"❌ MongoDB Connection Failed: {e}")

# 4. Root Route (Health Check)
@app.get("/")
async def health_check():
    # You can now return the DB status in the health check
    return {"status": "active", "message": "Diet Planner Backend is running!"}