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
        return dishes

    def get_one(self, menu_id: int, submenu_id: int, dish_id: int):
        query = select(Dish).join(SubMenu).where(and_(SubMenu.menu_id == menu_id,
                                                      Dish.submenu_id == submenu_id, Dish.id == dish_id))
        query_result = self.session.execute(query)
        dish = query_result.scalar_one_or_none()
        return dish

    def post(self, menu_id, submenu_id, dish: DishSchema):
        new_dish = Dish(submenu_id=submenu_id, **dish.model_dump())
        self.session.add(new_dish)
        self.session.commit()
        self.session.refresh(new_dish)
        return new_dish

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
            return to_edit
        else:
            raise HTTPException(status_code=404, detail="dish not found")

    def delete(self, menu_id: int, submenu_id: int, dish_id: int, ):
        query = delete(Dish).where(Dish.id == dish_id)
        self.session.execute(query)
        self.session.commit()
        return {"status": True, "message": "The dish has been deleted"}