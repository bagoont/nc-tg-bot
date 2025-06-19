"""Handlers for files dialog."""

import io
import pathlib
import re
from typing import TYPE_CHECKING, Any, cast

from aiogram.types import BufferedInputFile, CallbackQuery, Document, Message
from aiogram_dialog import Data, DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud, FsNode

from bot.core import settings
from bot.dialogs.files.states import Create, Multiselect

if TYPE_CHECKING:
    from aiogram import Bot


def _unique_name(name: str, other: list[str]) -> str:
    """Generate a unique filename by appending an incrementing suffix if it already exists in a list of other names.

    :param name: The base filename to check against duplicate
    :param other: A list of existing filenames to avoid collisions with.
    :return: The modified filename, which is guaranteed to be unique.
    """
    i = 1
    path = pathlib.Path(name)
    while name in other:
        name = f"{path.stem} ({i}){path.suffix}"
        i += 1
    return name


async def _fetch_fsnodes(nc: AsyncNextcloud, path: str | FsNode) -> list[FsNode]:
    """Fetch files from Nextcloud at the given path and returns them as an ordered list.

    :param nc: An instance of AsyncNextcloud providing the Nextcloud interface.
    :param path: The file or directory path to fetch. Can be a string (relative path) or FsNode (absolute path).
    :return: A sorted list of FsNode instances, with directories appearing before other files,
             sorted by whether they are directories (reverse order).
    """
    fsnodes = await nc.files.listdir(path, exclude_self=False)
    return [fsnodes[0], *sorted(fsnodes[1:], key=lambda fsnode: fsnode.is_dir, reverse=True)]


async def on_start(data: dict[str, Any], manager: DialogManager) -> None:
    """Handle the setup phase of the dialog.

    Initialize or retrieve any configured FSNodes for the dialog context during a dialog start.

    :param data: Dialog data.
    :param manager: The DialogManager instance managing this dialog context.
    :raises TypeError: If start data is not a dictionary or does not contain 'fsnodes' key.
    """
    if manager.start_data:
        if not isinstance(manager.start_data, dict):
            msg = "Start data must be a dictionary."
            raise TypeError(msg)
        if "fsnodes" in manager.start_data:
            manager.dialog_data["fsnodes"] = manager.start_data["fsnodes"]
            del manager.start_data["fsnodes"]
            return
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    manager.dialog_data["fsnodes"] = await _fetch_fsnodes(nc, "")


async def on_subdialog_start(data: dict[str, Any], manager: DialogManager) -> None:
    """Handle the setup phase of a sub-dialog.

    Retrieve any configured FSNodes for the current dialog context during a sub-dialog start.

    :param data: Dialog data.
    :param manager: The DialogManager instance managing this dialog context.
    :raises TypeError: If start data is not a dictionary.
    """
    if not isinstance(manager.start_data, dict):
        msg = "Start data must be a dictionary."
        raise TypeError(msg)
    manager.dialog_data["fsnodes"] = manager.start_data.get("fsnodes", [])
    del manager.start_data["fsnodes"]


async def on_process_result(data: Data, result: Data, manager: DialogManager) -> None:
    """Handle process result during sub-dialog completion.

    Update the dialog context with any new FSNodes passed when sub-dialog is complete.

    :param data: Dialog data.
    :param result: The processed result which may contain additional FSNode information if present.
    :param manager: The DialogManager instance managing this dialog context.
    """
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    if isinstance(result, dict):
        manager.dialog_data["fsnodes"] = result.get("fsnodes", await _fetch_fsnodes(nc, ""))


async def on_file(callback: CallbackQuery, widget: Any, manager: DialogManager, item_id: str) -> None:
    """Handle file selection events triggered.

    Update the dialog context with children FSNodes for the selected FSNode.

    :param callback:  The callback event.
    :param widget: The Button instance pressed by user representing one of potentially multiple Select buttons
                   arranged in a Scrollgroup, each corresponding to a unique file ID (item_id).
    :param manager: The DialogManager instance managing this dialog context.
    :param item_id: Unique identifier of the file being selected from Nextcloud.
    """
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    fsnode = await nc.files.by_id(item_id)
    fsnodes = await _fetch_fsnodes(nc, fsnode)
    manager.dialog_data["fsnodes"] = fsnodes


