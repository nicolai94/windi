from sqlalchemy import Table, Column, ForeignKey

from src.storage.models.base import Base

users_groups_table = Table(
    "users_groups",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="NO ACTION"), primary_key=True),
    Column("group_id", ForeignKey("groups.id", ondelete="NO ACTION"), primary_key=True),
)
