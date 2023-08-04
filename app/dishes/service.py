from app.dishes.crud import DishRepository
from app.dishes.schemas import DishSchema


class DishService:
    def __init__(self, database_repository: DishRepository = DishRepository()):
        self.database_repository = database_repository

    def get_dishes(self, menu_id, submenu_id) -> list:
        dishes = self.database_repository.get_all(menu_id, submenu_id)
        return dishes

    def get_dish(self, menu_id, submenu_id, dish_id):
        dish = self.database_repository.get_one(menu_id, submenu_id, dish_id)
        return dish

    def add_dish(self, menu_id, submenu_id, dish: DishSchema):
        dish = self.database_repository.post(menu_id, submenu_id, dish)
        return dish

    def edit_dish(self, menu_id, submenu_id, dish_id, dish: DishSchema):
        dish = self.database_repository.patch(menu_id, submenu_id, dish_id, dish)
        return dish

    def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        dish = self.database_repository.delete(menu_id, submenu_id, dish_id)
        return dish
