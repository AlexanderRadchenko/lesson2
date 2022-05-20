"""
Домашнее задание №1

Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите
  бота отвечать, в каком созвездии сегодня находится планета.

"""
import logging
import settings
import ephem
from datetime import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

'''
PROXY = {
    'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {
        'username': 'learn',
        'password': 'python'
    }
}
'''

def greet_user(update, context):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)

#получаем координаты планеты
def get_planets(update, context):
    user_text = update.message.text.split() #раздлеяем /planet и название планеты
    if len(user_text)==2 and user_text[0].lower()=='/planet' and user_text[1] in ("jupiter", 'jupyter', 'юпитер', "марс", 'mars', "earth", 'земля',"venus", 'венера'): #если нет лишних элементов и планета в списке
        if get_code(user_text[1]):
            update.message.reply_text(get_code(user_text[1]))

def talk_to_me(update, context):
    user_text = update.message.text
    update.message.reply_text(user_text)

#получение координат планеты на текущий день
def get_code(planet):
    today_date = (datetime.today().strftime('%Y-%m-%d'))
    if planet.lower() in  ("jupiter", 'jupyter', 'юпитер'):
        my_planet = ephem.Jupiter(today_date)
    if planet.lower() in  ("марс", 'mars'):
        my_planet = ephem.Mars(today_date)
    if planet.lower() in  ("earth", 'земля'):
        my_planet = ephem.Earth(today_date)
    if planet.lower() in  ("venus", 'венера'):
        my_planet = ephem.Venus(today_date)
    try:
        return ephem.constellation(my_planet)
    except NameError:
        pass


def main():
    mybot = Updater(settings.API_KEY,  use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, get_planets))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
   