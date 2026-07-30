import random
from pathlib import Path

WORDS_FILE = Path('data/words.txt')


def load_words() -> list[str]:
    with open(WORDS_FILE, 'r', encoding='utf-8') as f:
        return [line.strip().lower() for line in f if line.strip()]


def get_random_word() -> str:
    words = load_words()
    return random.choice(words)

