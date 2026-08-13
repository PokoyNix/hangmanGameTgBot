import pytest

from unittest.mock import patch

from app.core.models import GameStatus, GuessResult
from app.services.game_service import GameService


def test_start_game_creates_active_session() -> None:
    service = GameService()

    session = service.start_game(
        chat_id=1,
        user_id=100,
    )

    assert session.chat_id == 1
    assert session.message_id == 0
    assert service.has_active_game(
        chat_id=1,
        user_id=100,
    )


def test_get_session_returns_active_session() -> None:
    service = GameService()

    created_session = service.start_game(
        chat_id=1,
        user_id=100,
    )

    session = service.get_session(
        chat_id=1,
        user_id=100,
    )

    assert session is created_session


def test_user_cannot_start_second_game_in_same_chat() -> None:
    service = GameService()

    service.start_game(
        chat_id=1,
        user_id=100,
    )
    
    with pytest.raises(ValueError, match="already has active game"):
        service.start_game(
            chat_id=1,
            user_id=100,
        )


def test_different_users_can_have_games_in_same_chat() -> None:
    service = GameService()

    first_session = service.start_game(
        chat_id=1,
        user_id=100,
    )

    second_session = service.start_game(
        chat_id=1,
        user_id=200,
    )

    assert first_session is not second_session

    assert service.has_active_game(
        chat_id=1,
        user_id=100,
    )

    assert service.has_active_game(
        chat_id=1,
        user_id=200,
    )


def test_same_user_can_have_games_in_different_chats() -> None:
    service = GameService()

    first_session = service.start_game(
        chat_id=1,
        user_id=100,
    )

    second_session = service.start_game(
        chat_id=2,
        user_id=100,
    )

    assert first_session is not second_session

    assert service.has_active_game(
        chat_id=1,
        user_id=100,
    )

    assert service.has_active_game(
        chat_id=2,
        user_id=100,
    )


def test_remove_game_deletes_session() -> None:
    service = GameService()

    service.start_game(
        chat_id=1,
        user_id=100,
    )
    
    service.remove_game(
        chat_id=1,
        user_id=100,
    )

    assert service.get_session(
        chat_id=1,
        user_id=100,
    ) is None

    assert not service.has_active_game(
        chat_id=1,
        user_id=100,
    )


def test_remove_nonexistent_game_does_not_raise() -> None:
    service = GameService()

    service.remove_game(
        chat_id=1,
        user_id=100,
    )


def test_set_message_id_updates_session() -> None:
    service = GameService()

    service.start_game(
        chat_id=1,
        user_id=100,
    )

    service.set_message_id(
        chat_id=1,
        user_id=100,
        message_id=500,
    )

    session = service.get_session(
        chat_id=1,
        user_id=100,
    )

    assert session is not None
    assert session.message_id == 500


def test_set_message_id_without_active_game_raises() -> None:
    service = GameService()

    with pytest.raises(ValueError, match="No active game"):
        service.set_message_id(
            chat_id=1,
            user_id=100,
            message_id=500,
        )


def test_guess_returns_correct_result() -> None:
    service = GameService()

    with patch(
        "app.services.game_service.get_random_word",
        return_value="python",
    ):
        service.start_game(
            chat_id=1,
            user_id=100,
        )

    result, outcome = service.guess(
        chat_id=1,
        user_id=100,
        letter="p",
    )

    assert result == GuessResult.CORRECT
    assert outcome is None


def test_guess_returns_outcome_when_game_is_won() -> None:
    service = GameService()

    with patch(
        "app.services.game_service.get_random_word",
        return_value="a",
    ):
        service.start_game(
            chat_id=1,
            user_id=100,
        )

    result, outcome = service.guess(
        chat_id=1,
        user_id=100,
        letter="a",
    )

    assert result == GuessResult.CORRECT

    assert outcome is not None
    assert outcome.status == GameStatus.WON
    assert outcome.word == "a"


def test_guess_returns_outcome_when_game_is_lost() -> None:
    service = GameService()

    with patch(
        "app.services.game_service.get_random_word",
        return_value="z",
    ):
        service.start_game(
            chat_id=1,
            user_id=100,
        )

    for letter in ("a", "b", "c", "d", "e"):
        result, outcome = service.guess(
            chat_id=1,
            user_id=100,
            letter=letter,
        )

        assert result == GuessResult.INCORRECT
        assert outcome is None

    result, outcome = service.guess(
        chat_id=1,
        user_id=100,
        letter="f",
    )

    assert result == GuessResult.INCORRECT
    assert outcome is not None
    assert outcome.status == GameStatus.LOST
    assert outcome.word == "z"


def test_finished_game_is_removed_from_service() -> None:
    service = GameService()

    with patch(
        "app.services.game_service.get_random_word",
        return_value="a",
    ):
        service.start_game(
            chat_id=1,
            user_id=100,
        )

    result, outcome = service.guess(
        chat_id=1,
        user_id=100,
        letter="a",
    )

    assert result == GuessResult.CORRECT
    assert outcome is not None
    assert outcome.status == GameStatus.WON

    assert service.get_session(
        chat_id=1,
        user_id=100,
    ) is None

    assert not service.has_active_game(
        chat_id=1,
        user_id=100,
    )

