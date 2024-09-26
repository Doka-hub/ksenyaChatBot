from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    fullname = State()
    company_name = State()
    city = State()
    phone = State()


class PaymentFormState(StatesGroup):
    email = State()
    type = State()
