from fastapi import HTTPException
from sqlalchemy import and_, delete
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import db_session
from app.dishes.schemas import DishSchemaResponse, DishSchema
from app.models import Dish
from app.models import SubMenu


class DishRepository:
    def __init__(self, session: Session = db_session):
        self.session: Session = session

    def get_all(self, menu_id: int, submenu_id: int):
        query = select(Dish).join(SubMenu).where(and_(Dish.submenu_id == submenu_id, SubMenu.menu_id == menu_id))
        query_result = self.session.execute(query)
        dishes = query_result.scalars().all()
        dishes_list = []
        for dish in dishes:
            dish_response = DishSchemaResponse(**dish.__dict__)
            dish_response.id = str(dish_response.id)
            dish_response.price = str(round(dish_response.price, 2))
            dishes_list.append(dish_response)
        return dishes_list

    def get_one(self, menu_id: int, submenu_id: int, dish_id: int):
        query = select(Dish).join(SubMenu).where(and_(SubMenu.menu_id == menu_id,
                                                      Dish.submenu_id == submenu_id, Dish.id == dish_id))
        query_result = self.session.execute(query)
        dish = query_result.scalar_one_or_none()
        if dish:
            dish_dict = dish.__dict__
            dish_dict["id"] = str(dish_dict["id"])
            dish_dict["price"] = str(round(dish_dict["price"], 2))
            return DishSchemaResponse(**dish_dict)
        else:
            raise HTTPException(status_code=404, detail="dish not found")

    def post(self, menu_id, submenu_id, dish: DishSchema):
        new_dish = Dish(submenu_id=submenu_id, **dish.model_dump())
        self.session.add(new_dish)
        self.session.commit()
        self.session.refresh(new_dish)
        to_return = new_dish.__dict__
        to_return["id"] = str(to_return["id"])
        to_return["price"] = str(round(to_return["price"], 2))
        return DishSchemaResponse(**to_return)

    def patch(self, menu_id: int, submenu_id: int, dish_id: int, dish: DishSchema):
        query = select(Dish).join(SubMenu).where(and_(SubMenu.menu_id == menu_id,
                                                      Dish.submenu_id == submenu_id, Dish.id == dish_id))
        result = self.session.execute(query)
        to_edit = result.scalar_one_or_none()
        if to_edit:
            to_edit.title = dish.title
            to_edit.description = dish.description
            to_edit.price = dish.price
            self.session.commit()
            self.session.refresh(to_edit)
            to_return = to_edit.__dict__
            to_return["id"] = str(to_return["id"])
            to_return["price"] = str(round(to_return["price"], 2))
            return DishSchemaResponse(**to_return)
        else:
            raise HTTPException(status_code=404, detail="dish not found")

    def delete(self, menu_id: int, submenu_id: int, dish_id: int, ):
        query = delete(Dish).where(Dish.id == dish_id)
        self.session.execute(query)
        self.session.commit()
        return {"status": True, "message": "The dish has been deleted"}