import os
from dotenv import load_dotenv

load_dotenv() # Load variables from .env

class Settings:
    MONGO_URL: str = os.getenv("MONGO_URL")
    DB_NAME: str = os.getenv("DB_NAME")
    SECRET_KEY: str = os.getenv("SECRET_KEY")

settings = Settings()