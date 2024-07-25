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
### 3.1. Construir la imagen de ```docker``` que será utilizada en el ```docker-compose.yaml```
Ubicarse en la raíz del repositorio y ejecutar el comando 👇
```bash
docker buildx b -t mei-chlng .
```

### 3.2. Ejecutar ```docker compose```
>[!TIP]
>En algunos casos se usa el comando ```docker compose up``` en vez de ```docker-compose up```.

Posteriormente ejecutar el comando 👇
```bash
docker compose up
```
>[!CAUTION]
>Ejecutar en otra terminal: ```sudo chmod -R 777 mongodata```, para dar permiso a la escritura dentro del folder de los datos de mongodb, de lo contrario se estará reiniciando constantemente el contenedor ```mongo-server```.


## 4. Ingresar a la API para consumir sus endpoints
Ingresar a https://localhost:8081/docs
