from fastapi import HTTPException

from app.submenu.crud import SubMenuRepository
from app.submenu.schemas import SubMenuSchema, SubMenuSchemaResponse


class SubMenuService:
    def __init__(self, database_repository: SubMenuRepository = SubMenuRepository()):
        self.database_repository = database_repository

    def get_submenus(self, menu_id) -> list:
        submenus = self.database_repository.get_all(menu_id)
        submenus_lst = []
        for submenu in submenus:
            submenu_response = SubMenuSchemaResponse(**submenu.__dict__)
            submenu_response.id = str(submenu_response.id)
            submenus_lst.append(submenu_response)
        return submenus_lst

    def get_submenu(self, menu_id, submenu_id):
        submenu = self.database_repository.get_one(menu_id, submenu_id)
        if submenu:
            submenu_dict = submenu.__dict__
            submenu_dict["id"] = str(submenu_dict["id"])
            return SubMenuSchemaResponse(**submenu_dict)
        else:
            raise HTTPException(status_code=404, detail="submenu not found")

    def add_submenu(self, menu_id, submenu: SubMenuSchema):
        new_submenu = self.database_repository.post(menu_id, submenu)
        to_return = new_submenu.__dict__
        to_return["id"] = str(to_return["id"])
        return SubMenuSchemaResponse(**to_return)

    def edit_submenu(self, menu_id, submenu_id, submenu: SubMenuSchema):
        to_edit = self.database_repository.patch(menu_id, submenu_id, submenu)
        to_return = to_edit.__dict__
        to_return["id"] = str(to_return["id"])
        return SubMenuSchemaResponse(**to_return)

    def delete_submenu(self, menu_id: int, submenu_id: int):
        submenu = self.database_repository.delete(menu_id, submenu_id)
        return submenu
