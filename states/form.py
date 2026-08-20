from aiogram.fsm.state import StatesGroup, State

class AppealForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State() # Jańadan qosıldı
    waiting_for_direction = State()
    waiting_for_group = State()
    waiting_for_course = State()
    waiting_for_appeal = State()
