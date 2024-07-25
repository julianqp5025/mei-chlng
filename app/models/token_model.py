# *-* coding: utf-8 *-*
# app/models/token_model.py

from pydantic import BaseModel
from typing import Optional


# Creamos el modelo de datos para la generación del token con autenticación en el endpoint: /api/v1/login con usuario y contraseña
class Token(BaseModel):
  access_token: str
  token_type: str


class TokenData(BaseModel):
  username: Optional[str] = None