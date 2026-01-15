from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # 👈 New Import
from fastapi.responses import FileResponse   # 👈 New Import
from app.core.database import database
from app.routers import auth, diet 
import os

# 1️⃣ Initialize the FastAPI app
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

# 3️⃣ Register routers (API Endpoints)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(diet.router) 

# 4️⃣ Database connection check
@app.on_event("startup")
async def startup_db_client():
    try:
        await database.client.admin.command('ping')
        print("✅ MongoDB Connected Successfully!")
    except Exception as e:
        print(f"❌ MongoDB Connection Failed: {e}")

# ==========================================
# 5️⃣ SERVE FRONTEND (The Fix)
# ==========================================

# A. Find the path to the 'frontend' folder
# (Goes up two levels from 'app/routers' or one level from 'app')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "Front-End")

# B. Serve index.html at the root URL "/"
@app.get("/")
async def read_root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# C. Mount the rest of the files (CSS, JS, login.html, etc.)
# This tells FastAPI: "If the user asks for /style.css, look in the frontend folder"
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")