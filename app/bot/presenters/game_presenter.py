from app.core.game import HangmanGame
from app.core.models import GameOutcome, GameStatus, GuessResult
from app.utils.hangman_visual import render_hangman


def render_game_state(game: HangmanGame) -> str:
    """
    Render the current state of an active game.
    """

    hangman = render_hangman(
        attempts_left=game.attempts_left(),
    )

    return (
        f"<pre>{hangman}</pre>\n"
        f"<b>Word:</b> {game.masked_word()}\n"
        f"<b>Attempts:</b> {game.attempts_left()}\n"
        f"<b>Letters:</b> {game.guessed_letters_str()}"
    )


def render_guess_result(
    result: GuessResult,
    game: HangmanGame | None,
    outcome: GameOutcome | None,
) -> str:
    """
    Render the result of a player's guess.
    """

    response = _render_guess_message(result)

    if outcome is not None:
        response += _render_outcome(outcome)
        return response

    if game is not None:
        response += f"\n\n{render_game(game)}"

    return response


def _render_guess_message(result: GuessResult) -> str:
    """
    Render feedback for a single guess.
    """

    messages = {
        GuessResult.CORRECT: "There is such letter!",
        GuessResult.INCORRECT: "There is not such letter...",
        GuessResult.ALREADY_GUESSED: (
            "You already have guessed this letter."
        ),
        GuessResult.GAME_FINISHED: "The game has already finished.",
    }

    return messages[result]


def _render_outcome(outcome: GameOutcome) -> str:
    """
    Render the final result of a completed game.
    """

    if outcome.status == GameStatus.WON:
        title = " <b>Win!</b>"
    else:
        title = " <b>Lost!</b>"

    return (
        f"\n\n{title}\n"
        f"The word was: <b>{outcome.word}</b>"
    )

