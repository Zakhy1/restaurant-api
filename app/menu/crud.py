from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.database import db_session

from app.menu.schemas import MenuSchemaResponse, MenuSchema
from app.models import Menu


class MenuRepository:  # TODO Вынести в notify обработку после запросов
    def __init__(self, session: Session = db_session):
        self.session: Session = session

    def get_all(self):
        menus = self.session.execute(select(Menu)).scalars().all()
        menus_lst = []
        for item in menus:
            response = MenuSchemaResponse(**item.__dict__)
            response.id = str(response.id)
            menus_lst.append(response)
        return menus_lst

    def get_one(self, menu_id: int):
        query = select(Menu).where(Menu.id == menu_id)
        menu = self.session.execute(query).scalar_one_or_none()
        if menu:
            menu_dict = menu.__dict__
            menu_dict["id"] = str(menu_dict["id"])
            return MenuSchemaResponse(**menu_dict)
        else:
            raise HTTPException(status_code=404, detail="menu not found")

    def post(self, menu: MenuSchema):
        new_menu = Menu(
            **menu.model_dump()
        )
        self.session.add(new_menu)
        self.session.commit()
        self.session.refresh(new_menu)
        menu_dict = new_menu.__dict__
        menu_dict["id"] = str(menu_dict["id"])
        return MenuSchemaResponse(**menu_dict)

    def patch(self, menu_id: int, menu: MenuSchema):
        to_edit = self.session.get(Menu, menu_id)
        if to_edit:
            to_edit.title = menu.title
            to_edit.description = menu.description
            self.session.commit()
            self.session.refresh(to_edit)
            menu_dict = to_edit.__dict__
            menu_dict["id"] = str(menu_dict["id"])
            return MenuSchemaResponse(**menu_dict)
        else:
            raise HTTPException(status_code=404, detail="menu not found")

    def delete(self, menu_id: int):
        query = delete(Menu).where(Menu.id == menu_id)
        self.session.execute(query)
        self.session.commit()
        return {"status": True, "message": "The menu has been deleted"}
