from aiogram.types import User
from aiogram_i18n.managers import BaseManager

from bot.core import settings
from bot.db import UserRepository


class LocaleManager(BaseManager):
    async def set_locale(self, locale: str, event_from_user: User, users: UserRepository) -> None:
        user = await users.get_by_tg_id(event_from_user.id)
        if user is None:
            msg = "User not found."
            raise ValueError(msg)
        user.language = locale
        await users.session.commit()

    async def get_locale(self, event_from_user: User, users: UserRepository) -> str:
        user = await users.get_by_tg_id(event_from_user.id)
        if user is None:
            if event_from_user.language_code in settings.AVALIABLE_LANGUAGES:
                return event_from_user.language_code
            return settings.DEFAULT_LANGUAGE
        return user.language
