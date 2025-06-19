"""_summary_"""

from aiogram.fsm.state import State, StatesGroup


class Files(StatesGroup):
    """_summary_"""

    SCROLLGROUP = State()


class Multiselect(StatesGroup):
    """_summary_"""

    MULTISELECT = State()
    MUTLTIDOWNOLOAD = State()
    MULTIDELETE = State()


class Create(StatesGroup):
    """_summary_"""

    TYPE = State()
    FOLDER = State()
    FILES = State()
    UPLOAD = State()
