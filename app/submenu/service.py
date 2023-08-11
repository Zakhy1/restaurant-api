from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases import RedisCache
from app.submenu.crud import SubMenuRepository
from app.submenu.schemas import SubMenuSchema, SubMenuSchemaResponse


class SubMenuService:
    def __init__(self, session: AsyncSession,
                 redis_client: RedisCache = RedisCache()):
        self.database_repository = SubMenuRepository(session)
        self.redis_client = redis_client

    async def get_submenus(self, menu_id: int) -> list[SubMenuSchemaResponse]:
        cached = self.redis_client.get_cache(f'all:{menu_id}')
        if cached is not None:
            return cached
        submenus = await self.database_repository.get_all(menu_id)
        submenus_lst = []
        for submenu in submenus:
            submenu_response = SubMenuSchemaResponse(**submenu.__dict__)
            submenu_response.id = str(submenu_response.id)
            submenus_lst.append(submenu_response)
        self.redis_client.set_cache(f'all:{menu_id}', submenus_lst)
        return submenus_lst

    async def get_submenu(self, menu_id: int, submenu_id: int) -> SubMenuSchemaResponse:
        cached = self.redis_client.get_cache(f'{menu_id}:{submenu_id}')
        if cached is not None:
            return cached
        submenu = await self.database_repository.get_one(menu_id, submenu_id)
        if submenu:
            submenu_dict = submenu.__dict__
            submenu_dict['id'] = str(submenu_dict['id'])
            response = SubMenuSchemaResponse(**submenu_dict)
            self.redis_client.set_cache(f'{menu_id}:{submenu_id}', response)
            return response
        else:
            raise HTTPException(status_code=404, detail='submenu not found')

    async def add_submenu(self, menu_id: int, submenu: SubMenuSchema) -> SubMenuSchemaResponse:
        new_submenu = await self.database_repository.post(menu_id, submenu)
        to_return = new_submenu.__dict__
        to_return['id'] = str(to_return['id'])
        response = SubMenuSchemaResponse(**to_return)
        self.redis_client.set_cache(f'{menu_id}:{response.id})', response)
        self.redis_client.clear_all_cache(menu_id)
        return response

    async def edit_submenu(self, menu_id: int, submenu_id: int, submenu: SubMenuSchema) -> SubMenuSchemaResponse:
        to_edit = await self.database_repository.patch(menu_id, submenu_id, submenu)
        to_return = to_edit.__dict__
        to_return['id'] = str(to_return['id'])
        response = SubMenuSchemaResponse(**to_return)
        self.redis_client.set_cache(f'{menu_id}:{submenu_id}', response)
        self.redis_client.clear_all_cache(menu_id)
        return response

    async def delete_submenu(self, menu_id: int, submenu_id: int) -> dict:
        submenu = await self.database_repository.delete(menu_id, submenu_id)
        self.redis_client.delete_cache(f'{menu_id}:{submenu_id}')
        self.redis_client.clear_all_cache(menu_id)
        return submenu
