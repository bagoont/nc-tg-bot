"""Trash bin menu handler."""

from typing import cast

from aiogram.types import Message
from aiogram.types import User as TgUser
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_trashbin_msg
from bot.nextcloud import TrashbinService


async def menu(message: Message, i18n: I18nContext, nc: AsyncNextcloud) -> Message:
    """Trash bin menu.

    Trash bin entry point.

    :param message: Message object.
    :param msg_from_user: User who sent the message.
    :param i18n: Internationalization context.
    :param nc: Nextcloud API client.
    """
    msg_from_user = cast(TgUser, message.from_user)
    srv = await TrashbinService.create_instance(nc)

    text, reply_markup = get_trashbin_msg(i18n, srv.trashbin, srv.get_size(), msg_from_user.id)
    return await message.reply(text=text, reply_markup=reply_markup)
