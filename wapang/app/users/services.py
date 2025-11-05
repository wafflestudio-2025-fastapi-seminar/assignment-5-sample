from typing import Annotated
from argon2 import PasswordHasher

from fastapi import Depends
from wapang.app.users.models import User
from wapang.app.users.repositories import UserRepository
from wapang.app.users.exceptions import EmailAlreadyExistsException
from wapang.app.users.schemas import UserUpdateRequest
from wapang.common.exceptions import InvalidFormatException

class UserService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends()]) -> None:
        self.user_repository = user_repository

    async def create_user(self, email: str, password: str) -> User:        
        if await self.user_repository.get_user_by_email(email):
            raise EmailAlreadyExistsException()

        hashed_password = PasswordHasher().hash(password)

        return await self.user_repository.create_user(email, hashed_password)