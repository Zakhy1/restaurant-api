from fastapi import HTTPException

from app.dishes.crud import DishRepository
from app.dishes.schemas import DishSchema, DishSchemaResponse


class DishService:
    def __init__(self, database_repository: DishRepository = DishRepository()):
        self.database_repository = database_repository

    def get_dishes(self, menu_id, submenu_id) -> list:
        dishes = self.database_repository.get_all(menu_id, submenu_id)
        dishes_list = []
        for dish in dishes:
            dish_response = DishSchemaResponse(**dish.__dict__)
            dish_response.id = str(dish_response.id)
            dish_response.price = str(round(dish_response.price, 2))
            dishes_list.append(dish_response)
        return dishes_list

    def get_dish(self, menu_id, submenu_id, dish_id):
        dish = self.database_repository.get_one(menu_id, submenu_id, dish_id)
        if dish:
            dish_dict = dish.__dict__
            dish_dict["id"] = str(dish_dict["id"])
            dish_dict["price"] = str(round(dish_dict["price"], 2))
            return DishSchemaResponse(**dish_dict)
        else:
            raise HTTPException(status_code=404, detail="dish not found")

    def add_dish(self, menu_id, submenu_id, dish: DishSchema):
        new_dish = self.database_repository.post(menu_id, submenu_id, dish)
        to_return = new_dish.__dict__
        to_return["id"] = str(to_return["id"])
        to_return["price"] = str(round(to_return["price"], 2))
        return DishSchemaResponse(**to_return)

    def edit_dish(self, menu_id, submenu_id, dish_id, dish: DishSchema):
        to_edit = self.database_repository.patch(menu_id, submenu_id, dish_id, dish)
        to_return = to_edit.__dict__
        to_return["id"] = str(to_return["id"])
        to_return["price"] = str(round(to_return["price"], 2))
        return DishSchemaResponse(**to_return)

    def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        dish = self.database_repository.delete(menu_id, submenu_id, dish_id)
        return dish
