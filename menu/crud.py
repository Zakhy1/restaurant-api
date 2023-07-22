from sqlalchemy import select
from sqlalchemy.orm import Session

from menu.schema import Menu as MenuSchema
from models import Menu


class MenuOperations:
    def __init__(self, engine):
        self.engine = engine

    def get_menus(self):
        with Session(self.engine) as session:
            menus = session.query(Menu).all()
            return menus

    def get_menu(self, menu_id: int):
        with Session(self.engine) as session:
            menu = session.get(Menu, menu_id)
            return menu

    def add_menu(self, menu: MenuSchema):  # TODO TEST
        with Session(self.engine) as session:
            query = select(Menu).where(Menu.title == menu.title)
            result = session.execute(query).scalar_one_or_none()
            if result:
                return {"error": f"menu with name '{menu.title}' already exist"}
            new_menu = Menu(title=menu.title, description=menu.description)
            session.add(new_menu)
            query = select(Menu).where(Menu.title == menu.title)  # todo refactor with 2 queries
            result = session.execute(query)
            session.commit()
            # session.refresh()
            return result.scalar_one_or_none()

    def edit_menu(self, menu_id: int, menu_item: MenuSchema):
        with Session(self.engine) as session:
            to_edit = session.get(Menu, menu_id)
            if to_edit:
                to_edit.title = menu_item.title
                to_edit.description = menu_item.description
                session.commit()
                return {"id": to_edit.id, "title": to_edit.title, "description": to_edit.description}
            else:
                return {"error": f"menu with id {menu_id} not found"}

    def delete_menu_item(self, menu_id: int):
        with Session(self.engine) as session:
            to_delete = session.get(Menu, menu_id)
            session.delete(to_delete)
            session.commit()
            return to_delete
