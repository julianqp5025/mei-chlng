# *-* coding: utf-8 *-*
# app/auth/auth_service.py

import json
from datetime import datetime, timedelta
from typing import Optional
from pymongo import MongoClient

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.models.token_model import TokenData
from app.models.access_model import UserAccessRegister
from app.utils.settings import Settings


# Cargamos todo el contenido del archivo settings.py
settings = Settings()


# Definimos el valor de las vars con lo obtenido del archivo settings.py
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_expire


# Definimos el esquema para criptografía y el endpoint al cuál serán enviadas las respuestas: /api/v1/login
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")


# Definimos la conexión a la DB con sus parámetros cargados desde las env vars que tiene el archivo settings.py
conn = MongoClient(host=settings.db_host, port=int(settings.db_port), username=settings.db_user, password=settings.db_pass, maxPoolSize=200)
db = conn["mei_users"]
access_collection = db["access"]


# Función que convierte las respuestas de la API a JSON
def convert_to_json(str_to_json):
  return json.loads(json.dumps(str_to_json, default=str))


# Función para validar el password de acceso con el esquema de criptografía definido
def verify_password(plain_password, password):
  return pwd_context.verify(plain_password, password)


# Función para generar el hash del password que será almacenado en la DB al realizar el registro del acceso para la API
def get_password_hash(password):
  return pwd_context.hash(password)


# Función para crear el usuario con acceso a la API y que podrá generar tokens
def create_access(user: UserAccessRegister):
  if (convert_to_json(access_collection.find_one({"username": user.username}))) is not None:
    raise HTTPException(status_code=409, detail=f"Duplicate record for id: {user.username}")
  
  new_access = {
    "username": user.username,
    "email": user.email,
    "password": get_password_hash(user.password)
  }

  access_collection.insert_one(new_access)

  return new_access


# Función que retorna el usuario de acceso cuando éste existe en la DB
def get_access(username: str):
  if (user := convert_to_json(access_collection.find_one({"username": username}))) is not None:
    return user

  raise HTTPException(status_code=404, detail=f"Username {username} not found")


# Función para validar el usuario de acceso (username & password)
def authenticate_access(username: str, password: str):
  user = get_access(username)
  if not user:
    return False
  if not verify_password(password, user["password"]):
    return False
  return user


# Función para crear el token de acceso a la API y su la expiración
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


# Función para generar el token de acceso a la API
def generate_token(username, password):
  user = authenticate_access(username, password)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect email/username or password",
      headers={"WWW-Authenticate": "Bearer"},
    )
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  return create_access_token(
    data={"sub": user["username"]}, expires_delta=access_token_expires
  )


# Función que limita/permite el acceso a los endpoints que reciban su estructura como parámetro, ex: async def list_users(current_access: UserAccess = Depends(auth_service.get_current_access))
async def get_current_access(token: str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
    token_data = TokenData(username=username)
  except JWTError:
    raise credentials_exception

  user = get_access(username=token_data.username)
  if user is None:
    raise credentials_exception
  return user