from aiogram.fsm.state import State, StatesGroup


class FSMState(StatesGroup):
    upload_style = State()
    upload_content = State()
    transfer_style = State()
