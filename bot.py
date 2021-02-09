import telebot
from telebot import types

bot = telebot.TeleBot('1563221611:AAETbd_iQcs2FnulVsAbyK-XYCyer0UXcjQ')


# здесь обрабатываем команды /команда
@bot.message_handler(commands=['start'])
def start_handler(message):
    msg = '''Привет, пани!
    Я библоитечный бот.'''
    main_menu(message.chat.id)  # уникальный номер твоего чата с ботом


# здесь обрабатываем сообщения
@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.text == 'Программирование':
        # здесь с инлайн кнопками
        show_book(message.chat.id)
    elif message.text == 'Фантастика':
        otvet = 'Стругацикие\nЛукьяненко'
        msg_out = bot.send_message(message.chat.id, otvet)
    elif message.text == 'Биотехнологии':
        link_to_book(message.chat.id)
    elif message.text == 'Убрать клавиатуру':
        clear_keyboard(message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Я вас не понял')


# здесь обрабатываем коллбэки
@bot.callback_query_handler(func=lambda call: True)
def download_book(call):
    dannye = call.data  # это данные которые мы сами раньше составили в качестве callback_data
    if dannye.startswith('epub='):
        # где то здесь мы нашли путь к нужному файлу
        # отдадим его
        with open('001.pdf', 'rb') as file:
            bot.send_document(call.message.chat.id, file)


def main_menu(chat_id):
    menu_buttons = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    menu_buttons.add('Программирование', 'Фантастика', 'Биотехнологии', 'Убрать клавиатуру')
    msg = 'Выберите категорию 👇'
    bot.send_message(chat_id, msg, reply_markup=menu_buttons)


# Кнопки - ссылки
def link_to_book(chat_id):
    link_buttons = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton(text='сходи туда', url='https://www.tut.by/')
    link_buttons.add(btn)
    msg = 'Здесь тут бай 👇'
    bot.send_message(chat_id, msg, reply_markup=link_buttons)


# удаляет клавиатуру и убирает сообщение об этом
def clear_keyboard(chat_id):
    keyboard = telebot.types.ReplyKeyboardRemove()
    msg = bot.send_message(chat_id, '-', reply_markup=keyboard)
    bot.delete_message(chat_id, msg.message_id)


def show_book(chat_id):
    # где-то тут мы подезли в файл(базу) и достали список книжек
    book_list = {'Книга 1': '001', 'Книга 2': '002', 'Книга 3': '003', 'Книга 4': '004'}
    # импортировали только объект types чтоб меньше писать
    books_buttons = types.InlineKeyboardMarkup()  # пока пустой список
    for key, value in book_list.items():
        books_buttons.add(types.InlineKeyboardButton(text=key, callback_data="book_id=" + value),
                          types.InlineKeyboardButton(text='формат epub', callback_data="epub=" + value),
                          types.InlineKeyboardButton(text='формат fb2', callback_data="fb2=" + value))
    bot.send_message(chat_id, 'Выберите формат', reply_markup=books_buttons)


bot.polling()