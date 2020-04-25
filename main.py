import telebot
from telebot import types
import requests as r
from bs4 import BeautifulSoup as BS
import constants

usd = "https://www.google.com/search?q=курс+доллара&oq=rehc+&aqs=chrome.4.69i57j69i59l3j0l4.3491j1j7&sourceid=chrome&ie=UTF-8"
eur = "https://www.google.com/search?q=курс+евро&oq=rehc+tdhj&aqs=chrome.1.69i57j0l7.3337j1j7&sourceid=chrome&ie=UTF-8"
btc = "https://www.google.com/search?sxsrf=ALeKk00wereP6f5lSOJitVaaHdgafDgl8A%3A1585588151469&ei=tyeCXr6XHIGRmwWC7rqABQ&q=btc+rate+usd&oq=btc+rate+&gs_lcp=CgZwc3ktYWIQAxgAMgwIABAUEIcCEEYQggIyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywE6BAgAEEc6BwgjEOoCECc6BAgjECc6BQgAEIMBOgIIADoECAAQQzoHCAAQgwEQQzoMCAAQgwEQQxBGEIICOgoIABCDARAUEIcCOgcIABAUEIcCOgQIABAKUKGKLFibuCxgiMUsaAJwAXgAgAGIAYgB1AmSAQQwLjEwmAEAoAEBqgEHZ3dzLXdperABCg&sclient=psy-ab"


def currency(ccy):
    url = r.get(ccy)
    soup = BS(url.content, "html.parser")
    res = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")
    return str(res[1])


bot = telebot.TeleBot(constants.token)

markup = types.ReplyKeyboardMarkup(True, True)
btn1 = types.KeyboardButton("USD")
btn2 = types.KeyboardButton("Euro")
btn3 = types.KeyboardButton("BTC")
markup.add(btn1, btn2, btn3)


@bot.message_handler(commands=["start"])
def start_answer(message):
    bot.send_message(message.chat.id, "Привет! Это CurrencyBot.\n Выберите валюту, курс которой вы хотите посмотреть",
                     reply_markup=markup)


@bot.message_handler(commands=["help"])
def help_answer(message):
    bot.send_message(message.chat.id, "Возникли вопросы?\n Пишите: @Vasily_Esipenko")


@bot.message_handler(content_types=["text"])
def text_answer(message):
    if message.text == "USD":
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, "Курс доллара: " + currency(usd)[33:38])
    elif message.text == "Euro":
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, "Курс евро: " + currency(eur)[33:38])
    elif message.text == "BTC":
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, "Курс BTC: " + currency(btc)[33:41] + "$")


bot.polling()
