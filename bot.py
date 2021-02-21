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

planets = ['Mars', 'Venus', 'Earth', 'Mercury', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

def get_const(update, context):
    user_text = update.message.text
    if user_text in planets:
        f = eval(f'ephem. {user_text} (ephem.now())')
        const = ephem.constellation(f)
        update.message.reply_text(const)
        
def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', get_const))
    dp.add_handler(MessageHandler(Filters.text, get_const))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()
    
if __name__ == '__main__':
    main()

    