from fastapi import FastAPI

from app.dishes.router import dish_router
from app.menu.router import menu_router
from app.submenu.router import submenu_router
from create_tables import init_models

app = FastAPI()


@app.on_event('startup')  # Пересоздает таблицы в бд # TODO onrelease delete
async def create_tables():
    await init_models()


app.include_router(menu_router, prefix='/api/v1', tags=['menus'])
app.include_router(submenu_router, prefix='/api/v1/menus/{menu_id}', tags=['submenus'])
app.include_router(dish_router, prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}', tags=['dishes'])
