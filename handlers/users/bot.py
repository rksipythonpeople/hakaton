from loader import cursor, connect, dp,bot
from aiogram import types
from utils.registration import *
from aiogram.dispatcher import FSMContext
import utils.func_change_bd as fcb
import re
import sqlite3 as sql
import handlers.keyboard as ak

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Начинаем наш диалог и проверяем БД, если нет человека,то регестрируем
@dp.message_handler(commands=['start'],state=None)
async def cmd_start(message: types.Message):

    user_id = message.from_user.id
    user_name = message.from_user.full_name
    result = cursor.execute("SELECT user_id,user_name,login,password FROM users").fetchall()

    id_list = []
    for i in range(len(result)):
        res = result[i]
        id,us_name,log,psswr = res
        id_list.append(id)
    if user_id in id_list: 
        if message.from_user.id in fcb.len_admin():
            await message.answer(f"Привет {user_name}. Рад снова тебя видеть",reply_markup=ak.admin_panel)
        else:
            await message.answer(f"Привет {user_name}. Рад снова тебя видеть")
    else:
        await message.answer(f"Привет {user_name}\nСейчас мы с тобой зарегистрируемся")
        await message.answer("Введите желаемый логин ")
        await UserInfo.login.set()

# Запоминаем логин и запрашиваем пароль
@dp.message_handler(content_types=["text"], state=UserInfo.login)
async def answer_login(message: types.Message, state: FSMContext):
    login = message.text
    await state.update_data(answerlog = login)
    await message.answer("Введите пароль\nПостарайтесь придумать посложнее")
    await UserInfo.password.set()

# Сохраняем логин и пароль в БД
@dp.message_handler(state=UserInfo.password)
async def answer_password(message: types.Message, state: FSMContext):
    password = message.text
    await state.update_data(answer_pass= password)
    data = await state.get_data()
    cursor.execute(f"""INSERT INTO users(user_id, user_name,login,password) VALUES({message.from_user.id}, '{message.from_user.full_name}','{data['answerlog']}','{data['answer_pass']}')""")
    connect.commit()
    await state.reset_state()
    await message.answer("Спасибо за регестрацию")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Команда HELP
@dp.message_handler(commands=['help'],state=None)
async def cmd_help(message: types.Message):
    await message.answer("Я помогу тебе в работе с сервисом GStore: подскажу информацию о товарах, помогу купить и активировать игру и т.д.")
    await message.answer("Если остались вопросы можешь мне их задать")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# # Получить свой ID
@dp.message_handler(commands=['profile'])
async def id_send(message: types.Message):
    await message.answer(f'Ваш ID: {message.from_user.id}')

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Назначить админа
@dp.message_handler(content_types=['text'])
async def make_user_admin(message: types.Message):
    if message.from_user.id in fcb.len_admin():
        if "Добавить админа" == message.text:
            await message.answer("Введите ID пользователя")
            await Admin_make.id.set()
        elif "Добавить хелпера" == message.text:
            await message.answer("Введите ID пользователя")
            await Helper_make.id.set()
        elif "Удалить админа" == message.text:
            await message.answer("Введите ID пользователя")
            await Admin_del.id.set()
        elif "Удалить хелпера" == message.text:
            await message.answer("Введите ID пользователя")
            await Helper_del.id.set()
        elif "Все админы" == message.text:
            await message.answer(f"Все админы: {fcb.len_admin()}")
    else:
        await message.answer("Недостаточно прав")
    

@dp.message_handler(state=Admin_make.id)
async def make2_user_admin(message: types.Message, state: FSMContext):
    
    if message.from_user.id in fcb.len_admin():
        if int(message.text) not in fcb.len_admin():
            admin_id = message.text
            await state.update_data(answer_id =admin_id)
            data = await state.get_data()
            fcb.add_admin(id_user= int(data["answer_id"]))
            await state.reset_state()
            await message.answer(f"Пользователь @id{admin_id} теперь админ")
            await dp.bot.send_message(int(admin_id), "Вы теперь админ")
        else:
            await message.answer(f"Этот пользователь уже админ")
            await state.reset_state()
    else:
        await message.answer("Недостаточно прав")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@dp.message_handler(state=Admin_make.id)
async def make2_user_helper(message: types.Message, state: FSMContext):
    if message.from_user.id in fcb.len_admin():
        if int(message.text) not in fcb.len_helper():
            helper_id = message.text
            await state.update_data(answer_id =helper_id)
            data = await state.get_data()
            fcb.add_helper(id_user= int(data["answer_id"]))
            await state.reset_state()
            await message.answer(f"Пользователь @id{helper_id} теперь хелпер")
            await dp.bot.send_message(int(helper_id), "Вы теперь хелпер")
        else:
            await message.answer(f"Этот пользователь уже хелпер")
            await state.reset_state()    
    else:
        await message.answer("Недостаточно прав")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@dp.message_handler(state=Admin_del.id)
async def del2_user_admin(message: types.Message, state: FSMContext): 
    if message.from_user.id in fcb.len_admin(): 
        if int(message.text) in fcb.len_admin():
            admin_id = message.text
            await state.update_data(answer_id =admin_id)
            data = await state.get_data()
            fcb.delete_admin(user_id= int(data["answer_id"]))
            await state.reset_state()
            await message.answer(f"Пользователь @id{admin_id} теперь не админ")
            await dp.bot.send_message(int(admin_id), "Вы теперь не админ")
        else:
            await message.answer(f"Этот пользователь ещё не админ")
            await state.reset_state()
    else:
        await message.answer("Недостаточно прав")


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@dp.message_handler(state=Helper_del.id)
async def del2_user_helper(message: types.Message, state: FSMContext): 
    if message.from_user.id in fcb.len_admin():
        if int(message.text) in fcb.len_helper():
            helper_id = message.text
            await state.update_data(answer_id =helper_id)
            data = await state.get_data()
            fcb.delete_helper(user_id= int(data["answer_id"]))
            await state.reset_state()
            await message.answer(f"Пользователь @id{helper_id} теперь не хелпер")
            await dp.bot.send_message(int(helper_id), "Вы теперь не хелпер")
        else:
            await message.answer(f"Этот пользователь ещё не хелпер")
            await state.reset_state()
    else:
        await message.answer("Недостаточно прав")

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# user_helper = {}

# @dp.message_handler(content_types=['text'],state=None)
# async def ask(message: types.Message):
#     if 'Задать вопрос' == message.text:
#         await message.answer("Какой у вас вопрос?")
#         await Ask.ask_qu.set()

# @dp.message_handler(state=Ask.ask_qu)
# async def ask2(message: types.Message, state: FSMContext):
#     qu = message.text
#     await state.update_data(ask_qu = qu)
#     data = await state.get_data()

    