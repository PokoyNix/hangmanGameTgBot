from dataclasses import dataclass
from enum import Enum


class GameStatus(str, Enum):
    """
    Represents current game state.
    """
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"


class GuessResult(str, Enum):
    """
    Represents result of a player's guess.
    """
    CORRECT = "correct"
    INCORRECT = "incorrect"
    ALREADY_GUESSED = "already_guessed"
    GAME_FINISHED = "game_finished"


@dataclass(frozen=True)
class GameOutcome:
    """
    Final result of a completed game.
    """
    status: GameStatus
    word: str

