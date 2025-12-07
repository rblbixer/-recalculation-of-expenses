from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.expense import Expense
from app.repositories.expenses import ExpenseRepository
from app.repositories.users import UserRepository


class ExpenseService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.expenses = ExpenseRepository(session)
        self.users = UserRepository(session)

    async def create(
        self,
        user_id: int,
        amount: float,
        category: str,
        description: Optional[str] = None,
        category_id: Optional[int] = None,
        username: Optional[str] = None,
    ) -> Expense:
        await self.users.get_or_create(user_id=user_id, username=username)
        expense = await self.expenses.create(
            user_id=user_id,
            amount=amount,
            category=category,
            description=description,
            category_id=category_id,
        )
        await self.session.commit()
        await self.session.refresh(expense)
        return expense

    async def list_today(self, user_id: int) -> List[Expense]:
        now = datetime.now(timezone.utc)
        start = datetime(year=now.year, month=now.month, day=now.day, tzinfo=timezone.utc)
        return await self.expenses.list_between(user_id, start, now)

    async def list_month(self, user_id: int) -> List[Expense]:
        now = datetime.now(timezone.utc)
        start = datetime(year=now.year, month=now.month, day=1, tzinfo=timezone.utc)
        return await self.expenses.list_between(user_id, start, now)

