import os
from dotenv import load_dotenv

load_dotenv()

# Basic details
SECRET_KEY = os.getenv("SECRET_KEY", "1d00b663c745f8ee5c1aefbd27ef5826d1c9b0a6fdfcb7e07187d20239edb942")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database details
DB_NAME=os.getenv('DB_NAME')
DB_USER=os.getenv('DB_USER')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable must be set.")
