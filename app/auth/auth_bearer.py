# app/auth/auth_bearer.py
from fastapi import Request, HTTPException
from app.auth.auth_handler import verify_session

def get_current_user(request: Request):
    token = request.cookies.get("session")
    if not token:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    user_id = verify_session(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    
    return user_id