async def on_back(callback: CallbackQuery, widget: Button, manager: DialogManager) -> None:
    """Handle navigation back to parent folder in a dialog.

    Update the dialog context with FSNodes for the parent path.

    :param callback: The callback event.
    :param widget: TODO: Write
    :param manager: The DialogManager instance managing this dialog context.
    """
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    fsnode: FsNode = manager.dialog_data["fsnodes"][0]
    path = str(pathlib.Path(fsnode.user_path).parent)
    parent_fsnodes = await _fetch_fsnodes(nc, path)
    manager.dialog_data["fsnodes"] = parent_fsnodes


async def on_download(callback: CallbackQuery, widget: Button, manager: DialogManager) -> None:
    """Handle file download event.

    Initiating a file download from Nextcloud. It will create an output buffer containing the file stream, write it to
    buffer in chunks, and send it in chunks as a document via the message.

    :param callback: The callback event.
    :param widget: The Button instance  representing the download button pressed by the user.
    :param manager: The DialogManager instance managing this dialog context.
    """
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    fsnode: FsNode = manager.dialog_data["fsnodes"][0]
    if fsnode.info.size > settings.TG_FILESIZE:
        # TODO: To i18n.
        await callback.answer(f"__too_big__: {fsnode.name}")
        return
    buff = io.BytesIO()
    await nc.files.download2stream(fsnode, buff, chunk_size=settings.nc.CHUNKSIZE)
    buff.seek(0)
    file = BufferedInputFile(buff.read(), chunk_size=settings.TG_CHUNK_SIZE, filename=fsnode.name)
    await callback.message.answer_document(file)  # type: ignore[union-attr]


async def on_delete(callback: CallbackQuery, widget: Button, manager: DialogManager) -> None:
    """Handle file delete event.

    Delete a file will remove it from the selected folder. The parent folder's FSNodes will also be updated to reflect
    the deletion, ensuring proper navigation when the dialog is resumed.

    :param callback: The callback event.
    :param widget: The Button instance representing the delete button pressed by the user.
    :param manager: The DialogManager instance managing this dialog context.
    """
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    fsnode: FsNode = manager.dialog_data["fsnodes"][0]
    await nc.files.delete(fsnode)
    path = str(pathlib.Path(fsnode.user_path).parent)
    fsnodes = await _fetch_fsnodes(nc, path)
    manager.dialog_data["fsnodes"] = fsnodes


async def on_multiselect(callback: CallbackQuery, widget: Button, manager: DialogManager) -> None:
    """Handle the multiselect event by starting the multiselect dialog.

    Retrieve the existing FSNodes and starts the multiselect dialog.

    :param callback: The callback event.
    :param widget: The Button instance representing the multiselect button pressed by the user.
    :param manager: The DialogManager instance managing this dialog context.
    """
    fsnodes: list[FsNode] = manager.dialog_data["fsnodes"]
    await manager.start(Multiselect.MULTISELECT, data={"fsnodes": fsnodes}, show_mode=ShowMode.EDIT)


async def on_multiselect_drop(callback: CallbackQuery, widget: Any, manager: DialogManager) -> None:
    """Hanndle drop selected event.

    :param callback: The callback event.
    :param widget: The Button instance representing the drop selected button pressed by the user.
    :param manager: The DialogManager instance managing this dialog context.
    """
    manager.current_context().widget_data["multiselect"] = []


