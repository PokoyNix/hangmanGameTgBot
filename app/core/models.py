from enum import Enum, auto


class GameStatus(Enum):
    IN_PROGRESS = auto()
    WON = auto()
    LOST = auto()


class GuessResult(Enum):
    CORRECT = auto()
    INCORRECT = auto()
    ALREADY_GUESSED = auto()
    GAME_FINISHED = auto()

