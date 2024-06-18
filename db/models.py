# __all__ - публичный список объектов
# https://ru.stackoverflow.com/questions/27983/%D0%A7%D1%82%D0%BE-%D1%82%D0%B0%D0%BA%D0%BE%D0%B5-all-%D0%B2-python

__all__ = [
    'User',
    'Base',
]

import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DATE


# Декларативная модель базы данных
# https://metanit.com/python/database/3.2.php
class Base(DeclarativeBase):
    pass


class User(Base):
    """модель пользователя tg для регистрации"""

    __tablename__ = "user_table"

    user_id = Column(Integer, nullable=False, unique=True, primary_key=True)

    username = Column(String, unique=False, nullable=True)  # Вместо String можно использовать VARCHAR()

    reg_date = Column(DATE, default=datetime.datetime.now())

    teacher = Column(String, unique=False, nullable=True)
