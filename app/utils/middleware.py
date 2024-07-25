# *-* coding: utf-8 *-*
# app/utils/middleware.py

import requests, os
from fastapi import HTTPException
from app.utils.settings import Settings


# Cargamos todo el contenido del archivo settings.py
settings = Settings()


# Validamos si el cliente de PyMongo está instalado
try:
  from pymongo import MongoClient
except ImportError:
  raise ImportError("PyMongo isn't installed")


# Creamos una clase que retorne la conexión a la DB
class MongoDB(object):
  def __init__(self, host=settings.db_host, port=int(settings.db_port), username=settings.db_user, password=settings.db_pass, database_name=None, collection_name=None):
    try:
      self._connection = MongoClient(host=settings.db_host, port=int(settings.db_port), username=settings.db_user, password=settings.db_pass, maxPoolSize=200)
    except Exception as error:
      raise Exception(error)

    self._database = None
    self._collection = None

    if database_name:
      self._database = self._connection[database_name]

    if collection_name:
      self._collection = self._database[collection_name]

  def insert(self, user):
    user_id = self._collection.insert_one(user).inserted_id
    return user_id


# Definimos una función que se encargué de poblar la DB con la info obtenida desde la api: https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios
def populate_info():
  user_url = os.getenv("SOURCE_DATA")
  res = requests.get(url=user_url, verify=False)
  api_data = res.json()

  if res.status_code != 200:
    print("Failed to get api_data:", res.status_code)
  else:
    print("Data...")

  print("[*] Pushing data to MongoDB...")
  mongodb = MongoDB(database_name=settings.db_name, collection_name=settings.db_coll)

  if (mongodb._collection.find_one({"_id": "2"})) is not None:
    raise HTTPException(status_code=404, detail=f"There are duplicated records")

  for value in api_data:
    print("[!] Inserting - id[", value["id"], "]")
    mongodb.insert(
      {
        "_id": value["id"],
        "fec_alta": value["fec_alta"],
        "user_name": value["user_name"],
        "codigo_zip": value["codigo_zip"],
        "credit_card_num": value["credit_card_num"],
        "credit_card_ccv": value["credit_card_ccv"],
        "cuenta_numero": value["cuenta_numero"],
        "direccion": value["direccion"],
        "geo_latitud": value["geo_latitud"],
        "geo_longitud": value["geo_longitud"],
        "color_favorito": value["color_favorito"],
        "foto_dni": value["foto_dni"],
        "ip": value["ip"],
        "auto": value["auto"],
        "auto_modelo": value["auto_modelo"],
        "auto_tipo": value["auto_tipo"],
        "auto_color": value["auto_color"],
        "cantidad_compras_realizadas": value["cantidad_compras_realizadas"],
        "avatar": value["avatar"],
        "fec_birthday": value["fec_birthday"]
      }
    )

  return {"msg": "info populated!!!"}