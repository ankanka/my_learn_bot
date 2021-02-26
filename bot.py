#https://t.me/Anna_LearnPython_bot

import logging
import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
logging.basicConfig(filename='bot.log', level=logging.INFO)

import settings

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    print('Вызван .start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')

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
                    

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('get_full_moon', get_full_moon))
    dp.add_handler(MessageHandler(Filters.regex('/wordcount'), word_count))
    dp.add_handler(MessageHandler(Filters.regex('/planet'), get_const))
    dp.add_handler(MessageHandler(Filters.regex('/city'), get_city))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()
    
if __name__ == '__main__':
    main()

    