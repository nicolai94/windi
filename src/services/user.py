from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from starlette import status

from src.api.schemas.user import UserCreateInput, Token
from src.core.security import create_access_token, verify_password
from src.storage.repositories.user import UserRepository


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, data: UserCreateInput) -> Token:
        user_repo = UserRepository(self.session)
        user = await user_repo.create_user(data)

        return Token(access_token=create_access_token({"sub": user.email}))

    async def login_with_oauth(self, form_data: OAuth2PasswordRequestForm) -> Token:
        user_repo = UserRepository(self.session)
        user = await user_repo.get_user_by_email(form_data.username)
        if not user or not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        return Token(access_token=create_access_token({"sub": user.email}))
