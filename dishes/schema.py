from pydantic import BaseModel


class Dishes(BaseModel):
    title: str
    description: str
    price: float

    class Confing:
        orm_mode = True
