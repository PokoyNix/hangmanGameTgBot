STAGES = [
    """
 +---+
 |   |
     |
     |
     |
     |
=========
""",
    """
 +---+
 |   |
 O   |
     |
     |
     |
=========
""",
    """
 +---+
 |   |
 O   |
 |   |
     |
     |
=========
""",
    """
 +---+
 |   |
 O   |
/|   |
     |
     |
=========
""",
    """
 +---+
 |   |
 O   |
/|\\  |
     |
     |
=========
""",
    """
 +---+
 |   |
 O   |
/|\\  |
/    |
     |
=========
""",
    """
 +---+
 |   |
 O   |
/|\\  |
/ \\  |
     |
=========
"""
]


def render_hangman(attempts_left: int, max_attempts: int = 6) -> str:
    index = max_attempts - attempts_left
    return STAGES[index]

