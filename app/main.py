from fastapi import FastAPI
from fastapi import HTTPException

from app.database import engine

# from app.dishes.crud import DishOperations
from app.dishes.schemas import DishSchema
from app.dishes.service import DishService
from app.menu.crud import MenuRepository
from app.menu.schemas import MenuSchema
from app.menu.service import MenuService
# from app.submenu.crud import SubMenuOperations
from app.submenu.schemas import SubMenuSchema
from app.submenu.service import SubMenuService

app = FastAPI()


# Меню
@app.get("/api/v1/menus")
def get_menus():
    service = MenuService()
    return service.get_menus()


@app.get("/api/v1/menus/{menu_id}")
def get_menu(menu_id):
    service = MenuService()
    return service.get_menu(menu_id)


@app.post("/api/v1/menus", status_code=201)
def add_menu(new_menu: MenuSchema):
    service = MenuService()
    return service.add_menu(new_menu)


@app.patch("/api/v1/menus/{menu_id}")
def edit_menu(menu_id: int, new_data: MenuSchema):
    service = MenuService()
    return service.edit_menu(menu_id, new_data)


@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: int):
    service = MenuService()
    return service.delete_menu(menu_id)


# Подменю
@app.get("/api/v1/menus/{menu_id}/submenus")
def get_submenus(menu_id: int):
    service = SubMenuService()
    return service.get_submenus(menu_id)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def get_submenu(menu_id, submenu_id):
    service = SubMenuService()
    return service.get_submenu(menu_id, submenu_id)


@app.post("/api/v1/menus/{menu_id}/submenus", status_code=201)
def add_submenu(menu_id, submenu: SubMenuSchema):
    service = SubMenuService()
    return service.add_submenu(menu_id, submenu)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def edit_submenu(menu_id, submenu_id, submenu: SubMenuSchema):
    service = SubMenuService()
    return service.edit_submenu(menu_id, submenu_id, submenu)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: int, submenu_id: int):
    service = SubMenuService()
    return service.delete_submenu(menu_id, submenu_id)


# Блюда
@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
def get_dishes(menu_id: int, submenu_id: int):
    service = DishService()
    return service.get_dishes(menu_id, submenu_id)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def get_dish(menu_id: int, submenu_id: int, dish_id: int):
    service = DishService()
    return service.get_dish(menu_id, submenu_id, dish_id)


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=201)
def add_dish(menu_id: int, submenu_id: int, dish: DishSchema):
    service = DishService()
    return service.add_dish(menu_id, submenu_id, dish)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def edit_dish(menu_id: int, submenu_id: int, dish_id: int, dish: DishSchema):
    service = DishService()
    return service.edit_dish(menu_id, submenu_id, dish_id, dish)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(menu_id: int, submenu_id: int, dish_id: int):
    service = DishService()
    return service.delete_dish(menu_id, submenu_id, dish_id)
