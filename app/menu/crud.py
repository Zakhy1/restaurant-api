from sqlalchemy import select, func, delete
from sqlalchemy.orm import Session

from app.menu.schema import Menu as MenuSchema
from app.models import Menu, SubMenu, Dish, CrudOperations


class MenuOperations(CrudOperations):
    def get_menus(self):
        with Session(self.engine) as session:
            menus = session.query(Menu).all()
            return menus

    def get_menu(self, menu_id: int):
        with Session(self.engine) as session:
            query = select(Menu).where(Menu.id == menu_id).select_from()
            menu = session.execute(query).scalar_one_or_none()

            query = select(func.count("*")).where(SubMenu.menu_id == menu_id).select_from(SubMenu)
            result = session.execute(query)
            submenus_count = result.scalar()

            query = select(func.count("*")).where(SubMenu.menu_id == menu_id).select_from(SubMenu) \
                .where(Dish.submenu_id == SubMenu.id)
            dishes_count = session.execute(query).scalar()
            if menu:
                return {"id": str(menu.id), "title": menu.title,
                        "description": menu.description, "submenus_count": submenus_count, "dishes_count": dishes_count}
            else:
                return None

    def add_menu(self, menu: MenuSchema):
        with Session(self.engine) as session:
            query = select(Menu).where(Menu.title == menu.title)
            result = session.execute(query).scalar_one_or_none()
            if result:
                return {"error": f"menu with name '{menu.title}' already exist"}
            new_menu = Menu(title=menu.title, description=menu.description)
            session.add(new_menu)
            query = select(Menu).where(Menu.title == menu.title)
            result = session.execute(query).scalar_one_or_none()
            session.commit()
            return {"id": str(result.id), "title": result.title, "description": result.description}

    def edit_menu(self, menu_id: int, menu_item: MenuSchema):
        with Session(self.engine) as session:
            to_edit = session.get(Menu, menu_id)
            if to_edit:
                to_edit.title = menu_item.title
                to_edit.description = menu_item.description
                session.commit()
                return {"id": str(to_edit.id), "title": to_edit.title, "description": to_edit.description}
            else:
                return {"error": f"menu with id {menu_id} not found"}

    def delete_menu_item(self, menu_id: int):
        with Session(self.engine) as session:
            query = select(Menu).where(Menu.id == menu_id)
            to_delete = session.execute(query).scalar_one_or_none()
            query = delete(Menu).where(Menu.id == menu_id)
            session.execute(query)
            session.commit()
            return to_delete
