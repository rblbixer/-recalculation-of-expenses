from typing import Optional

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.expense_service import ExpenseService

router = Router()


def _parse_add_command(text: str) -> tuple[float, str, Optional[str]]:
    parts = text.split(maxsplit=3)
    if len(parts) < 3:
        raise ValueError("Недостаточно аргументов")
    try:
        amount = float(parts[1])
    except ValueError as exc:  # pragma: no cover - defensive
        raise ValueError("Сумма должна быть числом") from exc
    category = parts[2]
    description = parts[3] if len(parts) > 3 else None
    return amount, category, description


async def _service_from_message(message: Message) -> ExpenseService | None:
    session_maker = message.bot.get("session_maker")
    if session_maker is None:
        await message.answer("Сервис недоступен. Попробуйте позже.")
        return None
    session = session_maker()
    return ExpenseService(session)


@router.message(Command("add"))
async def add_expense(message: Message) -> None:
    service = await _service_from_message(message)
    if service is None:
        return

    text = message.text or ""
    try:
        amount, category, description = _parse_add_command(text)
    except ValueError:
        await message.answer("Используйте: /add 150 такси домой")
        return

    async with service.session:
        expense = await service.create(
            user_id=message.from_user.id,  # type: ignore[union-attr]
            amount=amount,
            category=category,
            description=description,
            username=message.from_user.username if message.from_user else None,
        )
    await message.answer(
        f"✅ Добавлен расход {expense.amount} на {expense.category}",
    )


def _format_expenses(expenses) -> str:
    if not expenses:
        return "Нет расходов."
    lines = []
    for item in expenses:
        time_str = item.created_at.strftime("%H:%M")
        desc = f" — {item.description}" if item.description else ""
        lines.append(f"{time_str}: {item.amount} · {item.category}{desc}")
    return "\n".join(lines)


@router.message(Command("today"))
async def today(message: Message) -> None:
    service = await _service_from_message(message)
    if service is None:
        return
    async with service.session:
        expenses = await service.list_today(message.from_user.id)  # type: ignore[union-attr]
    await message.answer(_format_expenses(expenses))


@router.message(Command("month"))
async def month(message: Message) -> None:
    service = await _service_from_message(message)
    if service is None:
        return
    async with service.session:
        expenses = await service.list_month(message.from_user.id)  # type: ignore[union-attr]
    await message.answer(_format_expenses(expenses))

