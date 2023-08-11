from fastapi import HTTPException

from app.databases import RedisCache
from app.menu.crud import MenuRepository
from app.menu.schemas import MenuSchema, MenuSchemaResponse


class MenuService:
    def __init__(self, session,
                 redis_client: RedisCache = RedisCache()) -> None:
        self.database_repository = MenuRepository(session)
        self.redis_client = redis_client

    async def get_menus(self) -> list[MenuSchemaResponse]:
        cached = self.redis_client.get_cache('all')
        if cached is not None:
            return cached
        menus = await self.database_repository.get_all()
        menus_lst = []
        for item in menus:
            response = MenuSchemaResponse(**item.__dict__)
            response.id = str(response.id)
            menus_lst.append(response)
        self.redis_client.set_cache('all', menus_lst)
        return menus_lst

    async def get_menu(self, menu_id: int) -> MenuSchemaResponse:
        cached = self.redis_client.get_cache(f'{menu_id}')
        if cached is not None:
            return cached
        menu = await self.database_repository.get_one(menu_id)
        if menu:
            menu_dict = menu.__dict__
            menu_dict['id'] = str(menu_dict['id'])
            response = MenuSchemaResponse(**menu_dict)
            self.redis_client.set_cache(f'{menu_id}', response)
            return response
        else:
            raise HTTPException(status_code=404, detail='menu not found')

    async def add_menu(self, menu: MenuSchema):
        new_menu = await self.database_repository.post(menu)
        menu_dict = new_menu.__dict__
        menu_dict['id'] = str(menu_dict['id'])
        response = MenuSchemaResponse(**menu_dict)
        self.redis_client.set_cache(new_menu.id, response)
        self.redis_client.clear_cache('all*')
        return response

    async def edit_menu(self, menu_id: int, menu: MenuSchema) -> MenuSchemaResponse:
        to_edit = await self.database_repository.patch(menu_id, menu)
        menu_dict = to_edit.__dict__
        menu_dict['id'] = str(menu_dict['id'])
        response = MenuSchemaResponse(**menu_dict)
        self.redis_client.set_cache(f'{menu_id}', response)
        self.redis_client.clear_all_cache(menu_id)
        return response

    async def delete_menu(self, menu_id: int) -> dict:
        menu = await self.database_repository.delete(menu_id)
        self.redis_client.delete_cache(f'{menu_id}')
        self.redis_client.clear_all_cache(menu_id)
        return menu
