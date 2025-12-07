from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies import get_expense_service
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.services.expense_service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", response_model=ExpenseResponse)
async def create_expense(
    expense_data: ExpenseCreate,
    expense_service: ExpenseService = Depends(get_expense_service),
) -> ExpenseResponse:
    expense = await expense_service.create(**expense_data.model_dump())
    return ExpenseResponse.model_validate(expense)


@router.get("/today", response_model=List[ExpenseResponse])
async def list_today(
    user_id: int, expense_service: ExpenseService = Depends(get_expense_service)
) -> List[ExpenseResponse]:
    expenses = await expense_service.list_today(user_id)
    return [ExpenseResponse.model_validate(item) for item in expenses]


@router.get("/month", response_model=List[ExpenseResponse])
async def list_month(
    user_id: int, expense_service: ExpenseService = Depends(get_expense_service)
) -> List[ExpenseResponse]:
    expenses = await expense_service.list_month(user_id)
    return [ExpenseResponse.model_validate(item) for item in expenses]

