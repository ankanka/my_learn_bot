#https://t.me/Anna_LearnPython_bot

import ephem
from emoji import emojize
from glob import glob
import logging
from random import randint, choice
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
logging.basicConfig(filename='bot.log', level=logging.INFO)

import settings

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    print('Вызван .start')   
    context.user_data['emoji'] = get_smile(context.user_data)
    my_keyboard = ReplyKeyboardMarkup([['Прислать котика', 'test']])
    update.message.reply_text(
        f'Здравствуй, пользователь {context.user_data["emoji"]}!',
        reply_markup = my_keyboard
    )


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI) #выбирает эмодзи из списка
        return emojize(smile, use_aliases=True) #преобразовывает текст в иконку смайла
    return user_data['emoji']


planets = ['Mars', 'Venus', 'Mercury', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
def get_const(update, context):
    user_text = update.message.text.split()[1]
    if user_text in planets:
        f = eval(f'ephem. {user_text} (ephem.now())')
        const = ephem.constellation(f)
        update.message.reply_text(const)
def get_full_moon(update,context):
    full_moon_time = ephem.next_full_moon(ephem.now())
    update.message.reply_text(full_moon_time)
def word_count(update, context):
    text_to_count = update.message.text.split()
    try:
        if text_to_count == ' ':
            update.message.reply_text('Пустые значения не принимаются')

        else:
            output = len(text_to_count) - 1
            answer = f'{output} слова'
            update.message.reply_text(answer)
            
    except ZeroDivisionError:
        print('Деление на ноль')
cities = [
    'Москва', 'Ананьев', 'Воркута', 'Алметьевск', 'Киев', 'Воронеж', 
    'Жмеринка', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 
    'Казань', 'Нижний Новгород', 'Челябинск', 'Самара', 'Омск', 'Ялта',
    'Ростов-на-Дону', 'Урюпинск', 'Краснодар', 'Донецк', 'Килия', 'Астана'
]
def get_city(update, context):
    ut = update.message.text.split()[1]
    if ut in cities:
        a = list(ut)
        b = a[-1]
        c = b.lower()

        for city in cities:
            city = city.lower()
            if city[0] == c:
                answer = city.capitalize()
                update.message.reply_text(answer)
                cities.remove(answer)
                cities.remove(ut)
                break
                       
    else:
        update.message.reply_text('Город повторяется или его нет в списке')

def play_random_number(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!'
    elif user_number == bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ничья!'
    else:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, я выиграл!'
    return message

def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_number(user_number)
        except (TypeError, ValueError):
            message = 'Введите целое число'
    else:   
        message = "Введите число"
    update.message.reply_text(message)              

def send_cat_picture(update, context):
    cat_photos_list = glob('images/cat*.jp*g')  #ищем картинки
    cat_pic_filename = choice(cat_photos_list)  #получаем случайную картинку
    chat_id = update.effective_chat.id          #id чата с текущим пользователем
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb')) #rb - формат картинок, r - текста

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('get_full_moon', get_full_moon))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(MessageHandler(Filters.regex('/wordcount'), word_count))
    dp.add_handler(MessageHandler(Filters.regex('/planet'), get_const))
    dp.add_handler(MessageHandler(Filters.regex('/city'), get_city))


    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()
    
if __name__ == '__main__':
    main()

    