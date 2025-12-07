from datetime import datetime
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.expense import Expense
from app.repositories.expenses import ExpenseRepository


class ReportService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.expenses = ExpenseRepository(session)

    async def total_between(self, user_id: int, start: datetime, end: datetime) -> float:
        items: List[Expense] = await self.expenses.list_between(user_id, start, end)
        return float(sum(item.amount for item in items))

    async def by_category(
        self, user_id: int, start: datetime, end: datetime
    ) -> Dict[str, float]:
        items: List[Expense] = await self.expenses.list_between(user_id, start, end)
        totals: Dict[str, float] = {}
        for item in items:
            totals[item.category] = totals.get(item.category, 0) + float(item.amount)
        return totals

