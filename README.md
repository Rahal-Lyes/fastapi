# FastAPI --- Notes d'apprentissage

> Document personnel pour apprendre, pratiquer et retrouver rapidement
> les notions importantes de FastAPI.

------------------------------------------------------------------------

## 1. Objectif

Cette documentation me sert à :

-   comprendre FastAPI progressivement ;
-   noter les concepts importants ;
-   conserver des exemples que je peux réutiliser ;
-   documenter mes erreurs et leurs solutions ;
-   construire une base de référence pour mes futurs projets.

------------------------------------------------------------------------

# 2. Installation

## Créer un environnement virtuel

``` bash
python3 -m venv venv
source venv/bin/activate
```

## Installer FastAPI et Uvicorn

``` bash
pip install fastapi uvicorn
```

Vérifier :

``` bash
pip show fastapi
pip show uvicorn
```

------------------------------------------------------------------------

# 3. Premier serveur FastAPI

Créer `main.py` :

``` python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello FastAPI"}
```

Lancer le serveur :

``` bash
uvicorn main:app --reload
```


``` bash
fastapi run main.py
```
Explication :

-   `main` = fichier `main.py`
-   `app` = variable contenant `FastAPI()`
-   `--reload` = redémarre automatiquement le serveur pendant le
    développement.

URL :

``` text
http://127.0.0.1:8000
```

Documentation automatique :

``` text
http://127.0.0.1:8000/docs
```

Documentation alternative :

``` text
http://127.0.0.1:8000/redoc
```

------------------------------------------------------------------------

# 4. Routes HTTP

## GET

``` python
@app.get("/users")
def get_users():
    return [
        {"id": 1, "name": "Lyes"},
        {"id": 2, "name": "Yazid"}
    ]
```

## POST

``` python
@app.post("/users")
def create_user():
    return {"message": "User created"}
```

## PUT

``` python
@app.put("/users/{user_id}")
def update_user(user_id: int):
    return {"message": f"User {user_id} updated"}
```

## DELETE

``` python
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {"message": f"User {user_id} deleted"}
```

------------------------------------------------------------------------

# 5. Path Parameters

Le paramètre fait partie de l'URL.

``` python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

Exemple :

``` text
GET /users/10
```

Résultat :

``` json
{
  "user_id": 10
}
```

FastAPI vérifie automatiquement que `user_id` est un entier.

------------------------------------------------------------------------

# 6. Query Parameters

Les query parameters sont placés après `?`.

``` python
@app.get("/users")
def get_users(page: int = 1, limit: int = 10):
    return {
        "page": page,
        "limit": limit
    }
```

Exemple :

``` text
/users?page=2&limit=20
```

------------------------------------------------------------------------

# 7. Paramètre obligatoire

``` python
@app.get("/search")
def search(q: str):
    return {"query": q}
```

Exemple :

``` text
/search?q=fastapi
```

Ici `q` est obligatoire.

------------------------------------------------------------------------

# 8. Paramètre optionnel

``` python
from typing import Optional

@app.get("/search")
def search(q: Optional[str] = None):
    return {"query": q}
```

Ou avec Python moderne :

``` python
@app.get("/search")
def search(q: str | None = None):
    return {"query": q}
```

------------------------------------------------------------------------

# 9. Pydantic et les modèles

Pydantic permet de définir la structure des données.

``` python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int
```

Utilisation :

``` python
@app.post("/users")
def create_user(user: User):
    return user
```

Requête JSON :

``` json
{
  "name": "Lyes",
  "email": "lyes@example.com",
  "age": 24
}
```

FastAPI valide automatiquement les données.

------------------------------------------------------------------------

# 10. Response Model

On peut contrôler les données retournées par l'API.

``` python
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    return {
        "id": user_id,
        "name": "Lyes",
        "email": "lyes@example.com",
        "password": "secret"
    }
