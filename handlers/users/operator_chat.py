from loader import cursor, connect, dp,bot
from aiogram import types

ids_users = []

@dp.message_handler(content_types=["text","photo"])
async def start_operator_find(message: types.Message):
    if "позови оператора" in message.text.lower():
        await message.answer("Идёт поиск свободного оператора...")
        ids_users.append(message.text)
        return ids_users

@dp.message_handler(content_types=["text","photo"])
async def start_user_find(message: types.Message):
    if "помочь" in message.text.lower():
        await message.answer(f'Пользователи: {ids_users}')
    # result = cursor.execute("SELECT user_id,user_name FROM users").fetchall()

# async def messanger(message):
#     if message.from_user.chat_id == user1_chat_id:
#         await dp.bot.send_message(user2_chat_id, message.text)
#     else:
#         await dp.bot.send_message(user1_chat_id, message.text)