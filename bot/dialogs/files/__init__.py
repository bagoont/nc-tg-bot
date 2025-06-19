"""Files management dialogs.

Provide dialogs for managing files within Nextcloud. The command allow users to create folders, select files, upload
files, and perform other file-related operations.
"""

from aiogram import Router, filters, types
from aiogram_dialog import Dialog, DialogManager, StartMode
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.dialogs.files import handlers, windows
from bot.dialogs.files.states import Files
from bot.filters import AuthFilter
from bot.middlewares import NextcloudMD
from bot.utils import Commands

router: Router = Router(name="files")

router.message.middleware.register(NextcloudMD())
router.callback_query.middleware.register(NextcloudMD())


@router.message(filters.Command(Commands.files.value), AuthFilter())
async def files(
    message: types.Message,
    command: filters.CommandObject,
    nc: AsyncNextcloud,
    dialog_manager: DialogManager,
) -> None:
    """Process the files command to start files dialog.

    Start a scroll group in the chat for managing files.
    If path is provided, it uses that value; otherwise, it start from root.

    :param message: The message containing the file command.
    :param command: The CommandObject with additional parameters.
    :param nc: The AsyncNextcloud instance for interacting with Nextcloud.
    :param dialog_manager: The DialogManager instance managing this dialog context.
    """
    if command.args:
        await dialog_manager.start(Files.SCROLLGROUP, data={"path": command.args}, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.start(Files.SCROLLGROUP, mode=StartMode.RESET_STACK)


multiselect_dialog = Dialog(
    windows.multiselect(),
    windows.multidownload(),
    windows.multidelete(),
    on_start=handlers.on_subdialog_start,
    name="multiselect",
)
create_dialog = Dialog(
    windows.create(),
    windows.create_folder(),
    windows.proccess_documents(),
    windows.upload_documents(),
    on_start=handlers.on_subdialog_start,
    name="create",
)
dialog = Dialog(
    windows.scrollgroup(),
    on_start=handlers.on_start,
    on_process_result=handlers.on_process_result,
    name="files",
)

router.include_router(dialog)
router.include_router(multiselect_dialog)
router.include_router(create_dialog)
