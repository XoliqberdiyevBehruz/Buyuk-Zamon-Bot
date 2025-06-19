from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


phone_number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Phone Number", request_contact=True)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

yes_or_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Yes"),
            KeyboardButton(text="No")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)