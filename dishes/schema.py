from pydantic import BaseModel


class Dishes(BaseModel):
    id: int
    title: str
    description: str
    price: float
    submenu_id: int

    class Confing:
        orm_mode = True
