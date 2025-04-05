# app/routes/user.py
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth.auth_handler import create_session
import bcrypt

router = APIRouter()

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        return RedirectResponse(url="/", status_code=303)

    session_token = create_session(user.id)
    response = RedirectResponse(url="/formulario", status_code=303)
    response.set_cookie(key="session", value=session_token, httponly=True)
    return response
