from fastapi import HTTPException

from app.menu.crud import MenuRepository
from app.menu.schemas import MenuSchema, MenuSchemaResponse


class MenuService:
    def __init__(self, database_repository: MenuRepository = MenuRepository()):
        self.database_repository = database_repository

    def get_menus(self) -> list:
        menus = self.database_repository.get_all()
        menus_lst = []
        for item in menus:
            response = MenuSchemaResponse(**item.__dict__)
            response.id = str(response.id)
            menus_lst.append(response)
        return menus

    def get_menu(self, menu_id):
        menu = self.database_repository.get_one(menu_id)
        if menu:
            menu_dict = menu.__dict__
            menu_dict["id"] = str(menu_dict["id"])
            return MenuSchemaResponse(**menu_dict)
        else:
            raise HTTPException(status_code=404, detail="menu not found")

    def add_menu(self, menu: MenuSchema):
        new_menu = self.database_repository.post(menu)
        menu_dict = new_menu.__dict__
        menu_dict["id"] = str(menu_dict["id"])
        return MenuSchemaResponse(**menu_dict)

    def edit_menu(self, menu_id, menu: MenuSchema):
        to_edit = self.database_repository.patch(menu_id, menu)
        menu_dict = to_edit.__dict__
        menu_dict["id"] = str(menu_dict["id"])
        return MenuSchemaResponse(**menu_dict)

    def delete_menu(self, menu_id):
        menu = self.database_repository.delete(menu_id)
        return menu
