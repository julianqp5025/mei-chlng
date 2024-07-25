# *-* coding: utf-8 *-*
# app/utils/settings.py

import os, re

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


# Cargar env vars desde el archivo .env
load_dotenv()


# Creamos una clase que contenga las env vars en variables
class Settings(BaseSettings):
  source_data: str = os.getenv("SOURCE_DATA")
  db_name: str = os.getenv("DB_NAME")
  db_coll: str = os.getenv("DB_COLL")
  db_acce: str = os.getenv("DB_ACCE")
  db_user: str = os.getenv("DB_USER")
  db_pass: str = os.getenv("DB_PASS")
  db_host: str = os.getenv("DB_HOST")
  db_port: str = os.getenv("DB_PORT")

  secret_key: str = os.getenv("SECRET_KEY")
  token_expire: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")