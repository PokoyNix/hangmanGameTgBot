from app.core.game import HangmanGame
from app.core.models import GuessResult


class GameService:
    def __init__(self):
        self._games: dict[int, HangmanGame] = {}

    def start_game(self, user_id: int, word: str) -> HangmanGame:
        game = HangmanGame(word)
        self._games[user_id] = game
        return game

    def has_active_game(self, user_id: int) -> bool:
        game = self._games.get(user_id)
        return game is not None and not game.is_finished()

    def get_game(self, user_id: int) -> HangmanGame | None:
        return self._games.get(user_id)

    def guess(self, user_id: int, letter: str) -> GuessResult:
        game = self._games.get(user_id)

        if game is None:
            raise ValueError("No active game for user")

        result = game.guess(letter)

        if game.is_finished():
            del self._games[user_id]

        return result

