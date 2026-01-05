import motor.motor_asyncio
from app.core.config import settings

# 1. Create the Client
# Equivalent to mongoose.connect(process.env.MONGO_URL)
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)

# 2. Connect to the specific database
database = client[settings.DB_NAME]

# 3. Export Collections
# We define them here so we can import them easily in other files
users_collection = database.get_collection("users")
diet_plans_collection = database.get_collection("diet_plans")