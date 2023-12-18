from aiogram.fsm.state import State, StatesGroup


class GroupSelectionState(StatesGroup):
    educational_level_selection = State()
    group_selection = State()
