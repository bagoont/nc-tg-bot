"""Handler for moving to the parent directory."""

from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_fsnode_msg
from bot.keyboards.callback_data_factories import FsNodeMenuData
from bot.nextcloud import PrevFsNodeService
from bot.nextcloud.exceptions import FsNodeNotFoundError


async def back(
    query: CallbackQuery,
    query_msg: Message,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> Message | bool:
    """Move to the parent directory.

    :param query: Callback query object.
    :param query_msg: Message object associated with the query.
    :param callback_data: Callback data object containing the necessary data for fsnode.
    :param i18n: I18nContext.
    :param nc: AsyncNextcloud.
    """
    try:
        srv = await PrevFsNodeService.create_instance(nc, file_id=callback_data.file_id)
    except FsNodeNotFoundError:
        return await query_msg.edit_text(text=i18n.get("fsnode-not-found"))

    text, reply_markup = get_fsnode_msg(i18n, srv.fsnode, srv.attached_fsnodes, query.from_user.id)
    with suppress(TelegramBadRequest):
        msg = await query_msg.edit_text(text=text, reply_markup=reply_markup)
    return msg
