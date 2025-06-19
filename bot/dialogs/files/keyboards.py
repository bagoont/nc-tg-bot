import operator
from typing import Any

from aiogram_dialog.widgets.kbd import Multiselect, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format

from bot.core import settings


def sg_fsnodes(on_click: Any, *, items_key: str) -> ScrollingGroup:
    return ScrollingGroup(
        Select(
            Format("{item[0]} {item[1].name}"),
            id="select",
            item_id_getter=lambda item: item[1].file_id,
            items=items_key,
            on_click=on_click,
        ),
        id="sg_fsnodes",
        width=1,
        height=settings.TG_SCROLLING_HEIGHT,
    )


def sg_documents(on_click: Any, *, items_key: str) -> ScrollingGroup:
    return ScrollingGroup(
        Select(
            Format("❌ {item.file_name}"),
            id="select",
            item_id_getter=lambda doc: doc.file_unique_id,
            items=items_key,
            on_click=on_click,
        ),
        id="sg_documents",
        width=1,
        height=settings.TG_SCROLLING_HEIGHT,
    )


def ms_sg_fsnodes(*, items_key: str) -> ScrollingGroup:
    return ScrollingGroup(
        Multiselect(
            Format("✅ {item.name}"),
            Format("☑️ {item.name}"),
            id="multiselect",
            item_id_getter=operator.attrgetter("file_id"),
            items=items_key,
        ),
        id="ms_sg_fsnodes",
        width=1,
        height=settings.TG_SCROLLING_HEIGHT,
    )
