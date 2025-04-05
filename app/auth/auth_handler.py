# app/auth/auth_handler.py
from itsdangerous import URLSafeSerializer

SECRET_KEY = "1234"  # Substitua por um segredo real
serializer = URLSafeSerializer(SECRET_KEY)

def create_session(user_id: int):
    return serializer.dumps({"user_id": user_id})

def verify_session(token: str):
    try:
        data = serializer.loads(token)
        return data["user_id"]
    except Exception:
        return None
