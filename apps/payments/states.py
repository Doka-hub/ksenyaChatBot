from aiogram.fsm.state import State, StatesGroup


class ChoosePaymentState(StatesGroup):
    email = State()
    type = State()


class PaymentApproveState(StatesGroup):
    paid = State()
    screenshot = State()
