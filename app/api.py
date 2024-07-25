# *-* coding: utf-8 *-*
# app/api.py

import json
from pymongo import MongoClient
from pymongo import ReturnDocument
from fastapi import FastAPI, Body, HTTPException, Depends, status
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm

from app.utils.settings import Settings
from app.utils.middleware import populate_info
from app.models.user_model import UserModel, UserCollection, UserUpdateModel
from app.models.token_model import Token
from app.models.access_model import UserAccess, UserAccessRegister, AccessBase
from app.auth import auth_service


# Cargamos todo el contenido del archivo settings.py
settings = Settings()


# Inicializamos la API
app = FastAPI(title="Data Users API")


# Definimos la conexión a la DB con sus parámetros cargados desde las env vars que tiene el archivo settings.py
conn = MongoClient(host=settings.db_host, port=int(settings.db_port), username=settings.db_user, password=settings.db_pass, maxPoolSize=200)
db = conn["mei_users"]
users_collection = db["users"]


# Función que convierte las respuestas de la API a JSON
def convert_to_json(str_to_json):
  return json.loads(json.dumps(str_to_json, default=str))


# Función/Endpoint que reporta si la API está funcional y accesible
@app.get("/api/v1/healthcheck", response_description="Healthcheck", response_model_by_alias=False, tags=["Manage Users"])
async def healthcheck():
  return {"msg": "Hell Yeah!!!"}


# Función/Endpoint para poblar la DB desde la API haciendo su llamado. No requiere autenticación.
@app.post("/api/v1/populate_db", response_description="Populate DB", response_model_by_alias=False, tags=["Manage Info"])
async def populate_db():
  return populate_info()


# Función/Endpoint para CREAR usuarios con acceso a la API y que podrán generar el bearer token.
@app.post("/api/v1/access", response_description="Create Access", response_model=AccessBase, status_code=status.HTTP_201_CREATED, tags=["Manage Access"])
async def create_access(access: UserAccessRegister = Body(...)):
  return auth_service.create_access(access)


# Función/Endpoint para AUTENTICAR el usuario con acceso y que retorna el bearer token para ser usado en las peticiones a los endpoints de usuario.
@app.post("/api/v1/login", response_description="Login", response_model=Token, tags=["Manage Access"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
  access_token = auth_service.generate_token(form_data.username, form_data.password)
  return Token(access_token=access_token, token_type="bearer")


# Función/Endpoint restringido/a con bearer token que lista todos los usuarios guardados en la DB. Requiere autenticación.
@app.get("/api/v1/users", response_description="List all users", response_model=UserCollection, response_model_by_alias=False, tags=["Manage Users"])
async def list_users(current_access: UserAccess = Depends(auth_service.get_current_access)) -> UserCollection:
  return UserCollection(users=users_collection.find())


# Función/Endpoint restringido/a con bearer token que obtiene un usuario por username guardados en la DB. Requiere autenticación.
@app.get("/api/v1/user/{username}", response_description="Get user", response_model=UserModel, response_model_by_alias=False, tags=["Manage Users"])
async def get_user(username: str, current_access: UserAccess = Depends(auth_service.get_current_access)) -> UserModel:
  if (user := convert_to_json(users_collection.find_one({"user_name": username}))) is not None:
    return user

  raise HTTPException(status_code=404, detail=f"User {username} not found")


# Función/Endpoint restringido/a con bearer token para crear un usuario y guardarlo en la DB. Requiere autenticación.
@app.post("/api/v1/user", response_description="Create user", response_model=UserModel, status_code=status.HTTP_201_CREATED, response_model_by_alias=True, tags=["Manage Users"])
async def create_user(user: UserModel = Body(...), current_access: UserAccess = Depends(auth_service.get_current_access)):
  if (convert_to_json(users_collection.find_one({"_id": user.id}))) is not None:
    raise HTTPException(status_code=409, detail=f"Duplicate record for id: {user.id}")

  new_user = users_collection.insert_one(user.model_dump(by_alias=True))
  create_user = users_collection.find_one({"_id": new_user.inserted_id})
  return create_user


# Función/Endpoint restringido/a con bearer token para actualizar un usuario por username y guardarlo en la DB. Requiere autenticación.
@app.put("/api/v1/user/{username}", response_description="Update user", response_model=UserUpdateModel, response_model_by_alias=False, tags=["Manage Users"])
async def update_user(username: str, user: UserUpdateModel = Body(...), current_access: UserAccess = Depends(auth_service.get_current_access)):
  user = {
    u: v for u, v in user.model_dump(by_alias=True).items() if v is not None
  }

  if len(user) >= 1:
    update_user = users_collection.find_one_and_update(
      {"user_name": username},
      {"$set": user},
      return_document = ReturnDocument.AFTER,
    )

    if update_user is not None:
      return update_user
    else:
      raise HTTPException(status_code=404, detail=f"Username {username} not found")
    
  if (existing_user := users_collection.find_one({"user_name": username})) is not None:
    return existing_user

  raise HTTPException(status_code=404, detail=f"Username {username} not found")


# Función/Endpoint restringido/a con bearer token que elimina un usuario por username de la DB. Requiere autenticación.
@app.delete("/api/v1/user/{username}", response_description="Delete user", response_model_by_alias=False, tags=["Manage Users"])
async def delete_user(username: str, current_access: UserAccess = Depends(auth_service.get_current_access)):
  delete_user = users_collection.delete_one({"user_name": username})

  if delete_user.deleted_count == 1:
    return Response(status_code=status.HTTP_204_NO_CONTENT)

  raise HTTPException(status_code=404, detail=f"User {username} not found")