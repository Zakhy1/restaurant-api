from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Dish, Menu, CrudOperations
from app.models import SubMenu


class DishOperations(CrudOperations):
    def get_dishes(self, menu_id: int, submenu_id: int):
        with Session(self.engine) as session:
            query = select(Dish).join(SubMenu).where(and_(SubMenu.menu_id == menu_id, Dish.submenu_id == submenu_id))
            dishes = session.execute(query)
            return dishes.fetchall()

    def get_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        with Session(self.engine) as session:
            query = select(Dish).join(SubMenu).where(and_(SubMenu.menu_id == menu_id,
                                                          Dish.submenu_id == submenu_id, Dish.id == dish_id))
            dish = session.execute(query)
            result = dish.scalar_one_or_none()
            if result:
                return {"id": str(result.id), "title": result.title,
                        "description": result.description, "price": str(result.price)}
            else:
                return None

    def add_dish(self, menu_id, submenu_id, dish):
        with Session(self.engine) as session:
            query = select(Menu).where(Menu.id == menu_id)
            menu = session.execute(query)
            if not menu:
                return "menu does not exist"
            query = select(SubMenu).where(SubMenu.id == submenu_id)
            submenu = session.execute(query)
            if not submenu:
                return "submenu does not exist"

            query = select(Dish).where(Dish.title == dish.title)
            unique_dish = session.execute(query)
            if unique_dish.scalar_one_or_none():
                return f"dish with name {dish.title} exist in submenu {submenu_id} in menu {menu_id}"

            new_dish = Dish(title=dish.title, description=dish.description, price=dish.price, submenu_id=submenu_id)
            session.add(new_dish)

            query = select(Dish).where(Dish.title == dish.title)
            dish_to_return = session.execute(query)
            result = dish_to_return.scalar_one_or_none()
            session.commit()
            if result:
                return {"id": str(result.id), "title": result.title,
                        "description": result.description, "price": str(result.price)}
            else:
                return None

    def edit_dish(self, menu_id: int, submenu_id: int, dish_id: int, dish):
        with Session(self.engine) as session:
            to_edit = session.get(Dish, dish_id)
            if to_edit:
                to_edit.title = dish.title
                to_edit.description = dish.description
                to_edit.price = dish.price
                session.commit()
                return {"id": str(to_edit.id), "title": to_edit.title,
                        "description": to_edit.description, "price": str(to_edit.price)}
            else:
                return {"error": f"dish with id {dish_id} not found "
                                 f"id submenu with id {submenu_id} in menu with id {menu_id}"}

    def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int, ):
        with Session(self.engine) as session:
            to_delete = session.get(Dish, dish_id)
            if to_delete:
                session.delete(to_delete)
                session.commit()
                return {"status": True,
                        "message": "The menu has been deleted"}
            else:
                return f"there is no dish with id {dish_id}"

    def delete_all_dishes(self, submenu_id: int):
        with Session(self.engine) as session:
            to_delete = session.scalars(select(Dish).where(Dish.submenu_id == submenu_id)).fetchall()
            for i in to_delete:
                session.delete(i)
            session.commit()
            return to_delete
