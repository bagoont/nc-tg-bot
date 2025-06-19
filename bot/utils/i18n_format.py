from typing import TYPE_CHECKING, Any

from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text

if TYPE_CHECKING:
    from aiogram_i18n import I18nContext


class I18NFormat(Text):
    def __init__(self, key: str, when: WhenCondition = None):
        super().__init__(when)
        self.key = key

    async def _render_text(self, data: dict[str, Any], manager: DialogManager) -> str:
        i18n: I18nContext = manager.middleware_data["i18n"]
        await i18n.set_locale("ru")
        return i18n(self.key, **data.get("text", {}))