```

Le champ `password` ne sera pas retourné car il n'existe pas dans
`UserResponse`.

------------------------------------------------------------------------

# 11. Status Codes

``` python
from fastapi import status

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    return user
```

Quelques codes utiles :

  Code   Signification
  ------ -----------------------
  200    OK
  201    Created
  204    No Content
  400    Bad Request
  401    Unauthorized
  403    Forbidden
  404    Not Found
  422    Validation Error
  500    Internal Server Error

------------------------------------------------------------------------

# 12. HTTPException

Pour retourner une erreur :

``` python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):

    if user_id != 1:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": 1,
        "name": "Lyes"
    }
```

------------------------------------------------------------------------

# 13. Headers

Lire un header :

``` python
from fastapi import Header

@app.get("/headers")
def read_headers(user_agent: str | None = Header(default=None)):
    return {
        "user_agent": user_agent
    }
```

------------------------------------------------------------------------

# 14. Cookies

``` python
from fastapi import Cookie

@app.get("/cookies")
def read_cookie(session_id: str | None = Cookie(default=None)):
    return {
        "session_id": session_id
    }
```

------------------------------------------------------------------------

# 15. Form Data

Pour recevoir des données provenant d'un formulaire :

``` bash
pip install python-multipart
```

``` python
from fastapi import Form

@app.post("/login")
def login(
    username: str = Form(),
    password: str = Form()
):
    return {
        "username": username
    }
```

------------------------------------------------------------------------

# 16. Upload de fichiers

``` python
from fastapi import UploadFile, File

@app.post("/upload")
async def upload_file(file: UploadFile = File()):
    return {
        "filename": file.filename,
        "content_type": file.content_type
    }
```

Pour plusieurs fichiers :

``` python
from typing import List

@app.post("/uploads")
async def upload_files(files: List[UploadFile] = File()):
    return [
        {"filename": file.filename}
        for file in files
    ]
```

------------------------------------------------------------------------

# 17. async / await

FastAPI supporte les fonctions asynchrones.

``` python
@app.get("/async")
async def async_example():
    return {"message": "Hello async"}
```

Exemple avec une opération asynchrone :

``` python
import asyncio

@app.get("/wait")
async def wait_example():
    await asyncio.sleep(1)
    return {"message": "Finished"}
```

------------------------------------------------------------------------

# 18. APIRouter

Pour organiser une grande application.

Structure :

``` text
app/
├── main.py
├── routers/
│   ├── users.py
│   └── reports.py
├── models/
├── schemas/
└── services/
```

`routers/users.py` :

``` python
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
def get_users():
    return {"users": []}
```

`main.py` :

``` python
from fastapi import FastAPI
from routers.users import router as users_router

app = FastAPI()

app.include_router(users_router)
```

------------------------------------------------------------------------

# 19. Dépendances

FastAPI possède un système de Dependency Injection.

``` python
from fastapi import Depends

def get_current_user():
    return {
        "id": 1,
        "name": "Lyes"
    }

@app.get("/profile")
def profile(user = Depends(get_current_user)):
    return user
```

Concept important :

``` text
Route
  ↓
Depends()
  ↓
Dependency
  ↓
Données nécessaires
```

------------------------------------------------------------------------

# 20. Exemple : connexion à une base de données

Exemple conceptuel avec SQLAlchemy :

``` python
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://user:password@localhost/database"

engine = create_engine(DATABASE_URL)
```

À étudier ensuite :

-   SQLAlchemy
-   sessions
-   models
-   migrations
-   Alembic
-   PostgreSQL

------------------------------------------------------------------------

# 21. CRUD

CRUD signifie :

``` text
Create
Read
Update
Delete
```

Exemple d'API :

``` text
POST   /users
GET    /users
GET    /users/{id}
PUT    /users/{id}
DELETE /users/{id}
```

C'est une structure très fréquente dans les API REST.

------------------------------------------------------------------------

# 22. Authentication

Notions à apprendre :

-   JWT
-   access token
-   refresh token
-   OAuth2
-   password hashing
-   permissions
-   roles

Exemple de flux :

``` text
POST /login
      ↓
