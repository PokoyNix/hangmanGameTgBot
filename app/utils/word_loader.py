import random
from pathlib import Path

WORDS_PATH = Path('data/words.txt')


def load_words() -> list[str]:
    '''
    Load all valid words from the dictionary file.

    Returns:
        List of  lowercase words.
    '''
    with WORDS_PATH.open('r', encoding='utf-8') as file:
        return [
            line.strip().lower()
            for line in file.read().split()
            if line.strip().isalpha()
        ]


_WORDS = load_words()


def get_random_word() -> str:
    '''
    Return a random word from the loaded dictionary.
    '''
    return random.choice(_WORDS)

