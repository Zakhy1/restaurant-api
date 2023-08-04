from app.menu.crud import MenuRepository
from app.menu.schemas import MenuSchema


class MenuService:
    def __init__(self, database_repository: MenuRepository = MenuRepository()):
        self.database_repository = database_repository

    def get_menus(self) -> list:
        menus = self.database_repository.get_all()
        return menus

    def get_menu(self, menu_id):
        menu = self.database_repository.get_one(menu_id)
        return menu

    def add_menu(self, menu: MenuSchema):
        menu = self.database_repository.post(menu)
        return menu

    def edit_menu(self, menu_id, menu: MenuSchema):
        menu = self.database_repository.patch(menu_id, menu)
        return menu

    def delete_menu(self, menu_id):
        menu = self.database_repository.delete(menu_id)
        return menu