async def on_multidownload(callback: CallbackQuery, widget: Any, manager: DialogManager) -> None:
    """Handle a multifile download scenario where multiple files are selected.

    Manage downloading multiple files based on user selections. It ensure that each file is processed
    individually, handle edge cases like zero-size or too-big files, and update the download progress incrementally.

    :param callback: The callback event.
    :param widget: The Button instance representing the confirmation button to download selected pressed by the user.
    :param manager: The DialogManager instance managing this dialog context.
    """
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    fsnodes: list[FsNode] = manager.dialog_data["fsnodes"]
    selected_ids = cast(list[str], manager.current_context().widget_data["multiselect"])
    await manager.switch_to(Multiselect.MUTLTIDOWNOLOAD, show_mode=ShowMode.EDIT)

    count = len(selected_ids)
    await manager.update({"progress": 0})
    for i, fsnode in enumerate([fsnode for fsnode in fsnodes if fsnode.file_id in selected_ids], start=1):
        if fsnode.info.size > settings.TG_FILESIZE:
            await callback.message.answer(f"__too_big__: {fsnode.name}")  # type: ignore[union-attr]
            continue
        if fsnode.is_dir:
            await callback.message.answer(f"__downloading_dirs_is_not_supported_yet__: {fsnode.name}")  # type: ignore[union-attr]
            continue
        buff = io.BytesIO()
        await nc.files.download2stream(fsnode, buff, chunk_size=settings.nc.CHUNKSIZE)
        buff.seek(0)
        file = BufferedInputFile(buff.read(), chunk_size=settings.TG_CHUNK_SIZE, filename=fsnode.name)
        await callback.message.answer_document(file)  # type: ignore[union-attr]
        await manager.update(
            {
                "name": fsnode.name,
                "progress": i * 100 / count,
            }
        )
    await manager.done(result={"fsnodes": fsnodes}, show_mode=ShowMode.SEND)


async def on_multidelete(callback: CallbackQuery, widget: Any, manager: DialogManager) -> None:
    """Handle a multifile delete scenario where multiple files are selected.

    Manage ddeleting multiple files based on user selections. It deletes each file and update the download progress
    incrementally.

    :param callback: The callback event.
    :param widget: The Button instance representing the confirmation button to delete selected pressed by the user.
    :param manager: The DialogManager instance managing this dialog context.
    """
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    fsnodes: list[FsNode] = manager.dialog_data["fsnodes"]
    selected_ids = cast(list[str], manager.current_context().widget_data["multiselect"])
    await manager.switch_to(Multiselect.MULTIDELETE, show_mode=ShowMode.EDIT)

    count = len(selected_ids)
    await manager.update({"progress": 0})
    for i, fsnode in enumerate([fsnode for fsnode in fsnodes if fsnode.file_id in selected_ids], start=1):
        await nc.files.delete(fsnode)
        await manager.update(
            {
                "name": fsnode.name,
                "progress": i * 100 / count,
            }
        )
    await manager.done(
        result={"fsnodes": await nc.files.listdir(fsnodes[0], exclude_self=False)},
        show_mode=ShowMode.SEND,
    )


async def on_create(callback: CallbackQuery, widget: Button, manager: DialogManager) -> None:
    """Handle creating new file.

    :param callback: The callback event.
    :param widget: The Button instance representing the start create dialog button pressed by the user.
    :param manager: The DialogManager instance managing this dialog context.
    """
    fsnodes = manager.dialog_data["fsnodes"]
    await manager.start(Create.TYPE, show_mode=ShowMode.SEND, data={"fsnodes": fsnodes})


async def folder_name_handler(message: Message, widget: MessageInput, manager: DialogManager) -> None:
    """Handle message with folder name to create the folder.

    Check that the provided folder name conform to a valid format. If invalid, send an error message and exit.
    If valid, proceed to create the folder using the FSNodes and update the dialog data accordingly.

    :param message: The callback event.
    :param widget: The Button instance representing the folder creation button pressed by the user.
    :param manager: The DialogManager instance managing this dialog context.
    """
    i18n: I18nContext = manager.middleware_data["i18n"]
    if not re.match(r"^[a-zA-Z0-9][-a-zA-Z0-9]*[a-zA-Z0-9]?$", text := cast(str, message.text)):
        await message.answer(i18n.get("incorrect-folder-name"))
        return
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    fsnodes: list[FsNode] = manager.dialog_data["fsnodes"]
    name = _unique_name(text, [node.name for node in fsnodes[1:]])
    folder = await nc.files.mkdir(f"{fsnodes[0].user_path}{name}")
    # TODO: To i18n.
    await message.reply(f"__folder_created__: {folder.name}")
    await manager.done(
        result={"fsnodes": await nc.files.listdir(fsnodes[0], exclude_self=False)},
        show_mode=ShowMode.SEND,
    )


