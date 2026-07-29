import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BOT_TOKEN: str | None = os.getenv('BOT_TOKEN')


settings = Settings()

