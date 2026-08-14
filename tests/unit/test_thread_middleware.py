from unittest.mock import AsyncMock

import pytest
from aiogram.enums import ChatType
from aiogram.types import Chat, Message

from app.bot.middlewares.thread import ThreadMiddleware


@pytest.fixture
def middleware() -> ThreadMiddleware:
    return ThreadMiddleware()


@pytest.fixture
def handler() -> AsyncMock:
    return AsyncMock()


def create_message(
    chat_type: ChatType,
    chat_id: int = 1,
    message_thread_id: int | None = None,
) -> Message:
    return Message(
        message_id=1,
        date=0,
        chat=Chat(
            id=chat_id,
            type=chat_type,
        ),
        message_thread_id=message_thread_id,
    )


@pytest.mark.asyncio
async def test_private_message_is_allowed(
    middleware: ThreadMiddleware,
    handler: AsyncMock,
) -> None:
    message = create_message(
        chat_type=ChatType.PRIVATE,
    )

    result = await middleware(
        handler,
        message,
        {},
    )

    handler.assert_awaited_once_with(
        message,
        {},
    )

    assert result == handler.return_value


@pytest.mark.asyncio
async def test_allowed_thread_message_is_allowed(
    middleware: ThreadMiddleware,
    handler: AsyncMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "app.bot.middlewares.thread.settings.ALLOWED_THREAD_IDS",
        [42],
    )

    message = create_message(
        chat_type=ChatType.SUPERGROUP,
        message_thread_id=42,
    )

    result = await middleware(
        handler,
        message,
        {},
    )

    handler.assert_awaited_once_with(
        message,
        {},
    )

    assert result == handler.return_value


@pytest.mark.asyncio
async def test_forbidden_thread_message_is_ignored(
    middleware: ThreadMiddleware,
    handler: AsyncMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "app.bot.middlewares.thread.settings.ALLOWED_THREAD_IDS",
        [42],
    )

    message = create_message(
        chat_type=ChatType.SUPERGROUP,
        message_thread_id=99,
    )

    result = await middleware(
        handler,
        message,
        {},
    )

    handler.assert_not_awaited()
    assert result is None


@pytest.mark.asyncio
async def test_message_without_thread_is_ignored(
    middleware: ThreadMiddleware,
    handler: AsyncMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "app.bot.middlewares.thread.settings.ALLOWED_THREAD_IDS",
        [42],
    )

    message = create_message(
        chat_type=ChatType.SUPERGROUP,
        message_thread_id=None,
    )

    result = await middleware(
        handler,
        message,
        {},
    )

    handler.assert_not_awaited()
    assert result is None

