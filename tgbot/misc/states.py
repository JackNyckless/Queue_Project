from aiogram.dispatcher.filters.state import StatesGroup, State
from tgbot.funcs.read_check import subjects_read


class Actions(StatesGroup):
    ADD = State()
    REMOVE = State()
