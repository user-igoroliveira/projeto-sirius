from fastapi import FastAPI, Request, Form, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth.auth_handler import create_session, verify_session
from app.auth.auth_bearer import get_current_user
import bcrypt

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Página de login
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    registered = request.query_params.get("registered") == "true"
    return templates.TemplateResponse("login.html", {
        "request": request,
        "success": "Conta criada com sucesso! Faça login abaixo." if registered else None
    })

# Página de cadastro
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Processa o formulário de cadastro
@app.post("/register")
async def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    if not username.strip() or not password.strip():
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Usuário e senha são obrigatórios."
        })

    if len(password) < 6:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "A senha deve ter no mínimo 6 caracteres."
        })

    if password != confirm_password:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "As senhas não coincidem."
        })

    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Usuário já existe."
        })

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = User(username=username.strip(), hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()

    return RedirectResponse(url="/?registered=true", status_code=status.HTTP_302_FOUND)

# Processa o formulário de login
@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Credenciais inválidas."
        })

    token = create_session(user.id)
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="session", value=token, httponly=True)
    return response

# Página protegida do dashboard
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user_id: int = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user_id": user_id
    })

# Roteamento adicional
from app.routes import user
app.include_router(user.router)
