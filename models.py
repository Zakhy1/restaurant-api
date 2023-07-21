# Модели данных
from typing import List

from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base


class Menu(Base):
    __tablename__ = "menu"

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String)
    description = mapped_column(String)
    submenus: Mapped[List["Submenu"]] = relationship(back_populates="menu", cascade="all, delete")


class Submenu(Base):
    __tablename__ = "submenu"

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String)
    description = mapped_column(String)
    menu_id = mapped_column(Integer, ForeignKey("menu.id"))
    menu = relationship("Menu", backref="submenu")


class Dish(Base):
    __tablename__ = "dishes"

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String)
    description = mapped_column(String)
    price = mapped_column(Float)
    submenu_id = mapped_column(ForeignKey("submenu.id"))
    submenu = relationship("Submenu", backref="dish")