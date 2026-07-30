from .models import GameStatus, GuessResult


class HangmanGame:
    def __init__(self, word: str, max_attempts: int = 6):
        if not word.isalpha():
            raise ValueError("Word must contain only letters")

        self._word: str = word.lower()
        self._guessed_letters: set[str] = set()
        self._attempts_left: int = max_attempts
        self._status: GameStatus = GameStatus.IN_PROGRESS

    # -------------------------
    # Public API
    # -------------------------

    def guess(self, letter: str) -> GuessResult:
        if self._status != GameStatus.IN_PROGRESS:
            return GuessResult.GAME_FINISHED

        letter = self._normalize_input(letter)

        if letter in self._guessed_letters:
            return GuessResult.ALREADY_GUESSED

        self._guessed_letters.add(letter)

        if letter in self._word:
            self._update_win_condition()
            return GuessResult.CORRECT
        else:
            self._attempts_left -= 1
            self._update_loss_condition()
            return GuessResult.INCORRECT

    def word(self) -> str:
        return self._word
        
    def masked_word(self) -> str:
        return " ".join(
                letter if letter in self._guessed_letters else "_"
                for letter in self._word
            )

    def is_finished(self) -> bool:
        return self._status != GameStatus.IN_PROGRESS

    def attempts_left(self) -> int:
        return self._attempts_left

    def status(self) -> GameStatus:
        return self._status

    def guessed_letters(self) -> set[str]:
        return set(self._guessed_letters)

    def guessed_letters_str(self) -> str:
        return ', '.join(sorted(self.guessed_letters())) or '-'

    # -------------------------
    # Internal logic
    # -------------------------

    def _update_win_condition(self) -> None:
        if all(letter in self._guessed_letters for letter in self._word):
            self._status = GameStatus.WON

    def _update_loss_condition(self) -> None:
        if self._attempts_left <= 0:
            self._status = GameStatus.LOST

    def _normalize_input(self, letter: str) -> str:
        letter = letter.lower().strip()

        if len(letter) != 1 or not letter.isalpha():
            raise ValueError("Input must be a single letter")

        return letter

