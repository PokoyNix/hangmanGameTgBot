import pytest

from app.core.game import HangmanGame
from app.core.models import GameStatus, GuessResult


def test_game_starts_in_progress() -> None:
    game = HangmanGame("python")

    assert game.status() == GameStatus.IN_PROGRESS
    assert game.attempts_left() == 6
    assert game.guessed_letters() == set()


def test_correct_guess() -> None:
    game = HangmanGame("python")

    result = game.guess("p")

    assert result == GuessResult.CORRECT
    assert game.guessed_letters() == {"p"}
    assert game.attempts_left() == 6


def test_incorrect_guess_reduces_attempts() -> None:
    game = HangmanGame("python")

    result = game.guess("z")

    assert result == GuessResult.INCORRECT
    assert game.attempts_left() == 5


def test_repeated_guess_does_not_reduce_attempts() -> None:
    game = HangmanGame("python")

    game.guess("z")
    result = game.guess("z")

    assert result == GuessResult.ALREADY_GUESSED
    assert game.attempts_left() == 5


def test_game_is_won_when_all_letters_are_guessed() -> None:
    game = HangmanGame("cat")

    game.guess("c")
    game.guess("a")
    result = game.guess("t")

    assert result == GuessResult.CORRECT
    assert game.status() == GameStatus.WON
    assert game.is_finished()


def test_game_is_lost_when_attempts_run_out() -> None:
    game = HangmanGame("cat")

    for letter in "xyzuvw":
        game.guess(letter)

    assert game.attempts_left() == 0
    assert game.status() == GameStatus.LOST
    assert game.is_finished()


@pytest.mark.parametrize(
    "letter",
    ["", "ab", "1", "!"],
)
def test_invalid_guess_raises_error(letter: str) -> None:
    game = HangmanGame("python")

    with pytest.raises(ValueError):
        game.guess(letter)


def test_guess_after_game_is_finished() -> None:
    game = HangmanGame("cat")

    game.guess("c")
    game.guess("a")
    game.guess("t")

    result = game.guess("x")

    assert result == GuessResult.GAME_FINISHED

