from pydantic import BaseModel

from app.dishes.schemas import DishSchema
from app.submenu.schemas import SubMenuSchema


class MenuSchema(BaseModel):
    title: str
    description: str


class MenuSchemaResponse(MenuSchema):
    id: str | int
    submenus_count: int
    dishes_count: int


class FullDishResponse(DishSchema):
    id: str


class FullSubMenuResponse(SubMenuSchema):
    id: str
    dishes: list[FullDishResponse]


class FullMenuResponse(MenuSchema):
    id: str
    submenus: list[FullSubMenuResponse]


class FullMenuListResponse(BaseModel):
    menus: list[FullMenuResponse]
