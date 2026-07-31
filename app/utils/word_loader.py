from __future__ import annotations

import logging
import random

from config import settings

logger = logging.getLogger(__name__)


def load_words() -> list[str]:
    """
    Load all valid words from the dictionary file.

    Returns:
       List of  lowercase words.
    """

    if not settings.WORDS_PATH.exists():
        raise FileNotFoundError(
                f'Words file not found: {settings.WORDS_PATH}'
        )
    
    with settings.WORDS_PATH.open('r', encoding='utf-8') as file:
        words = [
                word.lower()
                for word in file.read().split()
                if word.isalpha()
        ]
    
    if not words:
        raise ValueError('Dictionary is empty.')
    
    logger.info(
            'Loaded %s words.',
            len(words),
    )
    
    return words


_WORDS = load_words()


def get_random_word() -> str:
    '''
    Return a random word from the loaded dictionary.
    '''
    return random.choice(_WORDS)

