from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.services.expense_service import ExpenseService


async def get_expense_service(
    session: AsyncSession = Depends(get_session),
) -> ExpenseService:
    return ExpenseService(session)

