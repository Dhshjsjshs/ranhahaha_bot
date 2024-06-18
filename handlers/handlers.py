__all__ = [
    "register_message_handler",
]

import logging

from aiogram import Router, F
from aiogram import types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from db import async_session_maker, User
from .callbacks import callback_continue

# настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# help_command
help_str = """
Вас приветствует бот <b><i>ИМЯ БОТА</i></b>\n
💬 Вы можете вывести справочную информацию, отправив команду <b>/help</b>\n
💬 Информацию о пользователе можно вывести с помощью команды <b>/status</b>
"""


async def help_command(message: types.Message):
    """справочная команда, регистрация пользователя"""

    async with async_session_maker() as session:
        session: AsyncSession
        query = select(User).where(User.user_id == message.from_user.id)
        user_exit = await session.execute(query)

        if user_exit.scalars().all():
            await message.reply(text=help_str, parse_mode="HTML")
            logging.info(f"user {message.from_user.id} asks for help")

        else:
            new_user = {
                "user_id": message.from_user.id,
                "username": message.from_user.username
            }
            stmt = insert(User).values(**new_user)
            await session.execute(stmt)
            await session.commit()
            await message.reply(help_str)
            logging.info(f"register new user: {message.from_user.id}")


async def status_command(message: types.Message):
    """Информация о пользователе"""

    async with async_session_maker() as session:
        session: AsyncSession
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)
        user = result.scalar()
        await message.reply(text=f"<b>User ID</b>: <i>{user.user_id}</i>\n"
                                 f"<b>User name</b>: <i>{user.username}</i>",
                            parse_mode="HTML")
        logging.info(f"user {message.from_user.id} is asking for status")


async def register_command(message: types.Message):
    text = f"Перейдите по ссылке () и авторизуйтесь. Далее сохраните свой токен (/token токен) "

    logging.info(f"{message.from_user.id} - register_command")
    await message.reply(text)


async def token_command(message: types.Message):
    async with async_session_maker() as session:
        session: AsyncSession

    logging.info(f"{message.from_user.id} - token_command")


async def add_command(message: types.Message):
    async with async_session_maker() as session:
        session: AsyncSession

    logging.info(f"{message.from_user.id} - add_command")


async def delete_command(message: types.Message):
    async with async_session_maker() as session:
        session: AsyncSession

    logging.info(f"{message.from_user.id} - delete_command")


class Form(StatesGroup):
    waiting_for_text = State()


async def callback_continue(callback: CallbackQuery, state: FSMContext):
    """продолжить"""
    async with async_session_maker() as session:
        session: AsyncSession
        # что-то происходит
        await session.commit()

    await callback.message.answer("Введите текст:")
    await Form.waiting_for_text.set()
    await state.update_data(callback=callback)

    logging.info(f"user {callback.from_user.id} pressed continue button")


# Обработчик ответа пользователя
async def process_text(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    callback = user_data.get('callback')

    # Здесь можно использовать текст, введенный пользователем
    user_text = message.text
    logging.info(f"user {callback.from_user.id} entered text: {user_text}")

    await message.answer("Успешно!")

    # Завершение состояния
    await state.finish()


def register_message_handler(router: Router):
    """Маршрутизация"""
    router.message.register(help_command, Command(commands=["start", "help"]))
    router.message.register(status_command, Command(commands=["status"]))
    router.message.register(delete_command, Command(commands=["delete"]))
    router.message.register(add_command, Command(commands=["add"]))
    router.message.register(token_command, Command(commands=["token"]))
    router.message.register(register_command, Command(commands=["register"]))
    router.callback_query.register(callback_continue, F.data.startswith("continue_"))
