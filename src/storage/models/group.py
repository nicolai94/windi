from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.models.base import Base
from src.storage.models.mixins.id_int_pk import IdIntPkMixin
from src.storage.models.users_groups import users_groups_table

if TYPE_CHECKING:
    from src.storage.models.user import User


class Group(IdIntPkMixin, Base):
    name: Mapped[str]
    owner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    owner: Mapped["User"] = relationship(back_populates="owner_groups")

    members: Mapped[List["User"]] = relationship(
        secondary=users_groups_table, back_populates="groups"
    )
