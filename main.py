from fastapi import FastAPI

from database import engine
from menu.crud import MenuOperations
from menu.schema import Menu as MenuSchema
from submenu import crud as submenu_crud

app = FastAPI()


# Меню
@app.get("/api/v1/menus")
async def get_menus():
    menu_crud = MenuOperations(engine)
    menus = menu_crud.get_menus()
    return {"menus": [menus]}


@app.get("/api/v1/menus/{menu_id}")
async def get_menu(menu_id):
    menu_crud = MenuOperations(engine)
    menu = menu_crud.get_menu(menu_id)
    return {"menu": menu}


@app.post("/api/v1/menus")
async def add_menu(menu: MenuSchema):
    menu_crud = MenuOperations(engine)
    result = menu_crud.add_menu_item(menu)
    return {"menu": result}


@app.patch("/api/v1/menus/{menu_id}")
async def edit_menu(menu_id: int, new_data: MenuSchema):
    menu_crud = MenuOperations(engine)
    result = menu_crud.edit_menu_item(menu_id, new_data)
    return {"menu": result}


@app.delete("/api/v1/menus/{menu_id}")
async def delete_menu(menu_id: int):
    menu_crud = MenuOperations(engine)
    deleted_item = menu_crud.delete_menu_item(menu_id)
    return {"menu": deleted_item}


# Подменю

@app.get("/api/v1/menus/{menu_id}/submenus")
async def get_submenus(menu_id: int):
    submenus = submenu_crud.get_submenus(menu_id)
    return {"submenus": submenus}


@app.post("/api/v1/menus/{menu_id}/submenus")
async def add_submenu(menu_id, submenu):
    new_submenu = submenu_crud.add_submenu(menu_id, submenu)
    return {"submenu": new_submenu}
