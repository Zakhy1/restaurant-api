from pydantic import BaseModel


class DishSchema(BaseModel):
    title: str
    description: str
    price: str | float


class DishSchemaResponse(DishSchema):
    id: str | int
