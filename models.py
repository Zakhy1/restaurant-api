from typing import List

from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Menu(Base):
    __tablename__ = "menus"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), unique=True)
    description: Mapped[str] = mapped_column(String(128))

    submenus: Mapped[List["SubMenu"]] = relationship(
        back_populates="menu", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Menu(id={self.id}, title={self.title}, description={self.description})"

    def __str__(self):
        str(self)


class SubMenu(Base):
    __tablename__ = "submenus"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), unique=True)
    description: Mapped[str] = mapped_column(String(128))

    menu_id: Mapped[int] = mapped_column(ForeignKey("menus.id"))
    menu: Mapped["Menu"] = relationship(back_populates="submenus")

    dishes: Mapped[List["Dish"]] = relationship(
        back_populates="submenu", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"SubMenu(id={self.id}, title={self.title}, description={self.description}, menu_id={self.menu_id})"

    def __str__(self):
        str(self)


class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), unique=True)
    description: Mapped[str] = mapped_column(String(128))
    price: Mapped[float] = mapped_column(Float())

    submenu_id: Mapped[int] = mapped_column(ForeignKey("submenus.id", ondelete="CASCADE"))
    submenu: Mapped["SubMenu"] = relationship(back_populates="dishes", cascade="all, delete-orphan", single_parent=True)

    def __repr__(self) -> str:
        return f"Dish(id={self.id}, title={self.title}, description={self.description}, price={self.price}, " \
               f"submenu_id={self.submenu_id})"

    def __str__(self):
        str(self)
