import telebot
from db import Database

with open('set/.env', 'r') as file:
    lines = file.readlines()
    BOT_KEY, PASS_KEY = lines[0].strip(), lines[1].strip()

bot = telebot.TeleBot(BOT_KEY)
db = Database('db/database.db')

hideBoard = telebot.types.ReplyKeyboardRemove()

@bot.message_handler(commands=['start'])
def start(message):
    if (not db.user_exists(str(message.from_user.id))):
        bot.send_message(message.chat.id, f'Здравствуйте, <b>{message.from_user.first_name}!</b> Вам нужно авторизоваться, введите ключ.', parse_mode='html', reply_markup=hideBoard)
        bot.register_next_step_handler_by_chat_id(message.chat.id, authtorization)
    else:
        bot.send_message(message.chat.id, f'Здравствуйте, <b>{message.from_user.first_name}!</b> Продолжаем работу.\nЕсли нужна помощь, введите /help', parse_mode='html', reply_markup=hideBoard)

def authtorization(message):
    if message.text == PASS_KEY:
        db.add_user(message.from_user.id)
        bot.send_message(message.chat.id, f'<b>Отлично, вы авторизованы!</b>\nЖдём нового клиента. Если нужна помощь, введите /help', parse_mode='html')
    else:
        bot.send_message(message.chat.id, f'Ключ не подошел.')


