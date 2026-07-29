import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import settings
from app.services.game_service import GameService
from app.bot.handlers import router


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # create service
    game_service = GameService()

    # throw in handlers
    dp['game_service'] = game_service

    dp.include_router(router)

    await bot.set_my_commands([
        BotCommand(command='start', description='Start Game'),
    ])

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

