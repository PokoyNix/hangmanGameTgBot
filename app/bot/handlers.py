import logging

from aiogram import Router
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


@router.callback_query(lambda c: c.data == 'new_game')
async def new_game_handler(callback: CallbackQuery, game_service: GameService) -> None:
    """
    Start a new game for the user.
    """
    
    if callback.from_user is None:
        return

    user_id = callback.from_user.id
    
    try:
        session = game_service.start_game(
            chat_id=callback.message.chat.id,
            user_id=user_id,
        )
    except ValueError:
        logger.info(
            'User %s attempted to start a new game '
            'while another game is active.',
            user_id,
        )

        await callback.answer(
            'You already have an active game.',
            show_alert=True,
        )

        return

    sent_message = await callback.message.answer(
        render_game_state(session.game),
    )

    game_service.set_message_id(
        chat_id=session.chat_id,
        user_id=user_id,
        message_id=sent_message.message_id,
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

    # validation: is there a game
    if not game_service.has_active_game(user_id):
        logger.debug(
            'User %s tried guessing without active game.',
        )

        await message.answer(
            'Start the game first.',
            reply_markup=new_game_keyboard(),
        )
        return

    try:
        result, outcome = game_service.guess(user_id, text)
    except ValueError:
        await message.answer('An unexpected game error occured.')
        return

    session = game_service.get_session(
        chat_id=message.chat.id,
        user_id=user_id,
    )

    if session is None and outcome is None:
        logger.error(
            'Game disappeared unexpectedly for user %s.',
            user_id,
        )

        await message.answer(
            'An unexpected game error occured.'
        )
        return

    # -------------------------
    # Form answer
    # -------------------------

    response = render_guess_result(
        result=result,
        game=session.game,
        outcome=outcome,
    )

    # if game is end
    if outcome is not None:
        await message.answer(
            response,
            reply_markup=new_game_keyboard()
        )
        return

    await message.answer(response)

