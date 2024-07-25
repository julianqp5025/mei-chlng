# Arquitectura de la aplicación
## Código
El siguiente gráfico muestra cómo es obtenida y almacenada la información que será expuesta a los usuarios por medio de una API interna.
![meli-challenge](https://github.com/user-attachments/assets/28e7f4f5-4222-41b4-98c1-8ba2b0b895b1)

## Infra (K8s)
Flujo de consumo y exposición de información usando un cluster de Kubernetes (K8s).
![meli-challenge (1)](https://github.com/user-attachments/assets/daca0d59-38a2-4d29-837b-4251e9a23e00)

# Estructura de la aplicación
## Librerías principales
| | Nombre | Descripción |
| --- | --- | --- |
| ✔️ | Excalidraw | Diseño de diagramas de arquitectura |
| ✔️ | FastAPI | Desarrollo de APIs |
| ✔️ | passlib | Criptografía |
| ✔️ | python-jose | JSON Web Tokens - JWT |

## Carpetas
| :warning: WARNING           |
|:----------------------------|
| Los archivos ```privkey.pem``` & ```cert.pem``` son para ejecutar tests y no deben usarse en ambientes productivos |
```bash
├── app
│   ├── api.py
│   ├── auth
│   │   └── auth_service.py
│   ├── models
│   │   ├── access_model.py
│   │   ├── token_model.py
│   │   └── user_model.py
│   └── utils
│       ├── middleware.py
│       └── settings.py
├── cert.pem
├── Dockerfile
├── main.py
├── privkey.pem
├── README.md
└── requirements.txt
```

# ¿Cómo ejecutar la aplicación en local?

>[!TIP]
> Recomendamos iniciar la aplicación con el método ```docker compose up``` (**Paso 3**), tiene información persistente y menos fricción a la hora de levantar la API.

## 1. Configurar archivo .env
Crear el archivo ```.env``` en la raíz del repositorio (sugerencia de ```.env``` 👇)
```text
# DB settings
SOURCE_DATA=https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios
DB_HOST=mongo-server # Si ejecutas con docker compose usa: mongo-server, si ejecutas el fichero main.py usa: localhost
DB_PORT=27017
DB_NAME=mei_users
DB_COLL=users
DB_ACCE=access
DB_USER=user
DB_PASS=pass

# Auth
ACCESS_TOKEN_EXPIRE_MINUTES=1440 # 24h / 1Day
SECRET_KEY=d867e9ea308ec781acb0166f23ff6b6ad90c52d515a0758f30fa65fea8077241 # Generar nuevo secret: openssl rand -hex 32
```

Para crear su propio ```SECRET_KEY``` puede usar el siguiente comando
```bash
openssl rand -hex 32
```


## 2. Ejecutar aplicación por tu propio método
### 2.1. Ejecutar el contenedor de docker para MongoDB
Este recibe las variables ```MONGODB_INITDB_DATABASE```, ```MONGODB_INITDB_ROOT_USERNAME``` & ```MONGODB_INITDB_ROOT_PASSWORD``` para configurarlo.
```bash
docker run --name mongodb -d -p 27017:27017 -e MONGODB_INITDB_DATABASE=mei_users -e MONGODB_INITDB_ROOT_USERNAME=user -e MONGODB_INITDB_ROOT_PASSWORD=pass mongodb/mongodb-community-server
```

### 2.2. Crear entorno virtual de Python e instalar librerías requeridas
Ubicarse en la raíz del repositorio y ejecutar los comandos 👇.
>[!TIP]
>En algunos casos se usa el comando ```python3``` en vez de ```python```.
```bash
python -m venv env
source env/bin/activate
pip install --no-cache-dir -r requirements.txt
```

### 2.3. Inicializar la aplicación
```bash
python main.py
```


## 3. Ejecutar aplicación usando ```docker compose up``` (```docker-compose up```)
## 3.1. Crear la carpeta ```mongodata``` para almacenar los datos de manera persistente.
Ubicarse en la raíz del repositorio y ejecutar el comando 👇
```bash
mkdir -p mongodata
chmod -R 777 mongodata
```

### 3.2. Construir la imagen de ```docker``` que será utilizada en el ```docker-compose.yaml```
```bash
docker buildx b -t mei-chlng .
```

### 3.3. Ejecutar ```docker compose```
>[!TIP]
>En algunos casos se usa el comando ```docker compose up``` en vez de ```docker-compose up```.

Posteriormente ejecutar el comando 👇
```bash
docker compose up
```


## 4. Ingresar a la API para consumir sus endpoints
### 4.1. Estamos usando un SSL autorfirmado, entonces debemos aceptar el riesgo y continuar hacía el endpoint
Para validar si la API se está ejecutando correctamente visita: ```https://localhost:8081/api/v1/healthcheck```
Clic en **Advanced** > **Continue to localhost (unsafe)**.
![Screenshot from 2024-07-25 09-54-05](https://github.com/user-attachments/assets/7baa0c3a-21ea-449a-bd36-592fc4e75ba9)

**```/api/v1/healthcheck```**

![Screenshot from 2024-07-25 11-54-45](https://github.com/user-attachments/assets/000a1ebf-d7eb-4b10-b54e-430962dbb362)


### 4.2. Tests de los endpoint usando los docs creados por FastAPI usando el estándar de OpenAPI
Ingresar a ```https://localhost:8081/docs```
![Screenshot_25-7-2024_10234_localhost](https://github.com/user-attachments/assets/b61bcf19-9bcf-45e2-96b2-a2dc055e11ce)

### 4.3. Insertar la información en la DB desde el endpoint externo
Para ello ejecutaremos el endpoint ```/api/v1/populated_db``` y su método POST.
Clic en **/api/v1/populated_db** > **Try it out** > **Execute**
![Screenshot from 2024-07-25 10-08-28](https://github.com/user-attachments/assets/861a378b-885e-421a-b329-c78f0d65aa39)

Si todo se ejecuta correctamente podremos el mensaje ```{"msg": "info populated!!!"}``` y en la DB podremos verla.
![Screenshot from 2024-07-25 11-57-29](https://github.com/user-attachments/assets/f553e291-a5fc-468b-b872-691939de9dfc)

![Screenshot from 2024-07-25 11-57-54](https://github.com/user-attachments/assets/bd426626-5f9e-4a86-8a7b-6a59ec006783)

### 4.4. Conexión y validación de información en la DB
En este caso usamos el cliente MongoDB Compass para conectarnos a la DB.
![Screenshot from 2024-07-25 10-12-02](https://github.com/user-attachments/assets/911f2676-bf5d-4446-8488-05cbdf073b26)

Validamos la información obtenida desde la fuente externa.
![Screenshot from 2024-07-25 10-14-58](https://github.com/user-attachments/assets/9493a3c0-d044-48f1-b0cd-2e8dd9cfb084)

### 4.5. Explorar los endpoints de administración de usuarios
Dichos endpoints están asegurados por medio de JWT, en caso de querer consultarlos sin autenticación (se identifican por el candado), obtendremos el mensaje ```{"detail": "Not authenticated"}```
![Screenshot from 2024-07-25 10-18-01](https://github.com/user-attachments/assets/8a4f1a7d-5f02-4f89-9117-bb6abbf1d5c0)

Ejecutarlos sin autenticación:
![Screenshot from 2024-07-25 10-19-47](https://github.com/user-attachments/assets/cbd27e72-4c00-4e5b-9691-a21b2480312c)

### 4.6. Crear usuario de acceso para consumir los endpoints
Para crear dichos accesos tenemos el endpoint ```/api/v1/access``` y ejecutamos su método POST.
![Screenshot from 2024-07-25 10-22-52](https://github.com/user-attachments/assets/e22925d2-24fb-4df6-a4d4-18f496eda9e5)

Validamos en la DB si el usuario fue creado:
Refrescamos la lista de DBs en MongoDB Compass y exploramos la collection ```access```, allí veremos el usuario creado y el hash para el password usando la librería ```passlib``` de Python.
![Screenshot from 2024-07-25 10-26-35](https://github.com/user-attachments/assets/5f2d0a40-ff00-4e43-aa00-b1570dfcf260)

### 4.7. Autenticando con JWT
Para crear el ```bearer token``` ejecutaremos el endpoint ```/api/v1/login``` o desde el botón ```Authorize``` ubicado en la parte superior derecha del sitio web.
![Screenshot from 2024-07-25 10-29-18](https://github.com/user-attachments/assets/5c5fedc9-4aec-4887-84be-d72ad1eeca4c)

**4.7.1. Ejecutando endpoint ```/api/v1/login```:**
![Screenshot from 2024-07-25 10-30-38](https://github.com/user-attachments/assets/a54139cf-4d3f-47df-9a8d-0feb794c81d2)

Si la respuesta es correcta, obtendremos el token temporal (24h / 1Día) para explorar los endpoints de la API:
![Screenshot from 2024-07-25 10-32-06](https://github.com/user-attachments/assets/ca8359a1-3bd8-4226-9bad-fa867aa91788)

**4.7.2. Usando el botón ```Authorize```:**
Hacer clic en el botón ```Authorize``` ubicado en la parte superior derecha del sitio web e ingresar los datos del usuario de acceso anteriormente creados (paso 4.6).

Veremos datos de confirmación para la sesión iniciada en caso de que los datos estén correctos:
![Screenshot from 2024-07-25 10-35-32](https://github.com/user-attachments/assets/f5d1ea61-9407-4c53-9cec-b244076b9933)
Clic en ```Close```

En caso contrario, veremos un mensaje de error con los datos ingresados:
![Screenshot from 2024-07-25 10-37-02](https://github.com/user-attachments/assets/d7f4b6b2-2922-47f0-9c7d-c38cf33b83f9)

### 4.8. Explorando los endpoints luego de la autenticación
Una vez los pasos de la sección 4.7 estén ejecutados correctamente, podremos ver que los métodos que anteriormente tenían un **candado abierto**, ahora tienen un **candado cerrado**, quiere decir que estamos autenticados correctamente.
![Screenshot from 2024-07-25 10-40-37](https://github.com/user-attachments/assets/51de9e36-063b-4d6c-bfc2-089e76ae7a18)

El modelo de datos para la API protege los campos de **```credit_card_num```, ```credit_card_ccv```, ```cuenta_numero```**, ya que fueron considerados datos críticos durante el ejercicio.

**A partir de aquí podremos explorar los endpoints:**

| Endpoint | Descripción |
| --- | --- |
| ```/api/v1/users``` | Endpoint para listar todos los usuarios de la DB |
| ```/api/v1/user/{username}``` [GET] | Endpoint para LISTAR un usuario por ```username``` |
| ```/api/v1/user/{username}``` [PUT] | Endpoint para ACTUALIZAR un usuario por ```username``` |
| ```/api/v1/user/{username}``` [DELETE] | Endpoint para ELIMINAR un usuario por ```username``` |
| ```/api/v1/user``` [POST] | Endpoint para CREAR usuarios |

**4.8.1. Listar todos los usuarios de la DB, endpoint: ```/api/v1/users```**
![Screenshot from 2024-07-25 11-01-56](https://github.com/user-attachments/assets/62f8ca25-d78e-49d2-b868-1db375cf55bd)

**4.8.2. Listar usuario por ```username```**

Para el ejemplo trabajaremos con el usuario: ```Junior39```

**4.8.2.1. Listar datos de ```Junior39``` , endpoint: ```/api/v1/user/{username}``` [GET]**
![Screenshot from 2024-07-25 11-05-34](https://github.com/user-attachments/assets/2f77192c-29aa-4955-a6b6-aa42daf97972)

**4.8.2.2. Actualizar datos de ```Junior39```, endpoint: ```/api/v1/user/{username}``` [PUT]**
![Screenshot from 2024-07-25 11-11-42](https://github.com/user-attachments/assets/199a8319-d0d8-4893-a8bf-8b2f17bbcfc5)

Validamos los cambios con el paso 4.8.2.1:
![Screenshot from 2024-07-25 11-12-51](https://github.com/user-attachments/assets/e28a1c47-ca71-40db-a500-19f7a5927c04)

**4.8.2.3. Eliminar usuario ```Junior39```, endpoint: ```/api/v1/user/{username}``` [DELETE]**
![Screenshot from 2024-07-25 11-14-37](https://github.com/user-attachments/assets/2c4c75ac-8a1a-4067-a8dd-5b365c9b146d)

Validamos los cambios con el paso 4.8.2.1:
![image](https://github.com/user-attachments/assets/864f0ddb-dd0a-4bfa-80e5-be853995948d)

Validamos los cambios con en MongoDB:
![Screenshot from 2024-07-25 11-16-40](https://github.com/user-attachments/assets/0e8573bb-52cd-4380-a261-1ee8467208ad)

**4.8.2.4. Creamos el usuario ```Junior39```, endpoint: ```/api/v1/user``` [POST]**:
![Screenshot from 2024-07-25 11-51-08](https://github.com/user-attachments/assets/82f850e9-7acd-4758-baa7-85b9c7088307)

Respuesta:
![Screenshot from 2024-07-25 11-51-59](https://github.com/user-attachments/assets/ec513ccc-ea51-4fff-bc3a-889e59ba3ffd)

Validamos los cambios con en MongoDB:
![Screenshot from 2024-07-25 11-52-32](https://github.com/user-attachments/assets/9e9ab99a-89c7-47fb-a6e9-cae6eb16c027)


## Oportunidades de mejora
El proyecto fue desarrollado siguiendo los lineamientos de **Service Organization Control Type 2 (SOC 2)**.

Fuente: https://loadforge.com/guides/load-testing/setting-up-your-fastapi-environment-for-soc2-security-standards

👇
- Implementar SSL para conectarse con MongoDB desde un cliente DB: https://www.mongodb.com/docs/manual/tutorial/configure-ssl/.
- Encriptación en reposo (Encrypting Data At Rest) usando [Vautl](https://www.vaultproject.io/), [AWS KMS](https://aws.amazon.com/kms/), etc.
- Captación de logs implícito desde el código (ex: ```loguru```) y que plataformas como [Prometheus](https://prometheus.io/), [Grafana](https://grafana.com/) o [Datadog](https://www.datadoghq.com/) obtengan más información de eventos.
- Implementar unit-tests con librerías como pyTest.
- En caso de publicar el proyecto en internet, tener en cuenta el estándar [OWASP](https://owasp.org/www-project-top-ten/) para apliaciones web.


## URLs consultadas para el desarrollo
- Liberar recursos del PC por usar Docker 🥲 : https://depot.dev/blog/docker-clear-cache
- Usar MongoDB con Docker: https://www.mongodb.com/resources/products/compatibilities/docker
- Generar y autofirmar SSL: https://www.suse.com/es-es/support/kb/doc/?id=000018152 - https://letsencrypt.org/docs/certificates-for-localhost/
- Implementar SSLs para ```uvicorn``` server: https://stackoverflow.com/questions/69207474/enable-https-using-uvicorn
- Integrar JWT al desarrollo: https://cosasdedevs.com/posts/autenticacion-login-jwt-fastapi/ - https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- Sobre PCI DSS para datos crítica: https://drata.com/blog/pci-compliance-checklist
- Manejo de status_code en HTTP: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- Sobre librería pymongo: https://pymongo.readthedocs.io/en/stable/tutorial.html
- Tipos de datos extra para modelos de FastAPI: https://fastapi.tiangolo.com/tutorial/extra-models/


## Errores recurrentes durante el desarrollo
- ```ObjectId object is not iterable error```: https://sentry.io/answers/fastapi-and-mongodb-objectid-object-is-not-iterable-error/
- ```"message": "input must be a 24 character hex string, 12 byte Uint"```: https://community.postman.com/t/message-input-must-be-a-24-character-hex-string-12-byte-uint/62379
- ```Permission denied [system:13]: \"/data/db/journal\""}}```: https://www.reddit.com/r/mongodb/comments/1c87s15/permission_denied_system13_datadbjournal/
- ```bson.errors.InvalidDocument: cannot encode object: SecretStr('**********'), of type: <class 'pydantic.types.SecretStr'>```, ```msg': 'Input should be a valid string SecretStr```: https://docs.pydantic.dev/2.0/usage/types/secrets/
