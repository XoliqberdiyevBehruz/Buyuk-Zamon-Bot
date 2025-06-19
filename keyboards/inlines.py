from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


yes_or_no = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Ha", callback_data='ha')
        ],
        [
            InlineKeyboardButton(text="Yoq", callback_data='yoq')
        ]
    ]
)

        