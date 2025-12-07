from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.expense import Expense
from app.repositories.base import BaseRepository


class ExpenseRepository(BaseRepository):
    async def create(
        self,
        user_id: int,
        amount: float,
        category: str,
        description: str | None = None,
        category_id: int | None = None,
    ) -> Expense:
        expense = Expense(
            user_id=user_id,
            amount=amount,
            category=category,
            description=description,
            category_id=category_id,
        )
        self.session.add(expense)
        await self.session.flush()
        return expense

    async def list_between(
        self, user_id: int, start: datetime, end: datetime
    ) -> List[Expense]:
        query = (
            select(Expense)
            .where(Expense.user_id == user_id)
            .where(Expense.created_at >= start)
            .where(Expense.created_at <= end)
            .order_by(Expense.created_at.desc())
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())


async def with_session(session: AsyncSession) -> ExpenseRepository:
    return ExpenseRepository(session)

