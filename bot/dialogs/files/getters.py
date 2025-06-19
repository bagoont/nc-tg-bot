from dataclasses import dataclass
from typing import Any

import humanize
from aiogram.types import Document
from aiogram_dialog import DialogManager
from nc_py_api import FsNode

from bot.utils import MIME_SYMBOLS


async def get_fsnodes(dialog_manager: DialogManager, **kwargs: Any) -> dict[str, Any]:
    fsnodes: list[FsNode] = dialog_manager.dialog_data["fsnodes"]

    return {
        "text": {
            "name": fsnodes[0].name,
            "path": fsnodes[0].user_path,
            "symbol": "📁" if fsnodes[0].is_dir else MIME_SYMBOLS.get(fsnodes[0].info.mimetype, ""),
            "type": "folder" if fsnodes[0].is_dir else fsnodes[0].info.mimetype,
            "favorite": str(fsnodes[0].info.favorite),
            "size": humanize.naturalsize(fsnodes[0].info.size),
            "last_modified": fsnodes[0].info.last_modified,
            "permissions": fsnodes[0].info.permissions,
            "user": fsnodes[0].user,
        },
        "fsnode": fsnodes[0],
        "sub": tuple(
            ("📁" if fsnode.is_dir else MIME_SYMBOLS.get(fsnode.info.mimetype, ""), fsnode)
            for fsnode in fsnodes[1:]
            if fsnode.is_readable
        ),
    }


async def get_documents(dialog_manager: DialogManager, **kwargs: Any) -> dict[str, Any]:
    return {"documents": dialog_manager.dialog_data.get("documents", [])}


async def get_progress(dialog_manager: DialogManager, **kwargs: Any) -> dict[str, Any]:
    return {
        "name": dialog_manager.dialog_data.get("name"),
        "progress": dialog_manager.dialog_data.get("progress", 0),
    }
