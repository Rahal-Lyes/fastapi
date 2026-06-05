from fastapi import FastAPI
app=FastAPI()

books = [
    {"name": "Python"},
    {"name": "C++"},
    {"name": "C#"}
]
@app.get("/api")
async def get_books():
  return books