from pydantic import BaseModel


class Menu(BaseModel):
    title: str
    description: str

    class Confing:
        orm_mode = True