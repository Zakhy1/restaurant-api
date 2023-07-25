from fastapi import FastAPI
from fastapi import HTTPException

from database import engine

from dishes.crud import DishOperations
from dishes.schema import Dishes as DishSchema
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
    return menus


@app.get("/api/v1/menus/{menu_id}")
async def get_menu(menu_id):  # TODO COUNT SUBMENUS
    menu_crud = MenuOperations(engine)
    menu = menu_crud.get_menu(menu_id)
    if menu:
        return menu
    raise HTTPException(status_code=404, detail="menu not found")


@app.post("/api/v1/menus", status_code=201)
async def add_menu(new_menu: MenuSchema):
    menu_crud = MenuOperations(engine)
    new_menu = menu_crud.add_menu(new_menu)
    return new_menu


@app.patch("/api/v1/menus/{menu_id}")
async def edit_menu(menu_id: int, new_data: MenuSchema):
    menu_crud = MenuOperations(engine)
    edited_menu = menu_crud.edit_menu(menu_id, new_data)
    return edited_menu


@app.delete("/api/v1/menus/{menu_id}")
async def delete_menu(menu_id: int):
    menu_crud = MenuOperations(engine)
    deleted_item = menu_crud.delete_menu_item(menu_id)
    return deleted_item


# Подменю
@app.get("/api/v1/menus/{menu_id}/submenus")
async def get_submenus(menu_id: int):
    submenu_crud = SubMenuOperations(engine)
    submenus = submenu_crud.get_submenus(menu_id)
    submenus_list = []
    for i in submenus:
        submenus_list += i
    return submenus_list


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def get_submenu(menu_id, submenu_id):  # TODO COUNT DISHES
    submenu_crud = SubMenuOperations(engine)
    submenu = submenu_crud.get_submenu(menu_id, submenu_id)
    if submenu:
        return submenu
    raise HTTPException(status_code=404, detail="submenu not found")


@app.post("/api/v1/menus/{menu_id}/submenus", status_code=201)
async def add_submenu(menu_id, submenu: SubMenuSchema):
    submenu_crud = SubMenuOperations(engine)
    new_submenu = submenu_crud.add_submenu(menu_id, submenu)
    return new_submenu


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def edit_submenu(menu_id, submenu_id, submenu: SubMenuSchema):
    submenu_crud = SubMenuOperations(engine)
    edited_submenu = submenu_crud.edit_submenu(menu_id, submenu_id, submenu)
    return edited_submenu


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(menu_id: int, submenu_id: int):
    submenu_crud = SubMenuOperations(engine)
    deleted_item = submenu_crud.delete_submenu(menu_id, submenu_id)
    return deleted_item


# Блюда
@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
async def get_dishes(menu_id: int, submenu_id: int):
    dish_crud = DishOperations(engine)
    dishes = dish_crud.get_dishes(menu_id, submenu_id)
    dishes_list = []
    for i in dishes:
        dishes_list += i
    return dishes_list


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def get_dish(menu_id: int, submenu_id: int, dish_id: int):
    dish_crud = DishOperations(engine)
    dish = dish_crud.get_dish(menu_id, submenu_id, dish_id)
    if dish:
        return dish
    raise HTTPException(status_code=404, detail="dish not found")


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=201)
async def add_dish(menu_id: int, submenu_id: int, dish: DishSchema):
    dish_crud = DishOperations(engine)
    dish = dish_crud.add_dish(menu_id, submenu_id, dish)
    return dish


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def edit_dish(menu_id: int, submenu_id: int, dish_id: int, dish: DishSchema):
    dish_crud = DishOperations(engine)
    to_edit = dish_crud.edit_dish(menu_id, submenu_id, dish_id, dish)
    return to_edit


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int):
    dish_crud = DishOperations(engine)
    to_delete = dish_crud.delete_dish(menu_id, submenu_id, dish_id)
    return to_delete
