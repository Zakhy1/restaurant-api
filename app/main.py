from fastapi import FastAPI

from app.dishes.router import dish_router
from app.menu.router import menu_router
from app.submenu.router import submenu_router

app = FastAPI()


app.include_router(menu_router, prefix='/api/v1', tags=['menus'])
app.include_router(submenu_router, prefix='/api/v1/menus/{menu_id}', tags=['submenus'])
app.include_router(dish_router, prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}', tags=['dishes'])
