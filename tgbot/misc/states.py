from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    bloger = State()
    phone_number = State()
    product = State()


class  BlogerState(StatesGroup):
    id = State()


class BlogerUpdateState(StatesGroup):
    id = State()
    phone_number = State()


class SendAdState(StatesGroup):
    message = State()
    ready = State()