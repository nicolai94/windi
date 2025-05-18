from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage import Group, User

from src.storage.repositories.base import BaseRepository


class GroupRepository(BaseRepository[Group]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Group)

    async def create_group(self, name: str, owner: User, members: list[User]) -> Group:
        group = Group(
            name=name,
            owner=owner,
            members=members,
        )
        self.session.add(group)

        try:
            await self.session.commit()
            await self.session.refresh(group)
        except SQLAlchemyError:
            await self.session.rollback()
            raise

        return group
