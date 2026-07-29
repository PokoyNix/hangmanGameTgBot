from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.services.game_service import GameService

router = Router()


@router.message(Command('start'))
async def start_handler(message: Message):
    await message.answer('Welcome to Hangman Game!')


@router.message()
async def guess_handler(message: Message):
    await message.answer('Letter processing...')

