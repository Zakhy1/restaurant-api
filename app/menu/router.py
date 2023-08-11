from fastapi import APIRouter

from app.menu.schemas import MenuSchema, MenuSchemaResponse
from app.menu.service import MenuService

menu_router = APIRouter()


@menu_router.get('/menus')
async def get_menus() -> list[MenuSchemaResponse]:
    service = MenuService()
    return await service.get_menus()


@menu_router.get('/menus/{menu_id}')
async def get_menu(menu_id: int) -> MenuSchemaResponse:
    service = MenuService()
    return await service.get_menu(menu_id)


@menu_router.post('/menus', status_code=201)
async def add_menu(new_menu: MenuSchema) -> MenuSchemaResponse:
    service = MenuService()
    return await service.add_menu(new_menu)


@menu_router.patch('/menus/{menu_id}')
async def edit_menu(menu_id: int, new_data: MenuSchema) -> MenuSchemaResponse:
    service = MenuService()
    return await service.edit_menu(menu_id, new_data)


@menu_router.delete('/menus/{menu_id}')
async def delete_menu(menu_id: int) -> dict:
    service = MenuService()
    return await service.delete_menu(menu_id)
