from fastapi import APIRouter

from app.submenu.schemas import SubMenuSchema, SubMenuSchemaResponse
from app.submenu.service import SubMenuService

submenu_router = APIRouter()


@submenu_router.get('/submenus')
async def get_submenus(menu_id: int) -> list[SubMenuSchemaResponse]:
    service = SubMenuService()
    return await service.get_submenus(menu_id)


@submenu_router.get('/submenus/{submenu_id}')
async def get_submenu(menu_id: int, submenu_id: int) -> SubMenuSchemaResponse:
    service = SubMenuService()
    return await service.get_submenu(menu_id, submenu_id)


@submenu_router.post('/submenus', status_code=201)
async def add_submenu(menu_id, submenu: SubMenuSchema) -> SubMenuSchemaResponse:
    service = SubMenuService()
    return await service.add_submenu(menu_id, submenu)


@submenu_router.patch('/submenus/{submenu_id}')
async def edit_submenu(menu_id, submenu_id, submenu: SubMenuSchema) -> SubMenuSchemaResponse:
    service = SubMenuService()
    return await service.edit_submenu(menu_id, submenu_id, submenu)


@submenu_router.delete('/submenus/{submenu_id}')
async def delete_submenu(menu_id: int, submenu_id: int) -> dict:
    service = SubMenuService()
    return await service.delete_submenu(menu_id, submenu_id)
