from sqlalchemy import select

from database import db_session
from models import SubMenu


def get_submenus(menu_id: int):  # TODO DONE with data and special conditions
    query = select(SubMenu).where(SubMenu.menu_id == menu_id)
    res = db_session.execute(query)
    for i in res:
        print(i)


def get_submenu(menu_id: int, submenu_id: int):  # TODO
    query = select(SubMenu).where(SubMenu.menu_id == menu_id and SubMenu.menu_id == submenu_id)
    res = db_session.execute(query)


def add_submenu(menu_id, submenu: SubMenu):
    query = select(SubMenu).where(SubMenu.title == SubMenu.title)
    result = db_session.execute(query)
    if result.one():
        return {"error": f"submenu with name '{submenu.title}' exist"}
    new_submenu = SubMenu(title=submenu.title, description=submenu.description, menu_id=submenu.menu_id)
