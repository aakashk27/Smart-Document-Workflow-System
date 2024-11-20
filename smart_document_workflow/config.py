import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "default")

    if(MONGO_URI.startswith("default")):
        raise ValueError("MONGO_URI not set in .env file")
