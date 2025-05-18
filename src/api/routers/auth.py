from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.services.user import UserService
from src.storage.models.db_helper import Session
from src.api.schemas.user import UserCreateInput, Token

router = APIRouter()


@router.post("/register", response_model=Token)
async def register(data: UserCreateInput, session: Session):
    user_service = UserService(session)

    return await user_service.create_user(data)


@router.post("/login", response_model=Token)
async def login(session: Session, form_data: OAuth2PasswordRequestForm = Depends()):
    user_service = UserService(session)

    return await user_service.login_with_oauth(form_data)
