from pydantic import BaseModel


class DishSchema(BaseModel):
    title: str
    description: str
    price: float


class DishSchemaResponse(DishSchema):
    id: str | int
    price: str
