import sys
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases import db_session
from app.models import SubMenu
from app.submenu.schemas import SubMenuSchema

sys.setrecursionlimit(2000)


class SubMenuRepository:
    def __init__(self, session: AsyncSession = db_session) -> None:
        self.session: AsyncSession = session

    async def get_all(self, menu_id: int) -> Sequence[SubMenu]:
        query_result = await self.session.execute(select(SubMenu).where(SubMenu.menu_id == menu_id))
        submenus = query_result.scalars().all()
        return submenus

    async def get_one(self, menu_id: int, submenu_id: int) -> SubMenu | None:
        query = select(SubMenu).where(and_(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id))
        query_result = await self.session.execute(query)
        submenu = query_result.scalar_one_or_none()
        return submenu

    async def post(self, menu_id: int, submenu: SubMenuSchema) -> SubMenu:
        menu_id = int(menu_id)
        new_submenu = SubMenu(menu_id=menu_id, **submenu.model_dump())
        self.session.add(new_submenu)
        await self.session.commit()
        await self.session.refresh(new_submenu)
        return new_submenu

    async def patch(self, menu_id: int, submenu_id: int, submenu: SubMenuSchema) -> SubMenu:
        menu_id = int(menu_id)
        submenu_id = int(submenu_id)
        query = select(SubMenu).where(and_(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id))
        result = await self.session.execute(query)
        to_edit = result.scalar_one_or_none()
        if to_edit:
            to_edit.title = submenu.title
            to_edit.description = submenu.description
            await self.session.commit()
            await self.session.refresh(to_edit)
            return to_edit
        else:
            raise HTTPException(status_code=404, detail='submenu not found')

    async def delete(self, menu_id: int, submenu_id: int) -> dict:
        query = delete(SubMenu).where(and_(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id))
        await self.session.execute(query)
        await self.session.commit()
        return {'status': True, 'message': 'The submenu has been deleted'}
