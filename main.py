from aiogram import Bot, Dispatcher, executor, types
from constants import token
import logging
from sqlscript import SQLscript
from parse import currency, usd, eur, btc
import asyncio
from datetime import datetime

logging.basicConfig(level=logging.INFO)

bot = Bot(token)
dp = Dispatcher(bot)

db = SQLscript("BotDb")

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.row("USD", "EUR", "BTC")
markup.row("Добавить валюту")

time_markup = types.InlineKeyboardMarkup()

one = types.InlineKeyboardButton("1 час", callback_data="1")
two = types.InlineKeyboardButton("2 часа", callback_data="2")
twelve = types.InlineKeyboardButton("12 часов", callback_data="12")
twentyfour = types.InlineKeyboardButton("24 часа", callback_data="24")

time_markup.add(one)
time_markup.add(two)
time_markup.add(twelve)
time_markup.add(twentyfour)


@dp.callback_query_handler(lambda x: x.data)
async def button1_process(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Вы успешно выбрали время для получения уведомлений")

    time = int(callback_query.data) * 3600
    await notification(time, callback_query.from_user.id)


@dp.message_handler(commands=["start"])
async def start_answer(message: types.Message):
    await message.answer("Привет, это CurrencyBot!\nЗдесь вы можете узнать курсы валют и биткоина")
    await message.answer("Выберите валюту:", reply_markup=markup)


@dp.message_handler(commands=["help"])
async def help_answer(message: types.Message):
    await message.answer("Возникли вопросы?\nПишите сюда: @Vasily_Esipenko")


@dp.message_handler(commands=["notify"])
async def notify(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, True)
    else:
        db.update_subscription(message.from_user.id, True)
    await message.answer("Вы подписались на ежедневные уведомления о курсах валют!\nВы можете отписаться в любой момент с помощью команды /disable")
    await asyncio.sleep(0.5)
    await message.answer("Выберите время для уведомлений:", reply_markup=time_markup)

@dp.message_handler(commands=["disable"])
async def disable(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Ваши уведомления итак отключены.")
    else:
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписались от уведомлений!")


@dp.message_handler(content_types=["text"])
async def text_answer(message: types.Message):
    if message.text == "USD":
        await bot.send_chat_action(message.from_user.id, "typing")
        await message.answer(currency(usd)[33:38] + "₽")
    elif message.text == "EUR":
        await bot.send_chat_action(message.from_user.id, "typing")
        await message.answer(currency(eur)[33:38] + "₽")
    elif message.text == "BTC":
        await bot.send_chat_action(message.from_user.id, "typing")
        await message.answer(currency(btc)[33:41] + "$")
    elif message.text == "Добавить валюту":
        await bot.send_chat_action(message.from_user.id, "typing")
        await message.answer("В разработке...")
    else:
        await bot.send_chat_action(message.from_user.id, "typing")
        await message.answer("Извините, я вас не понял :(\nПопробуйте еще раз")


async def notification(wait_for, user_id):
    while True:
        await asyncio.sleep(wait_for)
        for i in db.get_subscriptions():
            if i[1] == str(user_id) and i[2] == True:
                await bot.send_message(user_id, f"Курс валют на сегодня\n1. Доллар: {currency(usd)[33:38]}₽\n2. Евро: {currency(eur)[33:38]}₽\n3. Биткоин: {currency(btc)[33:41]}$")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