username + password
      ↓
validation
      ↓
access token
      ↓
client
      ↓
Authorization: Bearer <token>
      ↓
API
```

------------------------------------------------------------------------

# 23. CORS

Si un frontend Vue.js ou React communique avec FastAPI :

``` python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

À comprendre :

``` text
Frontend
   ↓
HTTP Request
   ↓
FastAPI
   ↓
CORS Middleware
   ↓
Response
```

------------------------------------------------------------------------

# 24. Variables d'environnement

Ne pas mettre les secrets directement dans le code.

Mauvais exemple :

``` python
DATABASE_URL = "postgresql://user:password@server/db"
```

Préférer :

``` text
.env
```

Exemple :

``` env
DATABASE_URL=postgresql://user:password@server/db
SECRET_KEY=my-secret-key
```

Puis utiliser une librairie/configuration adaptée pour charger ces
variables.

------------------------------------------------------------------------

# 25. Documentation OpenAPI

FastAPI génère automatiquement une documentation OpenAPI.

Swagger UI :

``` text
/docs
```

ReDoc :

``` text
/redoc
```

OpenAPI JSON :

``` text
/openapi.json
```

------------------------------------------------------------------------

# 26. Tester une API

Avec Swagger :

``` text
http://127.0.0.1:8000/docs
```

Avec `curl` :

``` bash
curl http://127.0.0.1:8000/
```

POST :

``` bash
curl -X POST \
  http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Lyes","email":"lyes@example.com","age":24}'
```

------------------------------------------------------------------------

# 27. Tests

Installer :

``` bash
pip install pytest httpx
```

Exemple :

``` python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
```

Lancer :

``` bash
pytest
```

------------------------------------------------------------------------

# 28. Middleware

Un middleware peut intercepter les requêtes et réponses.

Exemple :

``` python
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"{request.method} {request.url}")

    response = await call_next(request)

    return response
```

------------------------------------------------------------------------

# 29. Background Tasks

Pour exécuter une tâche après la réponse :

``` python
from fastapi import BackgroundTasks

def send_email(email: str):
    print(f"Sending email to {email}")

@app.post("/register")
def register(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email)

    return {
        "message": "User registered"
    }
```

------------------------------------------------------------------------

# 30. Exemple de petit projet

## API de gestion de tâches

Structure :

``` text
todo-api/
├── app/
│   ├── main.py
│   ├── routers/
│   │   └── tasks.py
│   ├── schemas/
│   │   └── task.py
│   ├── models/
│   │   └── task.py
│   ├── services/
│   └── database.py
├── tests/
│   └── test_tasks.py
├── .env
├── requirements.txt
└── README.md
```

Endpoints :

``` text
POST   /tasks
GET    /tasks
GET    /tasks/{id}
PUT    /tasks/{id}
DELETE /tasks/{id}
```

------------------------------------------------------------------------

# 31. Exemple de documentation d'un endpoint

## POST `/tasks`

Créer une nouvelle tâche.

### Request

``` json
{
  "title": "Apprendre FastAPI",
  "description": "Étudier les dépendances",
  "completed": false
}
```

### Response

``` json
{
  "id": 1,
  "title": "Apprendre FastAPI",
  "description": "Étudier les dépendances",
  "completed": false
}
```

### Status codes

``` text
201 Created
422 Validation Error
```

### À retenir

``` text
Request
  ↓
Pydantic Schema
  ↓
Validation
  ↓
Service
  ↓
Database
  ↓
Response Model
  ↓
JSON
```

------------------------------------------------------------------------

# 32. Mes erreurs / solutions

Utiliser cette section pour noter mes problèmes.

## Erreur : exemple

``` text
ModuleNotFoundError: No module named 'fastapi'
```

### Cause

