import sys

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Dish
from models import SubMenu
from submenu.schema import SubMenu as SubMenuSchema

sys.setrecursionlimit(2000)


class SubMenuOperations:
    def __init__(self, engine):
        self.engine = engine

    def get_submenus(self, menu_id: int):
        with Session(self.engine) as session:
            query = select(SubMenu).where(SubMenu.menu_id == menu_id)
            submenus = session.execute(query)
            return submenus.fetchall()

    def get_submenu(self, menu_id: int, submenu_id: int):
        with Session(self.engine) as session:
            query = select(SubMenu).where(SubMenu.id == submenu_id) \
                .where(SubMenu.menu_id == menu_id)
            submenu = session.execute(query)
            result = submenu.scalar_one_or_none()

            query = select(func.count("*")).where(Dish.submenu_id == submenu_id).select_from(
                Dish)
            dish_count_result = session.execute(query)
            dish_count = dish_count_result.scalar()

            if result:
                return {"id": str(result.id), "title": result.title,
                        "description": result.description, "dishes_count": dish_count}
            else:
                return None

    def add_submenu(self, menu_id: int, submenu: SubMenuSchema):
        with Session(self.engine) as session:

            query = select(SubMenu).where(SubMenu.title == submenu.title)
            result = session.execute(query)
            if result.scalar_one_or_none():
                return {"error": f"submenu with name '{submenu.title}' already exist"}

            new_submenu = SubMenu(
                title=submenu.title, description=submenu.description, menu_id=menu_id)
            session.add(new_submenu)

            query = select(SubMenu).where(SubMenu.title == submenu.title)
            submenu = session.execute(query)
            result = submenu.scalar_one_or_none()
            session.commit()
            if result:
                return {"id": str(result.id), "title": result.title, "description": result.description}
            else:
                return None

    def edit_submenu(self, menu_id, submenu_id, submenu: SubMenuSchema):
        with Session(self.engine) as session:
            to_edit = session.get(SubMenu, submenu_id)
            if to_edit:
                to_edit.title = submenu.title
                to_edit.description = submenu.description
                session.commit()
                return {"id": str(to_edit.id), "title": to_edit.title, "description": to_edit.description}
            else:
                return {"error": f"submenu with id {submenu_id} not found id menu with id {menu_id}"}

    def delete_submenu(self, menu_id: int, submenu_id: int):
        with Session(self.engine) as session:
            result = session.query(SubMenu).filter_by(id=submenu_id).scalar()
            if result:
                session.delete(result)
                session.commit()
                return {"id": str(result.id), "title": result.title, "description": result.description}
            else:
                return None
