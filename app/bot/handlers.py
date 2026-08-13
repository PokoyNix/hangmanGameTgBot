import logging

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from app.services.game_service import GameService
from app.bot.keyboards import new_game_keyboard
from app.bot.middlewares.thread import ThreadMiddleware
from app.bot.presenters.game_presenter import (
    render_game_state,
    render_guess_result,
)

logger = logging.getLogger(__name__)

router = Router()
router.message.middleware(ThreadMiddleware())
router.callback_query.middleware(ThreadMiddleware())

# -------------------------
# START GAME
# -------------------------

@router.message(Command('start'))
async def start_handler(message: Message) -> None:
    """
    Handle the /start command.
    """

    if message.from_user is None:
        return

    logger.info(
        'User %s opened the bot.',
        message.from_user.id,
    )

    await message.answer(
        f'Welcome to Hangman Game!\n\n' \
        f'Press button to start the game',
        reply_markup=new_game_keyboard()
    )

# -------------------------
# NEW GAME
# -------------------------

@router.callback_query(lambda c: c.data == 'new_game')
async def new_game_handler(callback: CallbackQuery, game_service: GameService) -> None:
    """
    Start a new game for the user.
    """
    
    if callback.from_user is None:
        return

    if callback.message is None:
        await callback.answer()
        return

    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    
    try:
        session = game_service.start_game(
            chat_id=chat_id,
            user_id=user_id,
        )
    except ValueError:
        logger.info(
            'User %s attempted to start a new game '
            'in chat %s while another game is active.',
            user_id,
            chat_id,
        )

        await callback.answer(
            'You already have an active game.',
            show_alert=True,
        )

        return

    game_message = await callback.message.answer(
        render_game_state(session.game),
    )

    game_service.set_message_id(
        chat_id=chat_id,
        user_id=user_id,
        message_id=game_message.message_id,
    )

    logger.info(
        'Game message %s created for user %s in chat %s.',
        game_message.message_id,
        user_id,
        chat_id,
    )

    await callback.answer()

# -------------------------
# GUESS LETTER
# -------------------------

@router.message()
async def guess_handler(message: Message, game_service: GameService) -> None:
    """
    Handle a player's letter guess.
    """

    if message.from_user is None:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text

    if not text:
        return

    text = text.strip().lower()

    # validation: one letter
    if len(text) != 1 or not text.isalpha():
        logger.debug(
            'User %s sent invalid guess: %r',
            user_id,
            text,
        )
        await message.answer(
            'Enter exactly one letter.'
        )
        return

    session = game_service.get_session(
        chat_id=chat_id,
        user_id=user_id,
    )

    # validation: is there a game
    if session is None or session.game.is_finished():
        logger.debug(
            'User %s attempted to guess without an active game '
            'in chat %s.',
            user_id,
            chat_id,
        )

        await message.answer(
            'Start the game first.',
            reply_markup=new_game_keyboard(),
        )
        return

    try:
        result, outcome = game_service.guess(
            chat_id=chat_id,
            user_id=user_id,
            letter=text,
        )
    except ValueError:
        logger.exception(
            'Failed to process guess for user %s in chat %s.',
            user_id,
            chat_id,
        )
        await message.answer('An unexpected game error occured.')
        return

    response = render_guess_result(
        result=result,
        game=session.game,
        outcome=outcome,
    )

    # Remove the user's guess message.
    try:
        await message.delete()
    except TelegramBadRequest:
        logger.exception(
            'Telegram rejected deletion of message %s '
            'from user %s in chat %s.',
            message.message_id,
            user_id,
            chat_id,
        )
    except TelegramForbiddenError:
        logger.exception(
            'Bot has no permission to delete message %s '
            'from user %s in chat %s.',
            message.message_id,
            user_id,
            chat_id,
        )

    # Update the existing game message.
    try:
        await message.bot.edit_message_text(
            chat_id=session.chat_id,
            message_id=session.message_id,
            text=response,
            reply_markup=(
                new_game_keyboard()
                if outcome is not None
                else None
            ),
        )
    except TelegramBadRequest:
        logger.exception(
            'Failed to update game message %s '
            'for user %s in chat %s.',
            session.message_id,
            user_id,
            chat_id,
        )

        await message.answer('An unexpected error occured while updating the game.')
        return

