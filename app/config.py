import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    DB_URL = os.getenv("DB_URL")
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGO = os.getenv("JWT_ALGO", "HS256")
    BASE_URL = os.getenv("BASE_URL")
    SSLCZ_STORE_ID = os.getenv("SSLCZ_STORE_ID")
    SSLCZ_STORE_PASS = os.getenv("SSLCZ_STORE_PASS")
    SSLCZ_SANDBOX = os.getenv("SSLCZ_SANDBOX", "true").lower() == "true"

settings = Settings()
