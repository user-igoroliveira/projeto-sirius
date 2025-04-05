# app/auth/auth_handler.py
import os
from itsdangerous import URLSafeSerializer
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
serializer = URLSafeSerializer(SECRET_KEY)

def create_session(user_id: int):
    return serializer.dumps({"user_id": user_id})

def verify_session(token: str):
    try:
        data = serializer.loads(token)
        return data["user_id"]
    except Exception:
        return None
