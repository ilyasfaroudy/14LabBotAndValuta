import telebot
from googletrans import Translator
from telebot import types

bot = telebot.TeleBot('6759432363:AAER2pMSfIN7c_Z6B6gqIq_wMnmlN6znCqs')
translator = Translator()
languages = {
    "английский": "en",
    "испанский": "es",
    "французский": "fr",
    "немецкий": "de",
    "итальянский": "it",
}
def send_welcome_message(chat_id):
    welcome_message = "Привет! Я бот-переводчик. Введите слово, которое вы хотите перевести."
    bot.send_message(chat_id, welcome_message)


def create_language_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(text=lang) for lang in languages.keys()]
    keyboard.add(*buttons)
    return keyboard
def create_translate_again_button():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Перевести снова"))
    return keyboard
@bot.message_handler(commands=['start'])
def handle_start(message):
    send_welcome_message(message.chat.id)
    bot.register_next_step_handler(message, process_word)
def process_word(message):
    word = message.text
    bot.send_message(message.chat.id, "Выберете язык из таблицы, на который вам нужно перевести:", reply_markup=create_language_keyboard())
    bot.register_next_step_handler(message, process_translation, word)
def process_translation(message, word):
    dest_lang = message.text.lower()
    if dest_lang in languages:
        src_lang = 'ru'
        try:
            translation = translator.translate(word, src=src_lang, dest=languages[dest_lang]).text
            bot.send_message(message.chat.id, f"Перевод: {translation}", reply_markup=create_translate_again_button())
            bot.register_next_step_handler(message, process_translate_again, word)
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка перевода: {e}")
    else:
        bot.send_message(message.chat.id, "Неверный язык. Выберете язык из списка.")

def process_translate_again(message, word):
    if message.text == "Перевести снова":
        bot.send_message(message.chat.id, "Введите слово, которое вы хотите перевести:", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_word)
    else:
        bot.send_message(message.chat.id, "Неверная команда. Выберете 'Перевести снова' из списка.")
bot.polling()
