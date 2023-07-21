from database import db_session
from models import Menu
from menu.schema import Menu as MenuSchema
from sqlalchemy import select


def get_menus():
    menus = db_session.query(Menu).all()
    return menus


def get_menu(menu_id):
    menu = db_session.get(Menu, menu_id)
    return menu


def add_menu_item(menu: MenuSchema):
    query = select(Menu).where(Menu.title == menu.title)
    result = db_session.execute(query)
    if result.one():
        return {"error": f"menu with name {menu.title} exist"}
    new_menu = Menu(title=menu.title, description=menu.description)
    db_session.add(new_menu)
    db_session.commit()
    return new_menu


def edit_menu_item(menu_id: int, menu_item: MenuSchema):
    to_edit = db_session.get(Menu, menu_id)
    if to_edit:
        to_edit.title = menu_item.title
        to_edit.description = menu_item.description
        db_session.commit()
        return {"id": to_edit.id, "title": to_edit.title, "description": to_edit.description}
    else:
        return {"error": f"menu with id {menu_id} not found"}


def delete_menu_item(menu_id: int):
    to_delete = db_session.get(Menu, menu_id)
    db_session.delete(to_delete)
    db_session.commit()
    return to_delete
