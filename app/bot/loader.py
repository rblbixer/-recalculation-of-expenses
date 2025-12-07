from aiogram import Bot, Dispatcher

from app.bot.handlers import commands, expenses


def create_bot(token: str) -> tuple[Bot, Dispatcher]:
    bot = Bot(token)
    dp = Dispatcher()
    dp.include_router(commands.router)
    dp.include_router(expenses.router)
    return bot, dp

