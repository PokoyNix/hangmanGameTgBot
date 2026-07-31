import logging

from app.core.game import HangmanGame
from app.core.models import GameOutcome, GuessResult
from app.utils.word_loader import get_random_word

logger = logging.getLogger(__name__)


class GameService:
    """
    Application service responsible for managing user games.
    """

    def __init__(self) -> None:
        self._games: dict[int, HangmanGame] = {}

    def start_game(self, user_id: int) -> HangmanGame:
        """
        Start a new game for user.
        """

        if self.has_active_game(user_id):
            logger.info(
                'User %s attempted to start a new game while another game is active.',
                user_id,
            )
            raise ValueError('User already has active game')

        word = get_random_word()
        game = HangmanGame(word)
        self._games[user_id] = game
        logger.info(
                'Started new game for user %s.',
                user_id,
        )

        return game

    def has_active_game(self, user_id: int) -> bool:
        """
        Check whether user has active game.
        """

        game = self._games.get(user_id)
        return game is not None and not game.is_finished()

    def get_game(self, user_id: int) -> HangmanGame | None:
        """
        Return user's current game.
        """
        return self._games.get(user_id)

    def remove_game(self, user_id: int) -> None:
        """
        Remove user's game if it exists.
        """
        self._games.pop(user_id, None)

    def guess(self, user_id: int, letter: str) -> tuple[GuessResult, GameOutcome | None]:
        """
        Process user's guess.
        """

        game = self._games.get(user_id)

        if game is None:
            raise ValueError("No active game for user")

        result = game.guess(letter)
        logger.info(
            'User %s guessed `%s`. Result: %s.',
            user_id,
            letter,
            result.value,
        )

        if game.is_finished():
            outcome = GameOutcome(
                status=game.status(),
                word=game.reveal_word()
            )

            logger.info(
                'Game is finished for user %s with status %s',
                user_id,
                outcome.status.value,
            )
            self.remove_game(user_id)
            return result, outcome

        return result, None