@bot.message_handler(commands=['stop'])
def del_user(message):
    if (db.user_exists(str(message.from_user.id))):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton("отмена"))
        markup.add(telebot.types.KeyboardButton("да"))
        bot.send_message(message.chat.id, f'Вы уверены, что хотите перестать получать данные клиентов?', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(message.chat.id, del_user_processing)
    else:
        bot.send_message(message.chat.id, f'Вы и так не авторизованы.')

def del_user_processing(message):
    if message.text.lower() == "отмена":
        bot.send_message(message.chat.id, f'Хорошо, вы продолжите получать данные клиентов.', parse_mode='html', reply_markup=hideBoard)
        return
    elif message.text.lower() == "да":
        bot.send_message(message.chat.id, f'Хорошо, <b>{message.from_user.first_name}!</b> Вы больше не будете получать данные о клиентах.', parse_mode='html', reply_markup=hideBoard)
        db.del_user(message.from_user.id)

@bot.message_handler(commands=['view_comments'])
def view_comments(message):
    if (db.user_exists(str(message.from_user.id))):
        comments = db.view_comments()
        bot.send_message(message.chat.id, f'Сейчас добавлены следующие комментарии:', parse_mode='html')
        all_comments = ""
        for i in range(len(comments)):
            all_comments += f'<b>{i + 1}.</b>\n{comments[i][2]}\n<b>{comments[i][1]}</b>\n\n'
        bot.send_message(message.chat.id, all_comments, parse_mode='html', reply_markup=hideBoard)
    else:
        bot.send_message(message.chat.id, f'Вы не авторизованы. Введите ключ.')

@bot.message_handler(commands=['add_comment'])
def add_comment(message):
    if (db.user_exists(str(message.from_user.id))):
        if len(db.view_comments()) < 3:
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(telebot.types.KeyboardButton("отмена"))
            bot.send_message(message.chat.id, f'Какое у комментатора <b>имя</b>?', parse_mode='html', reply_markup=markup)
            bot.register_next_step_handler_by_chat_id(message.chat.id, add_comment_request_name)
        else:
            bot.send_message(message.chat.id, f'Нельзя добавить больше трёх комментариев.', parse_mode='html', reply_markup=hideBoard)
    else:
        bot.send_message(message.chat.id, f'Вы не авторизованы. Введите ключ.')

def add_comment_request_name(message):
    if message.text.lower() == "отмена":
        bot.send_message(message.chat.id, f'Хорошо, не будем ничего добавлять.', parse_mode='html', reply_markup=hideBoard)
    else:
        global name
        name = message.text
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton("отмена"))
        bot.send_message(message.chat.id, f'Отлично, теперь отправьте текст комментария.', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(message.chat.id, add_comment_request_text)

def add_comment_request_text(message):
    if message.text.lower() == "отмена":
        bot.send_message(message.chat.id, f'Хорошо, не будем ничего добавлять.', parse_mode='html', reply_markup=hideBoard)
    else:
        text = message.text

        db.add_comment(name, text)
        bot.send_message(message.chat.id, f'Комментарий <b>успешно</b> добавлен!', parse_mode='html', reply_markup=hideBoard)

@bot.message_handler(commands=['edit_comment'])
def edit_comment(message):
    if (db.user_exists(str(message.from_user.id))):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton("отмена"))
        btns = [telebot.types.KeyboardButton(f"{i + 1}") for i in range(len(db.view_comments()))]
        markup.row(*btns)

        bot.send_message(message.chat.id, f'Какой по счету комментарий изменить? (Ответьте цифрой)', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(message.chat.id, edit_comment_request_name)
    else:
        bot.send_message(message.chat.id, f'Вы не авторизованы.  Введите ключ.')

def edit_comment_request_name(message):
    if message.text.isdigit():
        global edit_comment_id

        num = int(message.text)
        comments = db.view_comments()
        edit_comment_id = comments[num - 1][0]

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton("отмена"))
        markup.add(telebot.types.KeyboardButton("изменить только текст"))

        bot.send_message(message.chat.id, f'Введите новое имя комментатора.', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(message.chat.id, edit_comment_name)
    else:
        bot.send_message(message.chat.id, f'Хорошо, не будем ничего изменять.', parse_mode='html', reply_markup=hideBoard)

def edit_comment_name(message):
    if str(message.text).lower() == 'отмена':
        bot.send_message(message.chat.id, f'Хорошо, не будем ничего изменять.', parse_mode='html', reply_markup=hideBoard)
        return
    if str(message.text).lower() == 'изменить только текст':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton("отмена"))

        bot.send_message(message.chat.id, f'Тогда введите новый текст комментария.', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(message.chat.id, edit_comment_text)
    else:
        edit_comment_name = message.text
        db.edit_comment_name(edit_comment_id, edit_comment_name)

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton("отмена"))

        bot.send_message(message.chat.id, f'Имя комментария измененено, теперь введите новый текст комментария.', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(message.chat.id, edit_comment_text)

def edit_comment_text(message):
    if str(message.text).lower() == 'отмена':
        bot.send_message(message.chat.id, f'Хорошо, не будем изменять текст комментария.', parse_mode='html', reply_markup=hideBoard)
    else:
        edit_comment_text = message.text
        db.edit_comment_text(edit_comment_id, edit_comment_text)

        bot.send_message(message.chat.id, f'Текст комментария успешно изменен.', parse_mode='html', reply_markup=hideBoard)

@bot.message_handler(commands=['del_comment'])
def del_comment(message):
    if (db.user_exists(str(message.from_user.id))):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton("отмена"))
        btns = [telebot.types.KeyboardButton(f"{i + 1}") for i in range(len(db.view_comments()))]
        markup.row(*btns)

        bot.send_message(message.chat.id, f'Какой по счету комментарий удалить? (Ответьте цифрой)', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(message.chat.id, del_comment_processing)
    else:
        bot.send_message(message.chat.id, f'Вы не авторизованы.  Введите ключ.')

def del_comment_processing(message):
    if message.text.isdigit():
        num = int(message.text)
        comments = db.view_comments()
        del_comment_id = comments[num - 1][0]

        db.del_comment(del_comment_id)
        bot.send_message(message.chat.id, f'Комментарий <b>удален!</b>', parse_mode='html', reply_markup=hideBoard)
    else:
        bot.send_message(message.chat.id, f'Хорошо, не будем ничего удалять.', parse_mode='html', reply_markup=hideBoard)

@bot.message_handler(commands=['help'])
def help(message):
    if (db.user_exists(str(message.from_user.id))):
        bot.send_message(message.chat.id, "Этот бот показывает данные новых клиентов, заполнивших форму на сайте https://more-yacht.ru\nТакже вы можете просматривать, добавлять и удалять комментарии. \n\n"\
                                        "Вы можете управлять ботом, используя следующие команды:\n\n"\
                                        "<b>Основное</b>\n"\
                                        "/start - начало\n"\
                                        "/stop - перестать присылать данные\n\n"\
                                        "<b>Комментарии</b>\n"\
                                        "/view_comments - просмотреть список комментариев\n"\
                                        "/add_comment - добавить комментарий\n"\
                                        "/edit_comment - изменить комментарий\n"\
                                        "/del_comment - удалить комментарий", parse_mode='html', reply_markup=hideBoard)
    else:
        bot.send_message(message.chat.id, f'Вы не авторизованы. Введите ключ.')

@bot.message_handler()
def default(message):
    if db.user_exists(str(message.from_user.id)):
        bot.send_message(message.chat.id, f'Я не знаю команды "{message.text}"\nПопробуйте использовать команды из списка /help')
    else:
        authtorization(message)

def send_to_all_users(name, num, sel):
    for user in db.all_users():
        try:
            bot.send_message(user[0], f'<b>У нас новый клиент!</b>\n\n<b>Имя:</b> {name}\n<b>Номер телефона:</b> 8{num.replace(" ", "")}\n<b>Выбор клиента:</b> {sel}', parse_mode='html')
        except Exception as ex:
            print(ex)
            return "error"
    return "success"

def start_bot():
    bot.infinity_polling()

# if __name__ == "__main__":
#     bot.polling(none_stop=True)

# if __name__ == "bot.py":
#     bot.polling(none_stop=True)