from pydantic import BaseModel


class SubMenuSchema(BaseModel):
    title: str
    description: str


class SubMenuSchemaResponse(SubMenuSchema):
    id: str | int
    dishes_count: int
