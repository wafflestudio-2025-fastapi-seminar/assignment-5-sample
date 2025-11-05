from typing import Annotated
import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from wapang.app.users.models import User
from wapang.database.async_connection import get_async_db_session
from wapang.database.connection import get_db_session

class UserRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_db_session)]) -> None:
        self.session = session

    async def create_user(self, email: str, hashed_password: str) -> User:
        user = User(email=email, hashed_password=hashed_password)
        self.session.add(user)

        await self.session.flush()
        
        return user
    
    async def update_user(self, user: User) -> User:
        await self.session.merge(user)
        await self.session.flush()
        return user

    async def get_user_by_id(self, user_id: str) -> User | None:
        return await self.session.scalar(select(User).where(User.id == user_id))

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.session.scalar(select(User).where(User.email == email))

    async def get_user_by_nickname(self, nickname: str) -> User | None:
        return await self.session.scalar(select(User).where(User.nickname == nickname))