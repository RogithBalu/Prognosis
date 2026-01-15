from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.database import database
from app.routers import auth, diet 
import os
import subprocess # 👈 Import this to run the training script

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

# 4️⃣ Database & ML Training on Startup
@app.on_event("startup")
async def startup_events():
    # A. Connect to Database
    try:
        await database.client.admin.command('ping')
        print("✅ MongoDB Connected Successfully!")
    except Exception as e:
        print(f"❌ MongoDB Connection Failed: {e}")

    # B. Train ML Model (The Fix) 🧠
    # This runs 'python app/ml/ml.py' every time the server starts
    model_path = "app/ml/diet_classifier.pkl"
    script_path = "app/ml/ml.py"
    
    if not os.path.exists(model_path):
        print("⚠️ Model not found! Training a new one now...")
        try:
            # Run the training script inside the container
            subprocess.run(["python", script_path], check=True)
            print("✅ New ML Model trained and saved successfully!")
        except Exception as e:
            print(f"❌ Failed to train model: {e}")
    else:
        print("✅ ML Model found.")

# 5️⃣ Serve Frontend
# WARNING: Linux is case-sensitive! Ensure your folder is exactly "Front-End" or "frontend"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "Front-End") 

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")