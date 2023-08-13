from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.menu.schemas import MenuSchema
from app.models import Menu, SubMenu


class MenuRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def get_all(self) -> Sequence[Menu]:
        query = await self.session.execute(select(Menu))
        menus = query.scalars().all()
        return menus

    async def get_one(self, menu_id: int) -> Menu:
        query = await self.session.execute(select(Menu).where(Menu.id == menu_id))
        menu = query.scalar_one_or_none()
        return menu

    async def post(self, menu: MenuSchema) -> Menu:
        new_menu = Menu(
            **menu.model_dump()
        )
        self.session.add(new_menu)
        await self.session.commit()
        await self.session.refresh(new_menu)
        return new_menu

    async def patch(self, menu_id: int, menu: MenuSchema) -> Menu | None:
        to_edit = await self.session.get(Menu, menu_id)
        if to_edit:
            to_edit.title = menu.title
            to_edit.description = menu.description
            await self.session.commit()
            await self.session.refresh(to_edit)
            return to_edit
        else:
            raise HTTPException(status_code=404, detail='menu not found')

    async def delete(self, menu_id: int) -> dict:
        query = delete(Menu).where(Menu.id == menu_id)
        await self.session.execute(query)
        await self.session.commit()
        return {'status': True, 'message': 'The menu has been deleted'}

    async def get_all_entity(self) -> list:
        result = await self.session.execute(
            select(Menu).options(selectinload(Menu.submenus).selectinload(SubMenu.dishes)))
        menus = result.scalars().all()

        menus_list = []
        for menu_item in menus:
            menu_data = {
                'id': str(menu_item.id), 'title': menu_item.title, 'description': menu_item.description,
                'submenus': [
                    {
                        'id': str(submenu_item.id), 'title': submenu_item.title, 'description': submenu_item.description,
                        'dishes': [
                            {
                                'id': str(dish_item.id), 'title': dish_item.title, 'description': dish_item.description,
                                'price': str(dish_item.price)
                            } for dish_item in submenu_item.dishes
                        ]
                    } for submenu_item in menu_item.submenus
                ]
            }
            menus_list.append(menu_data)
        return menus_list
