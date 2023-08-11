from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.databases import db_session
from app.menu.schemas import MenuSchema
from app.models import Menu


class MenuRepository:  # TODO Вынести в notify обработку после запросов
    def __init__(self, session: Session = db_session) -> None:
        self.session: Session = session

    async def get_all(self) -> Sequence[Menu]:
        menus = self.session.execute(select(Menu)).scalars().all()
        return menus

    async def get_one(self, menu_id: int) -> Menu:
        query = select(Menu).where(Menu.id == menu_id)
        menu = self.session.execute(query).scalar_one_or_none()
        return menu

    async def post(self, menu: MenuSchema) -> Menu:
        new_menu = Menu(
            **menu.model_dump()
        )
        self.session.add(new_menu)
        self.session.commit()
        self.session.refresh(new_menu)
        return new_menu

    async def patch(self, menu_id: int, menu: MenuSchema) -> Menu | None:
        to_edit = self.session.get(Menu, menu_id)
        if to_edit:
            to_edit.title = menu.title
            to_edit.description = menu.description
            self.session.commit()
            self.session.refresh(to_edit)
            return to_edit
        else:
            raise HTTPException(status_code=404, detail='menu not found')

    async def delete(self, menu_id: int) -> dict:
        query = delete(Menu).where(Menu.id == menu_id)
        self.session.execute(query)
        self.session.commit()
        return {'status': True, 'message': 'The menu has been deleted'}
