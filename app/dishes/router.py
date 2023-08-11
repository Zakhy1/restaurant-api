from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases import get_session
from app.dishes.schemas import DishSchema, DishSchemaResponse
from app.dishes.service import DishService

dish_router = APIRouter()


@dish_router.get('/dishes')
async def get_dishes(menu_id: int, submenu_id: int, session: AsyncSession = Depends(get_session)) -> list[
        DishSchemaResponse]:
    service = DishService(session)
    return await service.get_dishes(menu_id, submenu_id)


@dish_router.get('/dishes/{dish_id}')
async def get_dish(menu_id: int, submenu_id: int, dish_id: int,
                   session: AsyncSession = Depends(get_session)) -> DishSchemaResponse:
    service = DishService(session)
    return await service.get_dish(menu_id, submenu_id, dish_id)


@dish_router.post('/dishes', status_code=201)
async def add_dish(menu_id: int, submenu_id: int, dish: DishSchema,
                   session: AsyncSession = Depends(get_session)) -> DishSchemaResponse:
    service = DishService(session)
    return await service.add_dish(menu_id, submenu_id, dish)


@dish_router.patch('/dishes/{dish_id}')
async def edit_dish(menu_id: int, submenu_id: int, dish_id: int, dish: DishSchema,
                    session: AsyncSession = Depends(get_session)) -> DishSchemaResponse:
    service = DishService(session)
    return await service.edit_dish(menu_id, submenu_id, dish_id, dish)


@dish_router.delete('/dishes/{dish_id}')
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int,
                      session: AsyncSession = Depends(get_session)) -> dict:
    service = DishService(session)
    return await service.delete_dish(menu_id, submenu_id, dish_id)
