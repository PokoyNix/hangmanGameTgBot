from email import message_from_binary_file

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.services.game_service import GameService
from app.core.models import GuessResult

router = Router()

# -------------------------
# START GAME
# -------------------------

@router.message(Command('start'))
async def start_handler(message: Message, game_service: GameService):
    user_id = message.from_user.id

    game = game_service.start_game(user_id)

    await message.answer(
            f'Game has begun!\n\n'
            f'{game.masked_word()}\n'
            f'Attempts: {game.attempts_left()}'
        )

# -------------------------
# GUESS LETTER
# -------------------------

@router.message()
async def guess_handler(message: Message, game_service: GameService):
    user_id = message.from_user.id
    text = message.text.strip().lower()

    # validation: one letter
    if len(text) != 1 or not text.isalpha():
        await message.answer('Enter exact one letter')
        return

    # validation: is there a game
    if not game_service.has_active_game(user_id):
        await message.answer('Start the game first: /start')
        return

    try:
        result = game_service.guess(user_id, text)
    except ValueError:
        await message.answer('Game error')
        return

    game = game_service.get_game(user_id)

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
    if game is None:
        # game has already been removed from service
        response += '\n\nGame has been ended'
        await message.answer(response)
        return

    # usual state
    response += (
            f'\n\nWord: {game.masked_word()}'
            f'\nAttempts: {game.attempts_left()}'
            f'\nLetters: {game.guessed_letters_str()}'
        )
    await message.answer(response)

