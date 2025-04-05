import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from app.database import engine, Base
from app.models import User

print(">> Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print(">> Tabelas criadas com sucesso!")
