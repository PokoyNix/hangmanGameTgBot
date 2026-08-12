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
    """
    Render the hangman state for the given number of remaining attempts.
    """

    if not 0 <= attempts_left <= max_attempts:
        raise ValueError(
                "attempts_left must be between 0 and max_attempts"
        )

    index = max_attempts - attempts_left
    
    if index >= len(STAGES):
        raise ValueError(
                "Number of stages does not match max_attempts"
        )
    return STAGES[index]

