from typing import Optional

from sqlalchemy import select

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    async def get(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, user_id: int, username: Optional[str] = None) -> User:
        user = User(id=user_id, username=username)
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_or_create(self, user_id: int, username: Optional[str] = None) -> User:
        existing = await self.get(user_id)
        if existing:
            return existing
        return await self.create(user_id, username=username)

