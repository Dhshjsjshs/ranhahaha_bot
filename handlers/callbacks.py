import logging
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from db import async_session_maker


# Callback_query_handler - это функция, которая позволяет обрабатывать коллбек-запросы от пользователей.
# Коллбэк-запрос - это запрос, который отправляется боту, когда пользователь нажимает кнопку в его чате.
# Обработчик для callback с F.data для aiogram3
# https://ru.stackoverflow.com/questions/1565436/%D0%9A%D0%B0%D0%BA-%D1%81%D0%B4%D0%B5%D0%BB%D0%B0%D1%82%D1%8C-%D0%BE%D0%B1%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA-%D0%BA%D0%BE%D0%BB%D0%B1%D0%B5%D0%BA%D0%BE%D0%B2-%D0%B2-aiogram-3


async def callback_continue(callback: CallbackQuery):
    """продолжить"""

    async with async_session_maker() as session:
        session: AsyncSession
        # что-то происходит
        await session.commit()

    await callback.message.answer("Выберите роль. К примеру: 'Учитель' или 'Слушатель'. Напишите в чат")
    logging.info(f"user {callback.from_user.id} pressed continue button")
