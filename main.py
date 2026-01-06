from api import todo, user
from fastapi import FastAPI

app = FastAPI()
app.include_router(todo.router)
app.include_router(user.router)


@app.get("/")
def health_check():
    return {"status": "ok"}
