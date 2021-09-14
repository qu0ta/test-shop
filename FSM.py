from aiogram.dispatcher.filters.state import StatesGroup, State


class ChoicePay(StatesGroup):
    amount = State()


class AddItem(StatesGroup):
    name = State()
    description = State()
    price = State()
    additem = State()