FastAPI n'est probablement pas installé dans l'environnement virtuel
utilisé.

### Solution

``` bash
source venv/bin/activate
pip install fastapi uvicorn
```

### Ce que j'ai appris

Toujours vérifier quel environnement Python est actif :

``` bash
which python
python --version
pip --version
```

------------------------------------------------------------------------

# 33. Questions à me poser

Quand j'apprends un nouveau concept, je peux noter :

### Concept

``` text
Dependency Injection
```

### Pourquoi ?

``` text
Pourquoi FastAPI utilise Depends() ?
```

### Exemple

``` python
def get_database():
    ...
```

### Quand l'utiliser ?

``` text
Quand plusieurs routes ont besoin de la même ressource ou logique.
```

### Ce que je dois encore comprendre

``` text
Comment gérer correctement une session SQLAlchemy ?
```

------------------------------------------------------------------------

# 34. Checklist d'apprentissage

## Niveau 1 --- Bases

-   [ ] Installer FastAPI
-   [ ] Créer une API
-   [ ] GET
-   [ ] POST
-   [ ] PUT
-   [ ] DELETE
-   [ ] Path parameters
-   [ ] Query parameters
-   [ ] Pydantic
-   [ ] Validation
-   [ ] HTTPException
-   [ ] Swagger / ReDoc

## Niveau 2 --- Organisation

-   [ ] APIRouter
-   [ ] Dependencies
-   [ ] Middleware
-   [ ] CORS
-   [ ] Upload de fichiers
-   [ ] Background Tasks
-   [ ] Configuration
-   [ ] Variables d'environnement

## Niveau 3 --- Base de données

-   [ ] PostgreSQL
-   [ ] SQLAlchemy
-   [ ] Sessions
-   [ ] Models
-   [ ] Relationships
-   [ ] Alembic
-   [ ] Migrations
-   [ ] CRUD

## Niveau 4 --- Sécurité

-   [ ] Password hashing
-   [ ] JWT
-   [ ] Access token
-   [ ] Refresh token
-   [ ] OAuth2
-   [ ] Roles
-   [ ] Permissions
-   [ ] CORS
-   [ ] Validation des entrées

## Niveau 5 --- Production

-   [ ] Docker
-   [ ] Docker Compose
-   [ ] Nginx
-   [ ] HTTPS
-   [ ] PostgreSQL production
-   [ ] Logging
-   [ ] Tests
-   [ ] CI/CD
-   [ ] Deployment
-   [ ] Monitoring

------------------------------------------------------------------------

# 35. Mon journal d'apprentissage

## Date

``` text
YYYY-MM-DD
```

## Sujet étudié

``` text
Exemple : Dependency Injection
```

## Ce que j'ai compris

``` text
...
```

## Exemple que j'ai réalisé

``` python
...
```

## Erreur rencontrée

``` text
...
```

## Solution

``` text
...
```

## Ce que je dois revoir

``` text
...
```

------------------------------------------------------------------------

# 36. Projet pratique final

Pour valider mes connaissances, créer une API complète avec :

``` text
FastAPI
    +
PostgreSQL
    +
SQLAlchemy
    +
Alembic
    +
JWT
    +
Docker
    +
Tests
```

Exemple de projet :

``` text
API de signalement urbain
```

Fonctionnalités :

-   utilisateurs ;
-   authentification ;
-   création de signalements ;
-   catégories ;
-   photos ;
-   localisation GPS ;
-   statuts ;
-   administration ;
-   statistiques ;
-   notifications.

Architecture :

``` text
Vue.js / React Native
          ↓
       REST API
          ↓
        FastAPI
          ↓
       Services
          ↓
      SQLAlchemy
          ↓
      PostgreSQL
```

------------------------------------------------------------------------

# 37. Règle personnelle

> Ne pas seulement lire la documentation. Pour chaque concept, écrire un
> petit exemple, le tester, provoquer une erreur, comprendre l'erreur et
> noter la solution.
