from fastapi import FastAPI
from database import Session
from models import Menu

app = FastAPI()
db_session = Session()


@app.get("/api/v1/menus")
async def get_menus():
    menus = db_session.query(Menu).all()

    return {"menus": [menus]}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
