from fastapi import HTTPException

from app.databases import RedisCache
from app.dishes.crud import DishRepository
from app.dishes.schemas import DishSchema, DishSchemaResponse


class DishService:
    def __init__(self, session,
                 redis_client: RedisCache = RedisCache()) -> None:
        self.database_repository = DishRepository(session)
        self.redis_client = redis_client

    async def get_dishes(self, menu_id: int, submenu_id: int) -> list[DishSchemaResponse]:
        cached = self.redis_client.get_cache(f'all:{menu_id}:{submenu_id}')
        if cached is not None:
            return cached
        dishes = await self.database_repository.get_all(menu_id, submenu_id)
        dishes_list = []
        for dish in dishes:
            dish_dict = dish.__dict__
            dish_dict['id'] = str(dish_dict['id'])
            dish_dict['price'] = str(round(dish_dict['price'], 2))
            dishes_list.append(DishSchemaResponse(**dish_dict))
        self.redis_client.set_cache(f'all:{menu_id}:{submenu_id}', dishes_list)
        return dishes_list

    async def get_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> DishSchemaResponse:
        cached = self.redis_client.get_cache(f'{menu_id}:{submenu_id}:{dish_id}')
        if cached is not None:
            return cached
        dish = await self.database_repository.get_one(menu_id, submenu_id, dish_id)
        if dish:
            dish_dict = dish.__dict__
            dish_dict['id'] = str(dish_dict['id'])
            dish_dict['price'] = str(round(dish_dict['price'], 2))
            response = DishSchemaResponse(**dish_dict)
            self.redis_client.set_cache(f'{menu_id}:{submenu_id}:{dish_id}', response)
            return response
        else:
            raise HTTPException(status_code=404, detail='dish not found')

    async def add_dish(self, menu_id: int, submenu_id: int, dish: DishSchema) -> DishSchemaResponse:
        new_dish = await self.database_repository.post(menu_id, submenu_id, dish)
        to_return = new_dish.__dict__
        to_return['id'] = str(to_return['id'])
        to_return['price'] = str(round(to_return['price'], 2))
        response = DishSchemaResponse(**to_return)
        self.redis_client.set_cache(f'{menu_id}:{submenu_id}:{response.id}', response)
        self.redis_client.clear_all_cache(menu_id)
        return response

    async def edit_dish(self, menu_id: int, submenu_id: int, dish_id: int, dish: DishSchema) -> DishSchemaResponse:
        to_edit = await self.database_repository.patch(menu_id, submenu_id, dish_id, dish)
        to_return = to_edit.__dict__
        to_return['id'] = str(to_return['id'])
        to_return['price'] = str(round(to_return['price'], 2))
        response = DishSchemaResponse(**to_return)
        self.redis_client.set_cache(f'{menu_id}:{submenu_id}:{dish_id}', response)
        self.redis_client.clear_all_cache(menu_id)
        return response

    async def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> dict:
        dish = await self.database_repository.delete(menu_id, submenu_id, dish_id)
        self.redis_client.delete_cache(f'{menu_id}:{submenu_id}:{dish_id}')
        self.redis_client.clear_all_cache(menu_id)
        return dish
