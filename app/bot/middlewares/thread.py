from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.types import CallbackQuery, Message, TelegramObject

from config import settings

logger = logging.getLogger(__name__)


class ThreadMiddleware(BaseMiddleware):
    """
    Allow bot interactions only in:

    - private chats
    - configured forum topics.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if isinstance(event, Message):
            if not self._is_allowed(
                event.chat.type,
                event.message_thread_id,
            ):
                logger.debug('Ignoring message %s from chat %s: thread %s is not allowed.',
                             event.message_id,
                             event.chat.id,
                             event.message_thread_id,)
                return None
        
        elif isinstance(event, CallbackQuery):
            message = event.message

            if message is None:
                return None

            if not self._is_allowed(
                message.chat.type,
                message.message_thread_id,
            ):
                logger.debug('Ignoring callback from chat %s: thread %s is not allowed.',
                             message.chat.id,
                             message.message_thread_id,)
                return None

        return await handler(event, data)

    @staticmethod
    def _is_allowed(
        chat_type: str,
        thread_id: int | None,
    ) -> bool:
        if chat_type == ChatType.PRIVATE:
            return True

        return thread_id in settings.ALLOWED_THREAD_IDS

