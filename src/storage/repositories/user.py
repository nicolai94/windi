from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.api.schemas.user import UserCreateInput
from src.core.security import hash_password
from src.storage import User

from src.storage.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_user_by_id(self, user_id: int):
        stmt = select(self.model).where(self.model.id == user_id)
        result = await self.session.execute(stmt)

        return result.scalars().first()

    async def get_users_by_ids(self, member_ids: list[int]) -> List[User]:
        stmt = select(self.model).where(self.model.id.in_(member_ids))
        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def create_user(self, data: UserCreateInput) -> User:
        user = User(
            name=data.name, email=data.email, password=hash_password(data.password)
        )
        self.session.add(user)

        try:
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()
            raise

        return user

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)

        return result.scalars().first()
