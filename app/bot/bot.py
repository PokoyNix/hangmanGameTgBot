import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import settings
from app.services.game_service import GameService
from app.bot.handlers import router

logger = logging.getLogger(__name__)


async def start_bot() -> None:
    '''
    Configure and start the Telegram bot.

    Initializes bot commands; registers routers,
    injects application services and starts polling.
    '''
    logger.info('Initializing Telegram bot...')
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )
    dp = Dispatcher()

    logger.info('Initializing application services.')
    game_service = GameService()
    logger.info('Services initialized.')

    dp['game_service'] = game_service

    dp.include_router(router)
    logger.info('Router registered.')

    await bot.set_my_commands([
        BotCommand(command='start', description='Start Game'),
    ])
    logger.info('Bot commands configured.')

    logger.info('Starting polling...')
    try:
        await dp.start_polling(bot)
    except Exception:
        logger.exception('Bot stopped unexpectedly.')
        raise
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start_bot())

