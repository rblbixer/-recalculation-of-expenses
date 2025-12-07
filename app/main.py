import asyncio
from contextlib import asynccontextmanager, suppress
from typing import Optional

from fastapi import FastAPI

from app.api.main import api_router
from app.bot.loader import create_bot
from app.core.config import settings
from app.core.database import get_session_maker, init_models
from app.core.exceptions import add_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    bot_task: Optional[asyncio.Task] = None
    bot = None

    if settings.bot_token and not settings.testing:
        bot, dp = create_bot(settings.bot_token)
        bot["session_maker"] = get_session_maker()
        bot_task = asyncio.create_task(dp.start_polling(bot))

    yield

    if bot_task:
        bot_task.cancel()
        with suppress(asyncio.CancelledError):
            await bot_task
    if bot:
        await bot.session.close()


app = FastAPI(
    title="Finance Bot API",
    debug=settings.debug,
    lifespan=lifespan,
)

add_exception_handlers(app)
app.include_router(api_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.api_host, port=settings.api_port, reload=settings.debug)

