from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

continue_button1 = InlineKeyboardButton(
    text="Учитель",
    callback_data="continue_teacher",
)

continue_button2 = InlineKeyboardButton(
    text="Ученик",
    callback_data="continue_user",
)

keyboard_continue = InlineKeyboardMarkup(inline_keyboard=[[continue_button1, continue_button2]])
