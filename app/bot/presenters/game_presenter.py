from app.core.game import HangmanGame
from app.core.models import GameOutcome, GameStatus, GuessResult
from app.utils.hangman_visual import render_hangman


def render_game_state(game: HangmanGame) -> str:
    """
    Render the current state of an active game.
    """

    return _render_state(
        game=game,
        word=game.masked_word(),
        show_attempts=True,
    )


def render_guess_result(
    result: GuessResult,
    game: HangmanGame,
    outcome: GameOutcome | None,
) -> str:
    """
    Render the result of a player's guess and the updated game state.
    """

    response = _render_guess_message(result)

    if outcome is not None:
        response += '\n\n'
        response += _render_final_state(
            game=game,
            outcome=outcome,
        )

        return response
    
    response += '\n\n'
    response += render_game_state(game)

    return response


def _render_state(
    game: HangmanGame,
    word: str,
    show_attempts: bool,
) -> str:
    """
    Render the visual state of a game.
    """

    hangman = render_hangman(
        attempts_left=game.attempts_left(),
    )

    response = (
        f"<pre>{hangman}</pre>\n"
        f"<b>Word:</b> {word}\n"
    )

    if show_attempts:
        response += (
            f"<b>Attempts:</b> {game.attempts_left()}\n"
        )

    response += (
        f"<b>Letters:</b> {game.guessed_letters_str()}"
    )

    return response


def _render_final_state(
    game: HangmanGame,
    outcome: GameOutcome,
) -> str:
    """
    Render the final state of a completed game.
    """

    if outcome.status == GameStatus.WON:
        title = " <b>YOU WON!</b>"
        message = " Congratulations!"
    else:
        title = " <b>YOU LOST!</b>"
        message = "Better luck next time!"

    state = _render_state(
        game=game,
        word=f"<b>{outcome.word}</b>",
        show_attempts=True,
    )

    return (
        f"{title}\n\n"
        f"{state}\n\n"
        f"{message}"
    )


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


# def _render_outcome(outcome: GameOutcome) -> str:
#     """
#     Render the final result of a completed game.
#     """
# 
#     if outcome.status == GameStatus.WON:
#         title = " <b>Win!</b>"
#     else:
#         title = " <b>Lost!</b>"
# 
#     return (
#         f"\n\n{title}\n"
#         f"The word was: <b>{outcome.word}</b>"
#     )

