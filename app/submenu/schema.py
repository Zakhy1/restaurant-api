from typing import Optional

from pydantic import BaseModel


class SubMenu(BaseModel):
    title: str
    description: str

    class Confing:
        orm_mode = True
