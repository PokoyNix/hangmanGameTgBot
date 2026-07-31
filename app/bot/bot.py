import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import settings
from app.services.game_service import GameService
from app.bot.handlers import router

logger = logging.getLogger(__name__)

async def start_bot():
    '''
    Configure and start the Telegram bot.

    Initializes bot commands; registers routers,
    injects application services and starts polling.
    '''
    logger.info('Initializing Telegram bot...')
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # create service
    game_service = GameService()

    # throw in handlers
    dp['game_service'] = game_service


    dp.include_router(router)
    logger.info('Router registered.')

    await bot.set_my_commands([
        BotCommand(command='start', description='Start Game'),
    ])
    logging.info('Bot commands configured.')

    logging.info('Starting polling...')
    try:
        await dp.start_polling(bot)
    except Exception:
        logger.exception('Bot stopped unexpectedly.')
        raise
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start_bot())

