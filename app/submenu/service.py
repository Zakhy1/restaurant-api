from fastapi import HTTPException

from app.databases import RedisCache
from app.submenu.crud import SubMenuRepository
from app.submenu.schemas import SubMenuSchema, SubMenuSchemaResponse


class SubMenuService:
    def __init__(self, database_repository: SubMenuRepository = SubMenuRepository(),
                 redis_client: RedisCache = RedisCache()):
        self.database_repository = database_repository
        self.redis_client = redis_client

    def get_submenus(self, menu_id) -> list:
        cached = self.redis_client.get(f'all:{menu_id}')
        if cached is not None:
            return cached
        submenus = self.database_repository.get_all(menu_id)
        submenus_lst = []
        for submenu in submenus:
            submenu_response = SubMenuSchemaResponse(**submenu.__dict__)
            submenu_response.id = str(submenu_response.id)
            submenus_lst.append(submenu_response)
        self.redis_client.set(f'all:{menu_id}', submenus_lst)
        return submenus_lst

    def get_submenu(self, menu_id, submenu_id):
        cached = self.redis_client.get(f'{menu_id}:{submenu_id}')
        if cached is not None:
            return cached
        submenu = self.database_repository.get_one(menu_id, submenu_id)
        if submenu:
            submenu_dict = submenu.__dict__
            submenu_dict["id"] = str(submenu_dict["id"])
            response = SubMenuSchemaResponse(**submenu_dict)
            self.redis_client.set(f'{menu_id}:{submenu_id}', response)
            return response
        else:
            raise HTTPException(status_code=404, detail="submenu not found")

    def add_submenu(self, menu_id, submenu: SubMenuSchema):
        new_submenu = self.database_repository.post(menu_id, submenu)
        to_return = new_submenu.__dict__
        to_return["id"] = str(to_return["id"])
        response = SubMenuSchemaResponse(**to_return)
        self.redis_client.set(f'{menu_id}:{response.id})', response)
        self.redis_client.clear_after_change(menu_id)
        return response

    def edit_submenu(self, menu_id, submenu_id, submenu: SubMenuSchema):
        to_edit = self.database_repository.patch(menu_id, submenu_id, submenu)
        to_return = to_edit.__dict__
        to_return["id"] = str(to_return["id"])
        response = SubMenuSchemaResponse(**to_return)
        self.redis_client.set(f'{menu_id}:{submenu_id}', response)
        self.redis_client.clear_after_change(menu_id)
        return response

    def delete_submenu(self, menu_id: int, submenu_id: int):
        submenu = self.database_repository.delete(menu_id, submenu_id)
        self.redis_client.delete(f'{menu_id}:{submenu_id}')
        self.redis_client.clear_after_change(menu_id)
        return submenu
