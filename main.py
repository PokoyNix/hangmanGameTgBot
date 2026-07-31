import asyncio

from app.bot.bot import start_bot
from app.infrastructure.logging import configure_logging


if __name__ == '__main__':
    configure_logging()
    asyncio.run(start_bot())

