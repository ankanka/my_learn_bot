from random import randint, choice
from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
import settings

def play_random_number(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!'
    elif user_number == bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ничья!'
    else:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, я выиграл!'
    return message

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI) #выбирает эмодзи из списка
        return emojize(smile, use_aliases=True) #преобразовывает текст в иконку смайла
    return user_data['emoji'] # возвращает тот же эмодзи, что уже отправлялся пользователю

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Прислать котика', KeyboardButton('Мои координаты', request_location=True)]
    ])
    