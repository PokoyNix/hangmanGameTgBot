from app.core.game import HangmanGame
from app.core.models import GameOutcome, GuessResult
from app.utils.word_loader import get_random_word


class GameService:
    def __init__(self):
        self._games: dict[int, HangmanGame] = {}

    def start_game(self, user_id: int) -> HangmanGame:
        word = get_random_word()
        game = HangmanGame(word)
        self._games[user_id] = game
        return game

    def has_active_game(self, user_id: int) -> bool:
        game = self._games.get(user_id)
        return game is not None and not game.is_finished()

    def get_game(self, user_id: int) -> HangmanGame | None:
        return self._games.get(user_id)

    def guess(self, user_id: int, letter: str) -> tuple[GuessResult, GameOutcome | None]:
        game = self._games.get(user_id)

        if game is None:
            raise ValueError("No active game for user")

        result = game.guess(letter)

        if game.is_finished():
            outcome = GameOutcome(
                    status=game.status(),
                    word=game.word()
                )
            del self._games[user_id]
            return result, outcome

        return result, None

