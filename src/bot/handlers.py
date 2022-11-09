from telebot import TeleBot

from src.bot import menu
from src.bot import cmds
from src.bot import text
from src.bot import callbacks
from src.bot import contact


def setup_handlers(bot: TeleBot):
    bot.register_message_handler(cmds.start, commands=['start'])
    # bot.register_message_handler(menu.main, func=lambda message: message.text == '🍎')
    # bot.register_message_handler(menu.admin, func=lambda message: message.text == '🐨')

    bot.register_callback_query_handler(callbacks.handlers, func=lambda call: True)

    bot.register_message_handler(text.handler, content_types=['text'])
    # bot.register_message_handler(contact.get_contact, content_types=['contact'])

