import sys

from fastapi import HTTPException
from sqlalchemy import and_, delete
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import db_session
from app.models import Dish
from app.models import SubMenu
from app.submenu.schemas import SubMenuSchema, SubMenuSchemaResponse

sys.setrecursionlimit(2000)


class SubMenuRepository:
    def __init__(self, session: Session = db_session):
        self.session: Session = session

    def get_all(self, menu_id: int):
        query_result = self.session.execute(select(SubMenu).where(SubMenu.menu_id == menu_id))
        submenus = query_result.scalars().all()
        submenus_lst = []
        for submenu in submenus:
            submenu_response = SubMenuSchemaResponse(**submenu.__dict__)
            submenu_response.id = str(submenu_response.id)
            submenus_lst.append(submenu_response)
        return submenus_lst

    def get_one(self, menu_id: int, submenu_id: int):
        query = select(SubMenu).where(and_(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id))
        query_result = self.session.execute(query)
        submenu = query_result.scalar_one_or_none()
        if submenu:
            submenu_dict = submenu.__dict__
            submenu_dict["id"] = str(submenu_dict["id"])
            return SubMenuSchemaResponse(**submenu_dict)
        else:
            raise HTTPException(status_code=404, detail="submenu not found")

    def post(self, menu_id: int, submenu: SubMenuSchema):
        new_submenu = SubMenu(menu_id=menu_id, **submenu.model_dump())
        self.session.add(new_submenu)
        self.session.commit()
        self.session.refresh(new_submenu)
        to_return = new_submenu.__dict__
        to_return["id"] = str(to_return["id"])
        return SubMenuSchemaResponse(**to_return)

    def patch(self, menu_id, submenu_id, submenu: SubMenuSchema):
        query = select(SubMenu).where(and_(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id))
        result = self.session.execute(query)
        to_edit = result.scalar_one_or_none()
        if to_edit:
            to_edit.title = submenu.title
            to_edit.description = submenu.description
            self.session.commit()
            self.session.refresh(to_edit)
            to_return = to_edit.__dict__
            to_return["id"] = str(to_return["id"])
            return SubMenuSchemaResponse(**to_return)
        else:
            raise HTTPException(status_code=404, detail="submenu not found")

    def delete(self, menu_id: int, submenu_id: int):
        query = delete(SubMenu).where(and_(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id))
        self.session.execute(query)
        self.session.commit()
        return {"status": True, "message": "The submenu has been deleted"}
