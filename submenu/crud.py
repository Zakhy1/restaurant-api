from sqlalchemy import select
from sqlalchemy.orm import Session

from models import SubMenu
from submenu.schema import SubMenu as SubMenuSchema


class SubMenuOperations:
    def __init__(self, engine):
        self.engine = engine

    def get_submenus(self, menu_id: int):
        with Session(self.engine) as session:
            query = select(SubMenu).where(SubMenu.menu_id == menu_id)
            submenus = session.execute(query)
            return submenus.fetchall()

    def get_submenu(self, menu_id: int, submenu_id: int):  # TODO
        with Session(self.engine) as session:
            query = select(SubMenu).where(SubMenu.id == submenu_id)\
                                   .where(SubMenu.menu_id == menu_id)
            res = session.execute(query)
            return res.scalar_one_or_none()

    def add_submenu(self, menu_id: int, submenu: SubMenuSchema):
        with Session(self.engine) as session:
            query = select(SubMenu).where(SubMenu.title == submenu.title)
            result = session.execute(query)
            if result.scalar_one_or_none():
                return {"error": f"submenu with name '{submenu.title}' already exist"}
            new_submenu = SubMenu(
                title=submenu.title, description=submenu.description, menu_id=menu_id)
            session.add(new_submenu)
            query = select(SubMenu).where(SubMenu.title == submenu.title)  # todo refactor with 2 queries
            result = session.execute(query)
            session.commit()
            return result.scalar_one_or_none()

    def edit_submenu(self, menu_id, submenu_id, submenu: SubMenuSchema):
        with Session(self.engine) as session:
            to_edit = session.get(SubMenu, submenu_id)
            if to_edit:
                to_edit.title = submenu.title
                to_edit.description = submenu.description
                session.commit()
                return {"id": to_edit.id, "title": to_edit.title, "description": to_edit.description}
            else:
                return {"error": f"menu with id {menu_id} not found"}

    def delete_submenu_item(self, menu_id: int, submenu_id: int):
        with Session(self.engine) as session:
            to_delete = session.get(SubMenu, submenu_id)
            session.delete(to_delete)
            session.commit()
            return to_delete
