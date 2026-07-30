import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BOT_TOKEN: str | None = os.getenv('BOT_TOKEN')
    ALLOW_THREAD_IDS: list[str] = os.getenv('ALLOW_THREAD_IDS').split(',')


settings = Settings()

