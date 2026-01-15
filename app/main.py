from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.database import database
from app.routers import auth, diet 
import os
import subprocess # 👈 New Import

# 1️⃣ Initialize App
app = FastAPI(
    title="Smart Diet Planner API",
    description="Backend for Diet Prediction App using FastAPI and MongoDB",
    version="1.0.0"
)

# 2️⃣ Setup CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3️⃣ Register Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(diet.router) 

# 4️⃣ Database & ML Training on Startup (THE FIX)
@app.on_event("startup")
async def startup_events():
    # A. Connect to Database
    try:
        await database.client.admin.command('ping')
        print("✅ MongoDB Connected Successfully!")
    except Exception as e:
        print(f"❌ MongoDB Connection Failed: {e}")

    # B. Train ML Model on Server 🧠
    # We force the server to run the training script right now.
    # This solves the "Missing File" and "Version Mismatch" errors.
    print("⏳ Checking ML Model...")
    script_path = os.path.join("app", "ml", "ml.py")
    
    try:
        # Run python app/ml/ml.py
        subprocess.run(["python", script_path], check=True)
        print("✅ New ML Model trained and saved successfully on Server!")
    except Exception as e:
        print(f"❌ Failed to train model: {e}")

# 5️⃣ Serve Frontend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "Front-End") # Ensure this matches GitHub folder name exactly!

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")