#https://t.me/Anna_LearnPython_bot

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import (greet_user, get_const, get_full_moon, get_city, talk_to_me,
                    send_cat_picture, user_coordinates, word_count, guess_number)

logging.basicConfig(filename='bot.log', level=logging.INFO)

import settings

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('get_full_moon', get_full_moon))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_picture)) # фильтр на то, чтоб реаоигровало только на текст "Прислать котика"
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.regex('/wordcount'), word_count))
    dp.add_handler(MessageHandler(Filters.regex('/planet'), get_const))
    dp.add_handler(MessageHandler(Filters.regex('/city'), get_city))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))


    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()
    
if __name__ == '__main__':
    main()

    