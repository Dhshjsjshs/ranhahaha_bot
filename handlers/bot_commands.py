__all__ = [
    "commands_for_bot",
]

from aiogram import types

bot_commands = (
    ("start", "Регистрация"),
    ("help", "Справка"),
    ("status", "Cтатус"),
    ("register", "Инструкция"),
    ("token", "Токен - Только для учителя"),
    ("add", "+ Папка - Только для учителя"),
    ("delete", "- Папка - Только для учителя")
)

commands_for_bot = []
for cmd in bot_commands:
    commands_for_bot.append(types.BotCommand(command=cmd[0], description=cmd[1]))
