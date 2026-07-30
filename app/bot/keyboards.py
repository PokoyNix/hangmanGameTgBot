from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def new_game_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="New game",
                        callback_data="new_game",
                    )
                ]
            ]
        )

