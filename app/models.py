from sqlalchemy import ForeignKey, Numeric, String, func, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    column_property,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class Dish(Base):
    __tablename__ = 'dishes'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(128))
    price: Mapped[Numeric] = mapped_column(Numeric(precision=10, scale=2))

    submenu_id: Mapped[int] = mapped_column(ForeignKey('submenus.id', ondelete='CASCADE'))
    submenu: Mapped['SubMenu'] = relationship(back_populates='dishes', cascade='all, delete-orphan', single_parent=True)

    def __repr__(self) -> str:
        return f'Dish(id={self.id}, title={self.title}, description={self.description}, price={self.price}, ' \
               f'submenu_id={self.submenu_id})'

    def __str__(self):
        str(self)


class SubMenu(Base):
    __tablename__ = 'submenus'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(128))

    menu_id: Mapped[int] = mapped_column(ForeignKey('menus.id'))
    menu: Mapped['Menu'] = relationship(back_populates='submenus')

    dishes: Mapped[list['Dish']] = relationship(
        back_populates='submenu', cascade='all, delete-orphan'
    )

    dishes_count = column_property(
        select(func.count(Dish.id)).where(Dish.submenu_id.in_(
            select(id)
        )).correlate_except(Dish).as_scalar()
    )

    def __repr__(self) -> str:
        return f'SubMenu(id={self.id}, title={self.title}, description={self.description}, menu_id={self.menu_id})'

    def __str__(self):
        str(self)


class Menu(Base):
    __tablename__ = 'menus'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(128))

    submenus: Mapped[list['SubMenu']] = relationship(
        back_populates='menu', cascade='all, delete-orphan'
    )

    submenus_count = column_property(
        select(func.count(SubMenu.id)).where(
            SubMenu.menu_id == id).correlate_except(SubMenu).as_scalar()
    )
    dishes_count = column_property(
        select(func.count(Dish.id)).where(Dish.submenu_id.in_(
            select(SubMenu.id).where(SubMenu.menu_id == id)
        )).correlate_except(Dish).as_scalar()
    )

    def __repr__(self) -> str:
        return f'Menu(id={self.id}, title={self.title}, description={self.description})'

    def __str__(self):
        str(self)
