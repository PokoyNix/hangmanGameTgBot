import logging

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from config import settings
from app.services.game_service import GameService
from app.core.models import GuessResult, GameStatus
from app.bot.keyboards import new_game_keyboard
from app.bot.middlewares.thread import ThreadMiddleware

logger = logging.getLogger(__name__)

router = Router()
router.message.middleware(ThreadMiddleware())
router.callback_query.middleware(ThreadMiddleware())

ALLOWED_THREAD_IDS = settings.ALLOWED_THREAD_IDS

# -------------------------
# START GAME
# -------------------------

@router.message(Command('start'))
async def start_handler(message: Message):
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
async def new_game_handler(callback: CallbackQuery, game_service: GameService):
    user_id = callback.from_user.id
    
    try:
        game = game_service.start_game(user_id)
    except ValueError:
        await callback.answer(
            'You already have an active game',
            show_alert=True,
        )

        logger.info(
            'User %s attempted to start a second game.',
            user_id,
        )

        return

    await callback.message.answer(
        f'New game has begun!\n\n'
        f'{game.masked_word()}\n'
        f'Attempts: {game.attempts_left()}'
    )

    await callback.answer()

# -------------------------
# GUESS LETTER
# -------------------------

@router.message()
async def guess_handler(message: Message, game_service: GameService):
    if message.from_user is None:
        return

    user_id = message.from_user.id
    text = message.text

    if not text:
        return

    text = text.strip().lower()

    # validation: one letter
    if len(text) != 1 or not text.isalpha():
        await message.answer('Enter exact one letter')
        logger.debug(
            'User %s sent invalid guess: %r',
            user_id,
            text,
        )

        return

    # validation: is there a game
    if not game_service.has_active_game(user_id):
        await message.answer(
            'Start the game first',
            reply_markup=new_game_keyboard()
        )
        logger.debug(
            'User %s tried guessing without active game.',
        )

        return

    try:
        result, outcome = game_service.guess(user_id, text)
    except ValueError:
        await message.answer('Game error')
        return

    game = game_service.get_game(user_id)

    if game is None and outcome is None:
        logger.error(
            'Game disappeared unexpectedly for user %s.',
            user_id,
        )

        await message.answer(
            'Unexpected error occured.'
        )
        return

    # -------------------------
    # Form answer
    # -------------------------

    if result == GuessResult.CORRECT:
        response = 'There is such letter!'
    elif result == GuessResult.INCORRECT:
        response = 'There is not such letter...'
    elif result == GuessResult.ALREADY_GUESSED:
        response = 'You already have guessed this letter'
    else:
        response = ''

    # if game is end
    if outcome:
        if outcome.status == GameStatus.WON:
            response += f'\n\nWin!'
        else:
            response += f'\n\nLost!'
        
        response += f'\nThe word was: {outcome.word}'
        
        await message.answer(
            response,
            reply_markup=new_game_keyboard()
        )
        return

    # usual state
    response += (
        f'\n\nWord: {game.masked_word()}'
        f'\nAttempts: {game.attempts_left()}'
        f'\nLetters: {game.guessed_letters_str()}'
    )
    await message.answer(response)

