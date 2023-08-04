from fastapi import APIRouter

from app.menu.schemas import MenuSchema
from app.menu.service import MenuService

menu_router = APIRouter()


@menu_router.get("/menus")
def get_menus():
    service = MenuService()
    return service.get_menus()


@menu_router.get("/menus/{menu_id}")
def get_menu(menu_id):
    service = MenuService()
    return service.get_menu(menu_id)


@menu_router.post("/menus", status_code=201)
def add_menu(new_menu: MenuSchema):
    service = MenuService()
    return service.add_menu(new_menu)


@menu_router.patch("/menus/{menu_id}")
def edit_menu(menu_id: int, new_data: MenuSchema):
    service = MenuService()
    return service.edit_menu(menu_id, new_data)


@menu_router.delete("/menus/{menu_id}")
def delete_menu(menu_id: int):
    service = MenuService()
    return service.delete_menu(menu_id)
