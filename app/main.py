from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases import get_session
from app.dishes.router import dish_router
from app.menu.router import menu_router
from app.menu.schemas import FullMenuListResponse
from app.menu.service import MenuService
from app.submenu.router import submenu_router
from create_tables import init_models

app = FastAPI()


@app.on_event('startup')
async def create_tables():
    await init_models()


@app.get('/api/v1/menus/all-items')
async def get_all(session: AsyncSession = Depends(get_session)) -> FullMenuListResponse:
    service = MenuService(session)
    return await service.get_all_items()


app.include_router(menu_router, prefix='/api/v1', tags=['menus'])
app.include_router(submenu_router, prefix='/api/v1/menus/{menu_id}', tags=['submenus'])
app.include_router(dish_router, prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}', tags=['dishes'])
