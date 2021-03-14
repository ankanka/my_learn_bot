import ephem
from glob import glob
from random import choice
from utils import get_smile, play_random_number, main_keyboard

def greet_user(update, context):
    print('Вызван .start')   
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f'Здравствуй, пользователь {context.user_data["emoji"]}!',
        reply_markup = main_keyboard()
    )

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text
    print(text)
    update.message.reply_text(f'{text} {context.user_data["emoji"]}')

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

def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}!",
        reply_markup=main_keyboard()
    )

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
