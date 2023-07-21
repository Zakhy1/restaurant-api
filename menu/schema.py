from pydantic import BaseModel


class Menu(BaseModel):
    id: int
    title: str
    description: str

    class Confing:
        orm_mode = True