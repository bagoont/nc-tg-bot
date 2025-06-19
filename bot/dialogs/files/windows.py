from typing import Any

from aiogram import F
from aiogram.types import ContentType
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, SwitchTo
from aiogram_dialog.widgets.text import Multi, Progress

from bot.dialogs.files import getters, handlers, keyboards
from bot.dialogs.files.states import Create, Files, Multiselect
from bot.utils import I18NFormat


def _is_selected(data: dict[Any, Any], widget: Whenable, manager: DialogManager) -> bool:
    return bool(manager.current_context().widget_data["multiselect"])


def scrollgroup() -> Window:
    return Window(
        I18NFormat("file-info"),
        keyboards.sg_fsnodes(handlers.on_file, items_key="sub"),
        Button(
            I18NFormat("back-btn"),
            id="back",
            on_click=handlers.on_back,
            when=F["fsnode"].user_path,
        ),
        Button(
            I18NFormat("multiselect-btn"),
            id="multiselect",
            on_click=handlers.on_multiselect,
            when=F["fsnode"].is_dir,
        ),
        Button(
            I18NFormat("download-btn"),
            id="download",
            on_click=handlers.on_download,
            when=~F["fsnode"].is_dir & F["fsnode"].is_readable,
        ),
        Button(
            I18NFormat("delete-btn"),
            id="delete",
            on_click=handlers.on_delete,
            when=F["fsnode"].user_path & F["fsnode"].is_deletable,
        ),
        Button(
            I18NFormat("create-btn"),
            id="create",
            on_click=handlers.on_create,
            when=F["fsnode"].is_dir & F["fsnode"].is_updatable,
        ),
        state=Files.SCROLLGROUP,
        getter=getters.get_fsnodes,
    )


def multiselect() -> Window:
    return Window(
        I18NFormat("multiselect-files"),
        keyboards.ms_sg_fsnodes(items_key="children"),
        Button(
            I18NFormat("multidownload-btn"),
            id="download",
            on_click=handlers.on_multidownload,
            when=_is_selected,
        ),
        Button(
            I18NFormat("multedelete-btn"),
            id="delete",
            on_click=handlers.on_multidelete,
            when=_is_selected,
        ),
        Button(
            I18NFormat("drop-selected-btn"),
            id="drop",
            on_click=handlers.on_multiselect_drop,
            when=_is_selected,
        ),
        Cancel(
            I18NFormat("back-btn"),
        ),
        state=Multiselect.MULTISELECT,
        getter=getters.get_fsnodes,
    )


def multidownload() -> Window:
    return Window(
        Multi(
            I18NFormat("multidownload-files"),
            Progress("progress"),
        ),
        state=Multiselect.MUTLTIDOWNOLOAD,
        getter=getters.get_progress,
    )


def multidelete() -> Window:
    return Window(
        Multi(
            I18NFormat("multidelete-files"),
            Progress("progress"),
        ),
        state=Multiselect.MULTIDELETE,
        getter=getters.get_progress,
    )


def create() -> Window:
    return Window(
        I18NFormat("create-file"),
        SwitchTo(
            I18NFormat("folder-btn"),
            id="folder",
            state=Create.FOLDER,
        ),
        SwitchTo(
            I18NFormat("upload-btn"),
            id="file",
            state=Create.FILES,
        ),
        Cancel(
            I18NFormat("cancel-btn"),
        ),
        state=Create.TYPE,
    )


def create_folder() -> Window:
    return Window(
        I18NFormat("create-folder"),
        MessageInput(
            handlers.folder_name_handler,
            content_types=[ContentType.TEXT],
        ),
        SwitchTo(
            I18NFormat("cancel-btn"),
            id="back",
            state=Create.TYPE,
        ),
        state=Create.FOLDER,
    )


def proccess_documents() -> Window:
    return Window(
        I18NFormat("upload-files-managment"),
        MessageInput(
            handlers.document_handler,
            content_types=[ContentType.DOCUMENT],
        ),
        keyboards.sg_documents(handlers.on_document, items_key="documents"),
        Button(
            I18NFormat("upload-btn"),
            id="upload",
            on_click=handlers.upload_document,
            when=F["documents"],
        ),
        SwitchTo(
            I18NFormat("cancel-btn"),
            id="back",
            state=Create.TYPE,
            on_click=handlers.clear_documents,
        ),
        getter=getters.get_documents,
        state=Create.FILES,
    )


def upload_documents() -> Window:
    return Window(
        Multi(
            I18NFormat("upload-files"),
            Progress("progress"),
        ),
        state=Create.UPLOAD,
        getter=getters.get_progress,
    )
