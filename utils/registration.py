from aiogram.dispatcher.filters.state import StatesGroup,State

class UserInfo(StatesGroup):
    login = State()
    password = State()

class Admin_make(StatesGroup):
    id = State()

class Helper_make(StatesGroup):
    id = State()

class Admin_del(StatesGroup):
    id = State()

class Helper_del(StatesGroup):
    id = State()