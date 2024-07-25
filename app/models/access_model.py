# *-* coding: utf-8 *-*
# app/models/access_model.py

from pydantic import BaseModel, Field, EmailStr


# Creamos el modelo de datos para la creación de accesos en el endpoint: /api/v1/access con usuario y contraseña
class AccessBase(BaseModel):
  email: EmailStr = Field(
    ...,
    example="me@me.com"
  )
  username: str = Field(
    ...,
    min_length=3,
    max_length=50,
    example="YourUsername"
  )


class UserAccess(AccessBase):
  id: int = Field(
    ...,
    example="5"
  )


class UserAccessRegister(AccessBase):
  password: str = Field(
    ...,
    min_length=8,
    max_length=64,
    example="StrongPassPlease"
  )