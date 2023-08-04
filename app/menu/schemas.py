from pydantic import BaseModel


class MenuSchema(BaseModel):
    title: str
    description: str


class MenuSchemaResponse(MenuSchema):
    id: str | int
    submenus_count: int
    dishes_count: int
