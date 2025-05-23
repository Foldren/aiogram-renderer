import logging
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv
from asyncio import run
from redis.asyncio import Redis
import routers
from bot_mode import BotMode
from configure import configure_renderer
from example.windows import main_window, alert_mode

load_dotenv()

bot = Bot(token=getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
redis_states = Redis.from_url(getenv("REDIS_URL"), db=14, decode_responses=True)
rd_storage = RedisStorage(redis=redis_states, key_builder=DefaultKeyBuilder(with_destiny=True))
dp = Dispatcher(storage=rd_storage)


async def main():
    logging.basicConfig(level=logging.INFO)

    await configure_renderer(
        dp=dp,
        # Подключаем окна
        windows=[main_window],
        # Задаем режимы бота (первый активный по умолчанию)
        modes=[
            BotMode(
                name="decoder_h2",
                values=["off 🟥⬜️  Декодер H264", "on ⬜️🟩  Декодер H264"]
            ),
            BotMode(
                name="decoder_h263",
                values=["off 🟥⬜️  h3", "on ⬜️🟩  h2"],
                alert_window=alert_mode
            )
        ]
    )

    # Подключаем роутер с хендлерами
    dp.include_routers(routers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run(main())
