from fastapi import FastAPI

from database import engine
from menu.crud import MenuOperations
from menu.schema import Menu as MenuSchema
from submenu.crud import SubMenuOperations
from submenu.schema import SubMenu as SubMenuSchema

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
    result = menu_crud.add_menu(menu)
    return {"menu": result}


@app.patch("/api/v1/menus/{menu_id}")
async def edit_menu(menu_id: int, new_data: MenuSchema):
    menu_crud = MenuOperations(engine)
    result = menu_crud.edit_menu(menu_id, new_data)
    return {"menu": result}


@app.delete("/api/v1/menus/{menu_id}")
async def delete_menu(menu_id: int):
    menu_crud = MenuOperations(engine)
    deleted_item = menu_crud.delete_menu_item(menu_id)
    return {"menu": deleted_item}


# Подменю
@app.get("/api/v1/menus/{menu_id}/submenus")
async def get_submenus(menu_id: int):
    submenu_crud = SubMenuOperations(engine)
    submenus = submenu_crud.get_submenus(menu_id)
    submenus_list = {"submenus": []}
    for i in submenus:
        submenus_list["submenus"] += i
    return submenus_list


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def get_submenu(menu_id, submenu_id):
    submenu_crud = SubMenuOperations(engine)
    submenu = submenu_crud.get_submenu(menu_id, submenu_id)
    return {"submenu": submenu}


@app.post("/api/v1/menus/{menu_id}/submenus")
async def add_submenu(menu_id, submenu: SubMenuSchema):
    submenu_crud = SubMenuOperations(engine)
    new_submenu = submenu_crud.add_submenu(menu_id, submenu)
    return {"submenu": new_submenu}


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def edit_submenu(menu_id, submenu_id, submenu: SubMenuSchema):
    submenu_crud = SubMenuOperations(engine)
    edited_submenu = submenu_crud.edit_submenu(menu_id, submenu_id, submenu)
    return edited_submenu


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(menu_id: int, submenu_id: int):
    submenu_crud = SubMenuOperations(engine)
    deleted_item = submenu_crud.delete_submenu_item(menu_id, submenu_id)
    return {"submenu": deleted_item}


# Блюда
@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
async def get_dishes(menu_id: int, submenu_id: int):
    pass


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def get_dish(menu_id: int, submenu_id: int, dish_id: int):
    pass


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
async def add_dish(menu_id: int, submenu_id: int):
    pass


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def edit_dish(menu_id: int, submenu_id: int, dish_id: int):
    pass


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int):
    pass
