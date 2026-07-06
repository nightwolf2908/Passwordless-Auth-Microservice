from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis import Redis
import random
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session

app = FastAPI(title="Passwordless Auth API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURACIÓN DE POSTGRESQL ---
DATABASE_URL = "postgresql://usuario_admin:mi_password_secreto@postgres_db:5432/auth_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CONFIGURACIÓN DE REDIS ---
REDIS_HOST = "redis_cache"
cliente_redis = Redis(host=REDIS_HOST, port=6379, decode_responses=True)

# --- MODELOS DE PYDANTIC ---
class SolicitudCodigo(BaseModel):
    email: str

class VerificacionCodigo(BaseModel):
    email: str
    codigo: str

class RegistroUsuario(BaseModel):
    email: str
    username: str


# --- ENDPOINTS ---

@app.get("/")
def inicio():
    return {"mensaje": "¡Backend de Autenticación Corriendo!"}

# ENDPOINT 1: Solicitar código (No cambia)
@app.post("/auth/request-code")
def solicitar_codigo(solicitud: SolicitudCodigo):
    email = solicitud.email
    codigo_otp = f"{random.randint(100000, 999999)}"
    try:
        cliente_redis.set(name=email, value=codigo_otp, ex=300)
        print("\n" + "="*40)
        print(f"📧 ENVIANDO CORREO A: {email}")
        print(f"🔑 TU CÓDIGO DE VERIFICACIÓN ES: {codigo_otp}")
        print("="*40 + "\n")
        return {"mensaje": "Código enviado con éxito. Revisa la terminal de Docker."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error con Redis: {str(e)}")

# ENDPOINT 2 MODIFICADO: Verificar código e informar si el usuario existe
@app.post("/auth/verify-code")
def verificar_codigo(solicitud: VerificacionCodigo, db: Session = Depends(get_db)):
    email = solicitud.email
    codigo_usuario = solicitud.codigo

    codigo_real = cliente_redis.get(name=email)

    if not codigo_real:
        raise HTTPException(status_code=400, detail="El código ha expirado o no se ha solicitado.")

    if codigo_usuario != codigo_real:
        raise HTTPException(status_code=400, detail="El código de verificación es incorrecto.")

    # Guardamos la marca de verificado en Redis por 10 minutos
    cliente_redis.set(name=f"verificado:{email}", value="true", ex=600)
    cliente_redis.delete(email)

    # REVISIÓN EN POSTGRESQL: ¿El usuario ya existe en Docker?
    usuario_existente = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
    
    if usuario_existente:
        return {
            "mensaje": "Código verificado.",
            "existe": True,
            "username": usuario_existente.username
        }
    
    return {
        "mensaje": "Código verificado.",
        "existe": False
    }

# ENDPOINT 3: Registro (Solo si NO existe)
@app.post("/auth/register")
def registrar_usuario(solicitud: RegistroUsuario, db: Session = Depends(get_db)):
    email = solicitud.email
    username = solicitud.username

    esta_verificado = cliente_redis.get(name=f"verificado:{email}")
    if not esta_verificado:
        raise HTTPException(status_code=401, detail="Este correo electrónico no ha sido verificado.")

    usuario_existente = db.query(UsuarioDB).filter((UsuarioDB.email == email) | (UsuarioDB.username == username)).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El nombre de usuario o el correo ya están registrados.")

    nuevo_usuario = UsuarioDB(username=username, email=email)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    cliente_redis.delete(f"verificado:{email}")

    return {
        "mensaje": "¡Usuario creado con éxito en PostgreSQL!",
        "usuario": {"username": nuevo_usuario.username, "email": nuevo_usuario.email}
    }

# ENDPOINT 4 NUEVO: Inicio de Sesión Directo (Si ya existe)
@app.post("/auth/login")
def login_usuario(solicitud: SolicitudCodigo, db: Session = Depends(get_db)):
    email = solicitud.email

    esta_verificado = cliente_redis.get(name=f"verificado:{email}")
    if not esta_verificado:
        raise HTTPException(status_code=401, detail="No verificado.")

    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="El usuario no existe.")

    cliente_redis.delete(f"verificado:{email}")

    return {
        "mensaje": "¡Sesión iniciada con éxito!",
        "token_simulado": f"jwt-session-token-for-{usuario.username}",
        "usuario": {"username": usuario.username, "email": usuario.email}
    }