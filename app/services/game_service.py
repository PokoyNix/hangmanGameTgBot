import logging

from app.core.game import HangmanGame
from app.core.models import GameOutcome, GuessResult
from app.services.models import GameSession
from app.utils.word_loader import get_random_word

logger = logging.getLogger(__name__)

GameKey = tuple[int, int]


class GameService:
    """
    Application service responsible for managing active game sessions.
    """

    def __init__(self) -> None:
        self._games: dict[GameKey, GameSession] = {}

    @staticmethod
    def _make_key(chat_id: int, user_id: int) -> GameKey:
        return chat_id, user_id

    def start_game(self, chat_id: int, user_id: int) -> GameSession:
        """
        Start a new game for a user in a chat.

        Raises:
            ValueError: if the user already has an active game
                in the specified chat.
        """

        key = self._make_key(chat_id, user_id)

        if self.has_active_game(chat_id, user_id):
            logger.info(
                'User %s attempted to start a new game'
                'in chat %s while another game is active.',
                user_id,
                chat_id,
            )
            raise ValueError('User already has active game')

        word = get_random_word()
        game = HangmanGame(word)

        session = GameSession(
            game=game,
            chat_id=chat_id,
            message_id=0,
        )

        self._games[key] = session
        logger.info(
            'Started new game for user %s in chat %s.',
            user_id,
            chat_id,
        )

        return session

    def has_active_game(self, chat_id: int, user_id: int) -> bool:
        """
        Check whether user has an active game in the chat.
        """

        session = self._games.get(
            self._make_key(chat_id, user_id)
        )

        return session is not None and not session.game.is_finished()

    def get_session(self, chat_id: int, user_id: int) -> GameSession | None:
        """
        Return the user's active game session.
        """
        return self._games.get(
            self._make_key(chat_id, user_id)
        )

    def set_message_id(self, chat_id: int, user_id: int, message_id: int) -> None:
        """
        Store the Telegram message ID associated with a game.
        """

        session = self.get_session(chat_id, user_id)

        if session is None:
            raise ValueError("No active game")

        session.message_id = message_id

    def remove_game(self, chat_id: int, user_id: int) -> None:
        """
        Remove user's game session if it exists.
        """
        self._games.pop(
            self._make_key(chat_id, user_id),
            None,
        )

    def guess(self, chat_id: int, user_id: int, letter: str) -> tuple[GuessResult, GameOutcome | None]:
        """
        Process user's guess.

        Returns:
            Guess result and final outcome if the game ended.
        """

        session = self.get_session(chat_id, user_id)

        if session is None:
            raise ValueError("No active game for user")

        result = session.game.guess(letter)
        logger.info(
            'User %s guessed `%s` in chat %s. Result: %s.',
            user_id,
            letter,
            chat_id,
            result.value,
        )

        if session.game.is_finished():
            outcome = GameOutcome(
                status=session.game.status(),
                word=session.game.reveal_word()
            )

            logger.info(
                'Game is finished for user %s in chat %s with status %s',
                user_id,
                chat_id,
                outcome.status.value,
            )
            
            return result, outcome

        return result, None

