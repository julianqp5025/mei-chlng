# *-* coding: utf-8 *-*
# app/models/user_model.py

from typing import List
from pydantic import BaseModel, Field, SecretStr


# Adaptamos el modelo de datos, su administración de usuarios/info obtenida y guardada en la DB, con los endpoints: /api/v1/users - /api/v1/user (GET, POST, PUT, DELETE)
class UserModel(BaseModel):
  id: str = Field(alias="_id")
  fec_alta: str = Field(...)
  user_name: str = Field(...)
  codigo_zip: str = Field(...)
  credit_card_num: SecretStr # Determina que el dato es confidencial y no debe ser mostrado en las respuestas de la API
  credit_card_ccv: SecretStr # Determina que el dato es confidencial y no debe ser mostrado en las respuestas de la API
  cuenta_numero: SecretStr # Determina que el dato es confidencial y no debe ser mostrado en las respuestas de la API
  direccion: str = Field(...)
  geo_latitud: str = Field(...)
  geo_longitud: str = Field(...)
  color_favorito: str = Field(...)
  foto_dni: str = Field(...)
  ip: str = Field(...)
  auto: str = Field(...)
  auto_modelo: str = Field(...)
  auto_tipo: str = Field(...)
  auto_color: str = Field(...)
  cantidad_compras_realizadas: int = Field(...)
  avatar: str = Field(...)
  fec_birthday: str = Field(...)


class UserCollection(BaseModel):
  users: List[UserModel]


class UserUpdateModel(BaseModel):
  user_name: str = Field(...)
  codigo_zip: str = Field(...)
  credit_card_num: str = Field(...)
  credit_card_ccv: str = Field(...)
  cuenta_numero: str = Field(...)
  direccion: str = Field(...)
  color_favorito: str = Field(...)
  auto: str = Field(...)
  auto_modelo: str = Field(...)
  auto_tipo: str = Field(...)
  auto_color: str = Field(...)
  fec_birthday: str = Field(...)