async def document_handler(message: Message, widget: MessageInput, manager: DialogManager) -> None:
    """Handle documents for uploading.

    Process incoming message events containing files and validate them before adding them to the dialog data document
    list. Verifies that the document has a non-empty file name, validates that the file size does not exceed the
    configured maximum allowed size.

    :param message: The callback event.
    :param widget: _description_ TODO
    :param manager: The DialogManager instance managing this dialog context.
    """
    document = cast(Document, message.document)
    if document.file_name is None or document.file_size is None:
        # TODO: To i18n.
        await message.reply("__invalid_file__")
        return
    if document.file_size > settings.nc.FILESIZE:
        # TODO: To i18n.
        await message.reply("__file_too_large__")
        return
    if "documents" in manager.dialog_data:
        manager.dialog_data["documents"].insert(0, document)
    else:
        manager.dialog_data["documents"] = [document]


async def on_document(callback: CallbackQuery, widget: Any, manager: DialogManager, item_id: str) -> None:
    """Handle removing document from dialog data document's list to upload.

    :param callback: The callback event.
    :param widget: The Button instance pressed by user representing one of potentially multiple Select buttons
                   arranged in a ScrollGroup, each corresponding to a unique document ID (item_id).
    :param manager: The DialogManager instance managing this dialog context.
    :param item_id: The unique identifier of the document being removed.
    """
    documents: list[Document] = manager.dialog_data["documents"]
    for document in documents:
        if document.file_unique_id == item_id:
            documents.remove(document)


async def clear_documents(callback: CallbackQuery, widget: Button, manager: DialogManager) -> None:
    """Clear list of documents to upload.

    :param callback: The callback event.
    :param widget: The Button instance representing the clear documents button pressed by the user.
    :param manager: The DialogManager instance managing this dialog context.
    """
    if "documents" in manager.dialog_data:
        del manager.dialog_data["documents"]


async def upload_document(callback: CallbackQuery, widget: Button, manager: DialogManager) -> None:
    """Handle confirmation of list of documents to be uploaded and upload them.

    Handle multiple file uploads by downloading each document from Telegram and uploading it to Nextcloud.
    Each file is assigned a unique name based on its source path and the available filesystem nodes (fsnodes)
    and update the upload progress incrementally.

    :param callback: The callback event.
    :param widget: The Button instance representing the confirmation button for uploading documents pressed by the user.
    :param manager: The DialogManager instance managing this dialog context.
    """
    bot: Bot = manager.middleware_data["bot"]
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    fsnodes: list[FsNode] = manager.dialog_data["fsnodes"]
    documents: list[Document] = manager.dialog_data["documents"]
    await manager.switch_to(Create.UPLOAD, show_mode=ShowMode.EDIT)

    count = len(documents)
    for i, document in enumerate(documents, start=1):
        file = await bot.get_file(document.file_id)
        name = cast(str, document.file_name)
        if file.file_path is None:
            await callback.message.reply("__invalid_file__")  # type: ignore[union-attr]
            continue
        buff = await bot.download_file(file.file_path, chunk_size=settings.TG_CHUNK_SIZE)
        name = _unique_name(name, [fsnode.name for fsnode in fsnodes[1:]])
        await nc.files.upload_stream(f"{fsnodes[0].user_path}{name}", buff, chunk_size=settings.nc.CHUNKSIZE)
        await manager.update(
            {
                "name": document.file_name,
                "progress": i * 100 / count,
            }
        )
    await manager.done(
        result={"fsnodes": await nc.files.listdir(fsnodes[0], exclude_self=False)},
        show_mode=ShowMode.SEND,
    )
