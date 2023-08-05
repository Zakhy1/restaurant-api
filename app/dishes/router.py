from fastapi import APIRouter

from app.dishes.schemas import DishSchema, DishSchemaResponse
from app.dishes.service import DishService

dish_router = APIRouter()


@dish_router.get("/dishes")
def get_dishes(menu_id: int, submenu_id: int) -> list[DishSchemaResponse]:
    service = DishService()
    return service.get_dishes(menu_id, submenu_id)


@dish_router.get("/dishes/{dish_id}")
def get_dish(menu_id: int, submenu_id: int, dish_id: int) -> DishSchemaResponse:
    service = DishService()
    return service.get_dish(menu_id, submenu_id, dish_id)


@dish_router.post("/dishes", status_code=201)
def add_dish(menu_id: int, submenu_id: int, dish: DishSchema) -> DishSchemaResponse:
    service = DishService()
    return service.add_dish(menu_id, submenu_id, dish)


@dish_router.patch("/dishes/{dish_id}")
def edit_dish(menu_id: int, submenu_id: int, dish_id: int, dish: DishSchema) -> DishSchemaResponse:
    service = DishService()
    return service.edit_dish(menu_id, submenu_id, dish_id, dish)


@dish_router.delete("/dishes/{dish_id}")
def delete_dish(menu_id: int, submenu_id: int, dish_id: int) -> dict:
    service = DishService()
    return service.delete_dish(menu_id, submenu_id, dish_id)
