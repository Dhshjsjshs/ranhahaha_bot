__all__ = [
    "register_message_handler",
]


import logging

from aiogram import Router, F
from aiogram import types
from aiogram.filters.command import Command
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from db import async_session_maker, User, DiskClass
from .callbacks import callback_continue
from .keyboards import keyboard_continue

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
            await message.reply("Регистрация как:", reply_markup=keyboard_continue)
            logging.info(f"register new user: {message.from_user.id}")


async def status_command(message: types.Message):
    """Информация о пользователе"""

    async with async_session_maker() as session:
        session: AsyncSession
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)
        user = result.scalar()
        if not user:
            await message.reply("Зарегистрируйтесь /start")
            return

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
        text_array = message.text.split()
        user = await session.get(User, message.from_user.id)
        #если у юзера есть ссылка на учителя значит он слушатель

        if user.teacher:
            await message.reply(f"Доступно только учителям")
        elif len(text_array) == 1:
            if user.token:
                await message.reply(f"Ваш токен = {user.token}")
            else:
                await message.reply(f"Введите /token ваш токен")
        else:
            token = text_array[1].strip()
            disk = DiskClass(token=token)

            if disk.disk_check_token():
                user.token = token
                await message.reply(f"Токен успешно сохранен")
            else:
                await message.reply(f"Ошибка")

    logging.info(f"{message.from_user.id} - token_command")



async def add_command(message: types.Message):
    async with async_session_maker() as session:
        session: AsyncSession

    logging.info(f"{message.from_user.id} - add_command")


async def delete_command(message: types.Message):
    async with async_session_maker() as session:
        session: AsyncSession

    logging.info(f"{message.from_user.id} - delete_command")


async def listen_user_text(message: types.Message):
    teacherid = message.text.split("/")[1]

    async with async_session_maker() as session:
        session: AsyncSession

        teacher = await session.get(User, teacherid)

        # если препод найден
        if teacher:
            currentuser = await session.get(User, message.from_user.id)

            # обновление учителя
            if currentuser:
                currentuser.teacher = teacherid

                await message.answer(f"Вы подписались на @{teacher.username}")
            else:
                # новый юзер
                new_user = User(id=message.from_user.id, teacher=teacherid, username=message.from_user.username)
                session.add(new_user)

                await message.answer(f"Вы приглашены как слушатель к @{teacher.username}")

        else:
            # если нет
            await message.answer("Неправильная ссылка")

        await session.commit()
        await session.close()


def register_message_handler(router: Router):
    """Маршрутизация"""
    router.message.register(help_command, Command(commands=["start", "help"]))
    router.message.register(status_command, Command(commands=["status"]))
    router.message.register(delete_command, Command(commands=["delete"]))
    router.message.register(add_command, Command(commands=["add"]))
    router.message.register(token_command, Command(commands=["token"]))
    router.message.register(register_command, Command(commands=["register"]))
    router.callback_query.register(callback_continue, F.data.startswith("continue_"))
    router.message.register(listen_user_text)
