# FastAPI Project Setup

## 1. Create the project directory

```bash
mkdir my_fastapi_project
cd my_fastapi_project
```

## 2. Create a virtual environment

```bash
python3 -m venv venv
```

## 3. Activate the virtual environment

### Linux 

```bash
source venv/bin/activate
```

## 4. Install FastAPI and dependencies

```bash
pip install "fastapi[standard]"
```

## 5. Save dependencies

```bash
pip freeze > requirements.txt
```

## 6. Create the application

Create a file named `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

## 7. Run the application

```bash
fastapi dev main.py
```

or

```bash
uvicorn main:app --reload
```

## 8. Open the application

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

## 9. Reinstall dependencies on another machine

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 10. Git Ignore

Create a `.gitignore` file:

```gitignore
venv/
__pycache__/
*.pyc
.env
```
