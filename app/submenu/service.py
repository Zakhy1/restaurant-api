from app.submenu.crud import SubMenuRepository
from app.submenu.schemas import SubMenuSchema


class SubMenuService:
    def __init__(self, database_repository: SubMenuRepository = SubMenuRepository()):
        self.database_repository = database_repository

    def get_submenus(self, menu_id) -> list:
        submenus = self.database_repository.get_all(menu_id)
        return submenus

    def get_submenu(self, menu_id, submenu_id):
        submenu = self.database_repository.get_one(menu_id, submenu_id)
        return submenu

    def add_submenu(self, menu_id, submenu: SubMenuSchema):
        submenu = self.database_repository.post(menu_id, submenu)
        return submenu

    def edit_submenu(self, menu_id, submenu_id, submenu: SubMenuSchema):
        submenu = self.database_repository.patch(menu_id, submenu_id, submenu)
        return submenu

    def delete_submenu(self, menu_id: int, submenu_id: int):
        submenu = self.database_repository.delete(menu_id, submenu_id)
        return submenu
