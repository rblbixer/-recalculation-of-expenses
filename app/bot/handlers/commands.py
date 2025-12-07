from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.bot.handlers.keyboards import main_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Привет! Я помогу вести расходы.\n"
        "Команды:\n"
        "/add 150 такси домой\n"
        "/today — расходы за сегодня\n"
        "/month — расходы за месяц",
        reply_markup=main_keyboard(),
    )


@router.message(Command("help"))
async def help_cmd(message: Message) -> None:
    await message.answer(
        "Доступные команды:\n"
        "/start — приветствие\n"
        "/add <сумма> <категория> [описание]\n"
        "/today — расходы за сегодня\n"
        "/month — расходы за месяц\n"
        "/categories — список категорий (скоро)\n"
        "/stats — краткая статистика (скоро)"
    )

