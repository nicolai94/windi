from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.models.base import Base
from src.storage.models.mixins.id_int_pk import IdIntPkMixin
from src.storage.models.users_groups import users_groups_table

if TYPE_CHECKING:
    from src.storage.models.group import Group


class User(IdIntPkMixin, Base):
    name: Mapped[str]
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str]

    owner_groups: Mapped[List["Group"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )

    groups: Mapped[List["Group"]] = relationship(
        secondary=users_groups_table, back_populates="members"
    )
