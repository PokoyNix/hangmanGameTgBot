from dataclasses import dataclass

from app.core.game import HangmanGame


@dataclass(slots=True)
class GameSession:
    """
    Represents an active game session.

    Combines the domain game state with the Telegram
    message used to display it.
    """

    game: HangmanGame
    chat_id: int
    message_id: int

