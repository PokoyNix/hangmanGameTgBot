from __future__ import annotations

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


class Settings:
    '''
    Application configuration.
    '''

    BOT_TOKEN: str | None = os.getenv('BOT_TOKEN')

    ALLOWED_THREAD_IDS: list[int] = [
            int(thread_id)
            for thread_id in os.getenv('ALLOWED_THREAD_IDS', '').split(',')
            if thread_id
    ]

    DATA_DIR: Path = BASE_DIR / 'data'

    WORDS_PATH: Path = DATA_DIR / 'words.txt'

    LOG_DIR: Path = BASE_DIR / 'logs'

    LOG_LEVEL: int = logging.INFO


settings = Settings()

