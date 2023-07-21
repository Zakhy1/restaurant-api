from pydantic import BaseModel


class SubMenu(BaseModel):
    id: int
    title: str
    description: str
    menu_id: int

    class Confing:
        orm_mode = True